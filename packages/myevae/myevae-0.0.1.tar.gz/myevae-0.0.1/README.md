# MyeVAE

A variational autoencoder leveraging multi-omics for risk prediction in newly diagnosed multiple myeloma patients.

<p align="left"><img src="https://raw.githubusercontent.com/JiaGengChang/myevae/refs/heads/main/assets/myeVAE.png" alt="Illustration of MyeVAE architecture, hosted on github" width="600"></p>

This Python package contains the code to train and run SHAP on MyeVAE. No GPU is required.

# Install

Install through PyPI
```bash
pip install myevae[parallel]
```
or through conda
```
conda install myevae[parallel]
```

This installation may take up to 5 minutes if you do not have PyTorch ≥ 2.0 installed in your python environment.

Installing with the `[parallel]` optional dependency is highly recommended as it allows parallelization of grid search using `dask` and `distributed` backends.

# Step-by-step guide

## 1. Download data

Download the raw multi-omics dataset and example outputs from the following link:

1. Input datasets are stored at https://myevae.s3.us-east-1.amazonaws.com/example_inputs.tar.gz

2. Example output files are stored at https://myevae.s3.us-east-1.amazonaws.com/example_outputs.tar.gz

Please use the download links sparingly.

If you use the AWS S3 CLI, the bucket ARN is `arn:aws:s3:::myevae` - you can list its contents and download specific files.

## 2. (Optional) Feature preprocessing

As there are over 50,000 raw features and contains missing values, this step performs supervised-feature selection, scaling, and imputation.

```bash
myevae preprocess \
    -e [endpoint: os | pfs] \
    -i [/inputs/folder]
```

Processed files will be stored in `train_features_[os|pfs]_processed.csv` and `valid_features_[os|pfs]_processed.csv`.

Preprocessing of features is resource-intensive. Alternatively, proceed to step 3 using the processed features in the example input data (https://myevae.s3.us-east-1.amazonaws.com/example_inputs.tar.gz).

```
train_features_os_processed.csv
train_features_pfs_processed.csv
valid_features_os_processed.csv
valid_features_pfs_processed.csv
```

## 3. Fit model

Place the hyperparameter grid (`param_grid.py`) in `/params/folder`.

```bash
myevae train \
    -e [endpoint: os | pfs] \
    -n [model_name] \
    -i [/inputs/folder] \
    -p [/params/folder] \
    -t [nthreads] \
    -o [/output/folder]
```

## 4. Score model

```bash
myevae score \
    -e [endpoint: os | pfs] \
    -n [model_name] \
    -i [/inputs/folder] \
    -o [/output/folder]
```

## 5. Generate SHAP plots
```bash
myevae shap \
    -e [endpoint: os | pfs] \
    -n [model_name] \
    -i [/inputs/folder] \
    -o [/output/folder]
```

# Requirements

## Files

<p align="left"><img src="https://raw.githubusercontent.com/JiaGengChang/myevae/refs/heads/main/assets/directory.png" alt="Illustration of folder structure, hosted on github" width="300"></p>


### Input csv files
Place the following `.csv` files inside your inputs folder (`/inputs/folder`), and the `param_grid.py` inside your preferred folder. Also create an empty folder for the outputs.
```bash
|-----/inputs
|     |----train_features.csv [ feature matrix of training samples ]
|     |----valid_features.csv [ feature matrix of validation samples ]
|     |----train_labels.csv [ survival files of training samples ]
|     |____valid_labels.csv [ survival files of validation samples ]
|-----/params
|     |____param_grid.py
|_____/output
      |____[output files created here]
```

For `features*.csv` and `labels*.csv`, column 0 is read in as the index, which should be the patient IDs.

Example input csv files can be downloaded from AWS S3 link above.

### Hyperparameter grid python file
Place a python file named `param_grid.py` containing the hyperparameter grid dictionary in the params folder (`/params/folder`). This contains the set of hyperparameters that grid search will be performed on. Otherwise, use the default provided in `src/param_grid.py`.

The example parameter grid provides 3 options for z_dim (dimension of latent space): 8, 16, or 32:
```python
from torch.nn import LeakyReLU, Tanh

# the default hyperparameter grid for debugging uses
# this is not meant to be used for real training, as the search space is only on z_dim
param_grid = {
    'z_dim': [8,16,32],
    'lr': [5e-4], 
    'batch_size': [1024],
    'input_types': [['exp','cna','gistic','fish','sbs','ig']],
    'input_types_subtask': [['clin']],
    'layer_dims': [[[32, 4],[16,4],[4,1],[4,1],[4,1],[4,1]]],
    'layer_dims_subtask' : [[4,1]],
    'kl_weight': [1],
    'activation': [LeakyReLU()],
    'subtask_activation': [Tanh()],
    'epochs': [100],
    'burn_in': [20],
    'patience': [5],
    'dropout': [0.3],
    'dropout_subtask': [0.3]
}
```

## Software
These dependencies will be automatically installed.
```
python >= 3.8
torch >= 1.9.0
scikit-learn >= 0.24.1
scikit-survival >= 0.17.1
importlib_resources
matplotlib
git+https://github.com/JiaGengChang/shap.git
```

The last dependency is a forked version of shap/shap which works for MyeVAE. Due to its multi-modal nature, MyeVAE takes a list of tensors as input rather than a single tensor. Hence, the original shap will not work.


## Recommended hardware

1. Minimum 4 CPU cores (8 cores is recommended)

2. Minimum 16 GB RAM (64GB is required for feature preprocessing)

No GPU is required.

Total CPU time for feature preprocessing: ~24 hours

Total CPU time for training: ~2 minutes per model (no GPU required)


# Citation

If you use MyeVAE in your research, please cite the authors:
```
[Manuscript under review. Contact author at changjiageng@u.nus.edu for citation.]
```