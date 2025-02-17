# Text to 3D

## Install

Some dependencies are not available on pip install, so we need to install them manually.
```bash
cd submodules

pip install -e ./diff-gaussian-rasterization

pip install triton-3.2.0-cp312-cp312-win_amd64.whl
```

## Run

 - run `shape-text.ipynb` to generate 3D shape by using SHAP-E from OpenAI
 - run `Huanyuan3D-1` to using Huanyuan3D from Tencent (refer to README.md in the Hunyuan3D repo)
