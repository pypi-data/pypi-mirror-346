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