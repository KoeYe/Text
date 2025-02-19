import os
import subprocess
import time
import argparse
from tqdm import tqdm
import torch
from PIL import Image

from hy3dgen.rembg import BackgroundRemover
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline, FaceReducer, FloaterRemover, DegenerateFaceRemover
from hy3dgen.text2image import HunyuanDiTPipeline
from hy3dgen.texgen import Hunyuan3DPaintPipeline

def text_to_3d(prompt='a car', t2i=None, i23d=None):
    rembg = BackgroundRemover()
    image = t2i(prompt)
    image = rembg(image)
    mesh = i23d(image, num_inference_steps=30, mc_algo='mc')[0]
    mesh = FloaterRemover()(mesh)
    mesh = DegenerateFaceRemover()(mesh)
    mesh = FaceReducer()(mesh, max_facenum=5000)
    return mesh, image

def paint_mesh(mesh, image, pipeline=None):
    mesh = pipeline(mesh, image)
    return mesh

def save(mesh, image, output_dir):
    mesh.export(os.path.join(output_dir, 'mesh.glb'))
    image.save(os.path.join(output_dir, 'image.png'))

def generate_3d_models(prompts_file, output_base_dir):
    # 确保输出目录存在
    os.makedirs(output_base_dir, exist_ok=True)

    t2i = HunyuanDiTPipeline('Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled')
    i23d = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained('tencent/Hunyuan3D-2')
    paint_pipeline = Hunyuan3DPaintPipeline.from_pretrained('tencent/Hunyuan3D-2')

    # 读取prompts文件
    with open(prompts_file, 'r', encoding='utf-8') as f:
        prompts = [line.strip() for line in f.readlines() if line.strip()]

    # 处理每个prompt
    for i, prompt in tqdm(enumerate(prompts), total=len(prompts), desc="Processing prompts"):
        print(f"\n[{i+1}/{len(prompts)}] Processing: {prompt}")

        # 为每个prompt创建独立的输出目录
        output_dir = os.path.join(output_base_dir, f"{prompt.replace(' ', '_')[0:10]}")
        os.makedirs(output_dir, exist_ok=True)

        try:
            mesh, image = text_to_3d(prompt, t2i, i23d)
            mesh = paint_mesh(mesh, image, paint_pipeline)
            save(mesh, image, output_dir)

            print(f"Successfully generated 3D model for: {prompt}")
        except subprocess.CalledProcessError as e:
            print(f"Error generating 3D model for: {prompt}")
            print(f"Error: {str(e)}")
            continue

        # 等待一小段时间再处理下一个
        time.sleep(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate 3D models using Hunyuan3D')
    parser.add_argument('--prompts_file', type=str,
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'prompt', 'prompt_with_text.txt'),
        help='Path to the prompts file')
    parser.add_argument('--output_dir', type=str,
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'hunyuan_test'),
        help='Output directory for generated models')
    parser.add_argument('--experiment_name', type=str, default='3dwithtext', help='Experiment name')
    parser.add_argument('--render', type=bool, default=False, help='Render the generated models')
    args = parser.parse_args()

    # 配置路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_file = os.path.join(current_dir, args.prompts_file)
    output_base_dir = os.path.join(current_dir, args.output_dir)

    experiment_name = args.experiment_name + time.strftime("%Y%m%d_%H%M%S")
    output_base_dir = os.path.join(current_dir, args.output_dir, experiment_name)

    # 检查prompts文件是否存在
    if not os.path.exists(prompts_file):
        raise FileNotFoundError(f"Prompts file not found: {prompts_file}")

    # 开始生成
    print(f"Starting batch generation...")
    print(f"Reading prompts from: {prompts_file}")
    print(f"Saving results to: {output_base_dir}")

    try:
        generate_3d_models(prompts_file, output_base_dir)
    except Exception as e:
        print(f"Error: {str(e)}")

    if args.render:
        command = f"python test/render.py --output_dir {output_base_dir}"
        subprocess.run(command, shell=True, check=True)