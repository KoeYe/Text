# Text to 3D

## Install
Preparing install for the project
``` bash
pip install -r requirements.txt
```

Preparing the third-party install
```bash
cd lib
git submodule update --init --recursive
./third-party-install.sh
```

## Run

 - run `shape-text.ipynb` to generate 3D shape by using SHAP-E from OpenAI
 - run `Huanyuan3D-1` to using Huanyuan3D from Tencent (refer to [README.md](lib/Hunyuan3D-1/README.md))
