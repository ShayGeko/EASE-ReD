import torch
import torch.nn as nn


class MLPRegressor(nn.Module):
    # by default sentence embedding is a vector in 384 dimensions
    def __init__(self, input_size=384, hidden_size=[500, 500, 500], output_size=7):
        super(MLPRegressor, self).__init__()
        
        layers = []

        # Add the input layer
        layers.append(nn.Linear(input_size, hidden_size[0]))
        layers.append(nn.ReLU())

        # hidden layers
        for i in range(len(hidden_size) - 1):
            layer = nn.Linear(hidden_size[i], hidden_size[i+1])
            # Initialize the weights with xavier normal
            nn.init.xavier_normal_(layer.weight)
            layers.append(layer)
            layers.append(nn.ReLU())

        # Add the output layer
        layers.append(nn.Linear(hidden_size[-1], output_size))
        self.layers = nn.Sequential(*layers)


    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x