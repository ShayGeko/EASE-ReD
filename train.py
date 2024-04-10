import sys
import pandas as pd
import numpy as np
import os
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import yaml
import shutil

from model import MLPRegressor
from data import load_data, prepare_data
from tqdm import tqdm

def train_model(X_train_tensor, X_test_tensor, Y_train_tensor, Y_test_tensor):
    model = MLPRegressor(input_size=X_train_tensor.shape[1])

    # classification loss
    # loss weights because white is a majority class:
    criterion = None
    if config['loss'] == 'MSE':
        criterion = nn.MSELoss()
    elif config['loss'] == 'BCEWithLogits':
        weights = torch.tensor([1, 1, 1, 1, 1, 1, 1])
        criterion = nn.BCEWithLogitsLoss(pos_weight=weights)
        Y_train_tensor = nn.functional.softmax(Y_train_tensor, dim=1)
    else:
        print("Invalid loss function")
        sys.exit(1)
    lr = float(config['lr'])
    weight_decay = float(config['weight_decay'])
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    
    name = config['name']
    
    train_losses = []
    val_losses = []
    for epoch in tqdm(range(20000)):  # Number of epochs
        optimizer.zero_grad()
        outputs = model(X_train_tensor)
        loss = criterion(outputs, Y_train_tensor) + torch.relu(-outputs).mean()

        if epoch % 100 == 0:
            print(f'Epoch {epoch}, Loss: {loss.item()}')
            with torch.no_grad():
                val_outputs = model(X_test_tensor)
                val_loss = criterion(val_outputs, Y_test_tensor)
                val_losses.append(val_loss.item())
            train_losses.append(loss.item())


        if epoch % 1000 == 0:
            plt.figure()
            plt.plot(train_losses, label='train')
            plt.plot(val_losses, label='val')
            plt.legend()
            plt.savefig(f'experiments/{name}/loss.png')

        if epoch > 0 and epoch % 1000 == 0:
            store_dir = f'./experiments/{name}/models'
            if not os.path.exists(store_dir):
                os.makedirs(store_dir)
            torch.save(model, f'./experiments/{name}/models/model-{epoch}.pth')
            
        loss.backward()
        optimizer.step()

    print("Done training!")

    return model

def main(config):
    city_demographics, city_cuisine_embeddings = \
        load_data(config)
    
    X_train, X_test, y_train, y_test, train_cities, test_cities = \
        prepare_data(city_cuisine_embeddings, city_demographics)
    

    print(train_cities[:5])
    print(train_cities.shape)
    name = config['name']
    folder = f'./experiments/{name}'
    if not os.path.exists(folder):
        os.makedirs(folder)
    np.save(os.path.join(folder, 'train_cities.npy'), train_cities, allow_pickle=True)
    np.save(os.path.join(folder, 'test_cities.npy'), test_cities, allow_pickle=True)

    # train model
    model = train_model(X_train, X_test, y_train, y_test)
    
    # save model
    torch.save(model, f'./experiments/{name}/models/final.pth')


if __name__ == "__main__":
    yml_config_file = sys.argv[1]
    print(yml_config_file)

    config = yaml.safe_load(open(yml_config_file))
    
    name = config['name']
    experiment_dir = f'./experiments/{name}'
    if not os.path.exists(experiment_dir):
        os.makedirs(experiment_dir)

    shutil.copy(yml_config_file, f'{experiment_dir}/config.yml')

    main(config)