# Text to 3D

## Install

Some dependencies are not available on pip install, so we need to install them manually.
```bash
cd submodules

pip install -e ./diff-gaussian-rasterization

pip install triton-3.2.0-cp312-cp312-win_amd64.whl

pip install torch
```

## Run

 - run `shape-text.ipynb` to generate 3D shape by using SHAP-E from OpenAI
 - run `Huanyuan3D-1` to using Huanyuan3D from Tencent. Refer to the [official site](https://3d.hunyuan.tencent.com) for more details.
