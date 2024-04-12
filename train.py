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

def store_visuals(actuals, predictions, cities, file):
    labels = ['white', 'black', 'asian', 'native', 'pacific', 'hispanic', 'mixed']
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    # Assuming we have 15 cities and want a 3x5 grid of subplots
    nrows = 3
    ncols = 5
    fig, axs = plt.subplots(nrows, ncols, figsize=(15, 10))  # Adjust figsize as needed
    fig.tight_layout(pad=3.0)

    for i, city in enumerate(cities):
        if(i >= nrows * ncols):
            break
        ax = axs[i // ncols, i % ncols]
        ax.set_ylabel('Population Percentage')
        ax.set_title(f'{city[0]}')
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.bar(x - width/2, actuals[i], width, label='Actual')
        ax.bar(x + width/2, predictions[i], width, label='Predicted')
        ax.set_ylim(0, 1)
        
        print(f'City: {city}')
        print("actuals:")
        print(actuals[i])
        print("predictions:")
        print(predictions[i])
        ax.legend()

    # Adjust or remove empty subplots if cities < nrows*ncols
    for i in range(len(cities), nrows*ncols):
        axs.flat[i].set_visible(False)

    # Save the entire figure containing all subplots
    plt.subplots_adjust(wspace=0.4, hspace=0.6)
    # plt.show()
    plt.savefig(f'{file}')
    plt.close()


def train_model(X_train, X_test, y_train, y_test, test_counties, config):
    hidden_layer_size = int(config['hidden_layer_size'])
    layers = [hidden_layer_size,hidden_layer_size,hidden_layer_size]
    model = MLPRegressor(input_size=X_train.shape[1], hidden_size=layers)

    # classification loss
    # loss weights because white is a majority class:
    criterion = None
    if config['loss'] == 'MSE':
        criterion = nn.MSELoss()
    elif config['loss'] == 'BCEWithLogits':
        weights = torch.tensor([1, 5, 5, 5, 5, 5, 5])
        criterion = nn.BCEWithLogitsLoss(pos_weight=weights)
        # y_train = nn.functional.softmax(y_train, dim=1)
    else:
        print("Invalid loss function")
        sys.exit(1)
    lr = float(config['lr'])
    weight_decay = float(config['weight_decay'])
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    
    name = config['name']
    
    train_losses = []
    val_losses = []

    num_epochs = int(config['num_epochs'])
    for epoch in tqdm(range(num_epochs)):  # Number of epochs
        model.train()
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train) # + torch.relu(-outputs).mean()

        if epoch % 25 == 0:
            with torch.no_grad():
                val_outputs = model(X_test)
                val_loss = criterion(val_outputs, y_test)
                val_losses.append(val_loss.item())
            print(f'Epoch {epoch}, train loss: {loss.item()}, validation loss: {val_losses[-1]}')
            train_losses.append(loss.item())


        if epoch % 100 == 0:
            plt.figure()
            x_ticks = np.arange(0, len(train_losses)) * 25
            plt.plot(x_ticks, train_losses, label='train')
            plt.plot(x_ticks, val_losses, label='val')
            plt.legend()
            plt.xlabel('Epoch')
            plt.ylabel('Loss')
            plt.savefig(f'./experiments/{name}/loss.png')
            plt.close()

        if epoch > 0 and epoch % 1000 == 0:
            store_dir = f'./experiments/{name}/models'
            if not os.path.exists(store_dir):
                os.makedirs(store_dir)
            torch.save(model, f'./experiments/{name}/models/model-{epoch}.pth')
            
            model.eval()
            predictions = model(X_test)
            # if(config['loss'] == 'BCEWithLogits'):
            #     predictions = nn.functional.softmax(predictions, dim=1)
            print(predictions.shape)

            results = predictions.detach().numpy()
            actuals = y_test.detach().numpy()
            counties = test_counties

            # visualize the results
            dir = f'./experiments/{config["name"]}/visuals'
            file = f'./experiments/{config["name"]}/visuals/predictions-{epoch}.png'
            if not os.path.exists(dir):
                os.makedirs(dir)

            store_visuals(actuals, results, counties, file)
            
        loss.backward()
        optimizer.step()

    print("Done training!")

    return model

def main(config):
    county_demographics, county_cuisine_embeddings = \
        load_data(config)
    
    X_train, X_test, y_train, y_test, train_counties, test_counties = \
        prepare_data(county_cuisine_embeddings, county_demographics)
    

    print(train_counties[:5])
    print(train_counties.shape)
    name = config['name']
    folder = f'./experiments/{name}'
    if not os.path.exists(folder):
        os.makedirs(folder)
    np.save(os.path.join(folder, 'train_counties.npy'), train_counties, allow_pickle=True)
    np.save(os.path.join(folder, 'test_counties.npy'), test_counties, allow_pickle=True)

    # train model
    model = train_model(X_train, X_test, y_train, y_test, test_counties, config)
    
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