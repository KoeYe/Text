import os
import argparse
import gradio as gr

def render_3d_models(output_base_dir, prompt_path):
    # 读取prompt文件内容
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompts = f.readlines()
    
    # 创建一个映射，用短prompt找到完整prompt
    prompt_map = {}
    for prompt in prompts:
        prompt = prompt.strip()
        if prompt:  # 忽略空行
            short_prompt = prompt[:5]  # 取前5个字符
            prompt_map[short_prompt] = prompt

    with gr.Blocks() as demo:
        gr.Markdown("# 3D Model Gallery")

        # 获取所有实验文件夹
        experiment_dirs = [d for d in os.listdir(output_base_dir) 
                         if os.path.isdir(os.path.join(output_base_dir, d))]
        
        for experiment_dir in experiment_dirs:

            
            # 获取实验文件夹下的所有prompt文件夹
            exp_path = os.path.join(output_base_dir, experiment_dir)
            prompt_dirs = [d for d in os.listdir(exp_path) 
                         if os.path.isdir(os.path.join(exp_path, d))]
            
            if len(prompt_dirs) == 0:
                continue

            gr.Markdown(f"## Experiment: {experiment_dir}")

            # 每行显示3个模型
            models_per_row = 3
            for i in range(0, len(prompt_dirs), models_per_row):
                with gr.Row():
                    current_row_dirs = prompt_dirs[i:i + models_per_row]
                    for prompt_dir in current_row_dirs:
                        # 从文件夹名称中提取prompt前5个字符
                        short_prompt = prompt_dir.split('_', 1)[1] if '_' in prompt_dir else prompt_dir
                        # 获取完整的prompt
                        full_prompt = prompt_map.get(short_prompt, prompt_dir)
                        
                        # 获取该prompt文件夹下的第一个glb文件
                        model_dir = os.path.join(exp_path, prompt_dir)
                        model_files = [f for f in os.listdir(model_dir)
                                    if f.endswith('.glb')]
                        if model_files:  # 如果存在模型文件
                            with gr.Column():
                                gr.Markdown(f"### {full_prompt}")
                                gr.Model3D(os.path.join(model_dir, model_files[0]))
    demo.launch()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Render 3D models')
    parser.add_argument('--output_dir', type=str, default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'hunyuan_test'), help='Output directory for generated models')
    parser.add_argument('--prompt_path', type=str, default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'prompt', 'prompt_with_text.txt'), help='Prompt file path')
    args = parser.parse_args()

    render_3d_models(args.output_dir, args.prompt_path)