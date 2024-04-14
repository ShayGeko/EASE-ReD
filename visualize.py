import sys
import yaml
import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from  matplotlib.colors import LinearSegmentedColormap
import os

from geopy.geocoders import Nominatim
from tqdm import tqdm
from torch import nn
import geopandas as gpd
from shapely.geometry import Point
from geodatasets import get_path

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
        print('MSE:')
        print(nn.MSELoss()(torch.tensor(predictions[i]), torch.tensor(actuals[i])).item())
        ax.legend()

    # Adjust or remove empty subplots if cities < nrows*ncols
    for i in range(len(cities), nrows*ncols):
        axs.flat[i].set_visible(False)

    # Save the entire figure containing all subplots
    plt.subplots_adjust(wspace=0.4, hspace=0.6)
    # plt.show()
    plt.savefig(f'{dir}/predictions.png')

def get_MSE(actuals, predictions, cities, dir, config):
    labels = ['white_pop', 'black_pop', 'asian_pop', 'indigenous', 'pacific_pop', 'hisp_pop', 'two_pop']
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    # Assuming we have 15 cities and want a 3x5 grid of subplots
    nrows = 3
    ncols = 5
    fig, axs = plt.subplots(nrows, ncols, figsize=(15, 10))  # Adjust figsize as needed
    fig.tight_layout(pad=3.0)
    counties = []
    MSEs = []
    pred = []
    act = []
    for i, city in enumerate(cities):
        counties.append(city[0])
        pred.append(predictions[i])
        act.append(actuals[i])
        if config['loss']=='CrossEntropy':
            # print('predictions before softmax:')
            # print(predictions)
            predictions[i] = nn.functional.softmax(torch.tensor(predictions[i]), dim=0).numpy()
            # print('predictions after softmax:')
            # print(predictions)
        MSE = nn.MSELoss()(torch.tensor(predictions[i]), torch.tensor(actuals[i])).item()
        MSEs.append(MSE)
    errors = pd.DataFrame({'county': counties,
                           'MSE': MSEs,
                           'predictions': pred,
                           'actuals': act})
    errors = errors.sort_values(['MSE'], ascending=False)
    errors = errors.reset_index(drop = True)
    errors_top15 = errors[0:15]
    for i in range(15):
        ax = axs[i // ncols, i % ncols]
        ax.set_ylabel('Population Percentage')
        ax.set_title(f"{errors_top15['county'][i]}")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.bar(x - width/2, errors_top15['actuals'][i], width, label='Actual')
        ax.bar(x + width/2, errors_top15['predictions'][i], width, label='Predicted')
        ax.set_ylim(0, 1)
        ax.legend()
    print(errors_top15[['county', 'MSE']])

    # Adjust or remove empty subplots if cities < nrows*ncols
    for i in range(len(cities), nrows*ncols):
        axs.flat[i].set_visible(False)

    # Save the entire figure containing all subplots
    plt.subplots_adjust(wspace=0.4, hspace=0.6)
    # plt.show()
    plt.savefig(f'{dir}/predictions_most_inaccurate.png')

    return errors

def get_lon_lat(errors):
    errors = errors[['county', 'MSE']]
    coordinates = []

    def get_coordinates(location_name):
        geolocator = Nominatim(user_agent="my_geocoder")
        try:
            location = geolocator.geocode(location_name + ", United States")
            print(location_name,"->",location)
            print(location.longitude, location.latitude)
            return location.longitude, location.latitude
        except:
            print(location_name + '-> not found')
            return 0,0
        
    for county in tqdm(errors['county']):
        coordinates.append(get_coordinates(county))
    coordinates = pd.DataFrame(coordinates)
    coordinates['county'] = errors['county']
    coordinates.to_csv('coordinates.csv')

def map_MSE(errors, dir):
    def marker_colour(num):
        if num > 0.08:
            return 'red'
        elif num > 0.05:
            return 'purple'
        elif num > 0.03:
            return 'blue'
        else:
            return 'green'
    errors = errors[['county', 'MSE']]
    errors['colour'] = errors['MSE'].apply(lambda x: marker_colour(x))
    coordinates = pd.read_csv('coordinates.csv', names = ['drop', 'longitude', 'latitude', 'county'])
    coordinates = coordinates.drop(columns = ['drop']).iloc[1:]
    errors = errors.merge(coordinates)
    errors = errors[(errors['longitude'] >= -180) & 
                    (errors['longitude'] <= -66) &
                    (errors['latitude'] >= 18) &
                    (errors['latitude'] <= 72)].reset_index(drop = True)
    # print(errors)

    errors_map = gpd.GeoDataFrame(
        errors, geometry=gpd.points_from_xy(errors.longitude, errors.latitude))
    print(errors_map)

    world = gpd.read_file(get_path("naturalearth.land"))

    fig= plt.figure()
    # We restrict to United States.
    usa = world.clip([-189, 18, -66, 72]).plot(color="white", edgecolor="black")

    # We can now plot our ``GeoDataFrame``.
    errors_map.plot(ax=usa, color=errors_map['colour'], markersize = 1)

    red_patch = mpatches.Patch(color='red', label='very high MSE')
    purple_patch = mpatches.Patch(color='purple', label='high MSE')
    blue_patch = mpatches.Patch(color='blue', label='medium MSE')
    green_patch = mpatches.Patch(color='green', label='low MSE')

    plt.legend(handles=[red_patch, purple_patch, blue_patch, green_patch])
    plt.savefig(f'{dir}/MSE_map.png')

def main(config):
    model = torch.load(f'./experiments/{config["name"]}/models/model-6000.pth')

    city_demographics, city_cuisine_embeddings = \
        load_data(config)

    X_train, X_test, y_train, y_test, train_cities, test_cities = \
        prepare_data(city_cuisine_embeddings, city_demographics)

    model.eval()
    predictions = model(X_test)
    predictions_all = model(torch.cat((X_train,X_test)))
    # if(config['loss'] == 'BCEWithLogits'):
    #     predictions = nn.functional.softmax(predictions, dim=1)
    # print(predictions.shape)
    # print(predictions_all.shape)

    results = predictions.detach().numpy()
    results_all = predictions_all.detach().numpy()
    actuals = y_test.detach().numpy()
    actuals_all = torch.cat((y_train,y_test)).detach().numpy()
    cities = test_cities
    cities_all = np.concatenate((train_cities, cities))
    # print(np.shape(cities_all))

    # visualize the results
    dir = f'./experiments/{config["name"]}/visuals'
    dir_MSE = f'./experiments/{config["name"]}/visuals/sorted_MSE'
    if not os.path.exists(dir):
        os.makedirs(dir)
    if not os.path.exists(dir_MSE):
        os.makedirs(dir_MSE)

    store_visuals(actuals, results, cities, dir)
    MSEs = get_MSE(actuals_all, results_all, cities_all, dir_MSE, config)
    # get_lon_lat(MSEs) #only run this once - will take 30 min and store a csv file of the coordinates
    map_MSE(MSEs, dir_MSE)


if __name__ == "__main__":
    yml_config_file = sys.argv[1]
    # print(yml_config_file)

    config = yaml.safe_load(open(yml_config_file))

    main(config)
