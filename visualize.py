import sys
import yaml
import torch
import numpy as np
import matplotlib.pyplot as plt
import os

from torch import nn

from data import load_data, prepare_data


def store_visuals(actuals, predictions, cities, dir):
    labels = ['white_pop', 'black_pop', 'asian_pop', 'indigenous', 'pacific_pop', 'hisp_pop', 'two_pop']
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
        ax.set_title(f'{city}')
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
    plt.savefig(f'{dir}/predictions.png')

def main(config):
    model = torch.load(f'./experiments/{config["name"]}/models/model-1000.pth')

    city_demographics, city_cuisine_embeddings = \
        load_data(config)
    
    X_train, X_test, y_train, y_test, train_cities, test_cities = \
        prepare_data(city_cuisine_embeddings, city_demographics)
    
    
    model.eval()
    predictions = model(X_test)
    # if(config['loss'] == 'BCEWithLogits'):
    #     predictions = nn.functional.softmax(predictions, dim=1)
    print(predictions.shape)

    results = predictions.detach().numpy()
    actuals = y_test.detach().numpy()
    cities = test_cities

    # visualize the results
    dir = f'./experiments/{config["name"]}/visuals'
    if not os.path.exists(dir):
        os.makedirs(dir)

    store_visuals(actuals, results, cities, dir)




if __name__ == "__main__":
    yml_config_file = sys.argv[1]
    print(yml_config_file)

    config = yaml.safe_load(open(yml_config_file))

    main(config)