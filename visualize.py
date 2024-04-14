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
from scipy.stats import normaltest, f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd
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

def get_MAE(actuals, predictions, cities, dir, config):

    counties = []
    MAEs = []
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
        MAE = np.mean(np.abs(predictions[i] - actuals[i]))
        MAEs.append(MAE)
    errors = pd.DataFrame({'county': counties,
                           'MAE': MAEs,
                           'predictions': pred,
                           'actuals': act})
    errors = errors.sort_values(['MAE'], ascending=False)
    errors = errors.reset_index(drop = True)

    return errors

def plot_MAE(errors, dir, filename):
    labels = ['white_pop', 'black_pop', 'asian_pop', 'indigenous', 'pacific_pop', 'hisp_pop', 'two_pop']
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    # Assuming we have 15 cities and want a 3x5 grid of subplots
    nrows = 3
    ncols = 5
    fig, axs = plt.subplots(nrows, ncols, figsize=(15, 10))  # Adjust figsize as needed
    fig.tight_layout(pad=3.0)
    for i in range(15):
        ax = axs[i // ncols, i % ncols]
        ax.set_ylabel('Population Percentage')
        ax.set_title(f"{errors['county'][i]}")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.bar(x - width/2, errors['actuals'][i], width, label='Actual')
        ax.bar(x + width/2, errors['predictions'][i], width, label='Predicted')
        ax.set_ylim(0, 1)
        ax.legend()

    # Save the entire figure containing all subplots
    plt.subplots_adjust(wspace=0.4, hspace=0.6)
    # plt.show()
    plt.savefig(f'{dir}/{filename}')

def one_model_tests(data):
    normal_p = normaltest(data).pvalue
    if normal_p < 0.05:
        print('data is not normal! p-value is ' + str(normal_p))
    else:
        print('data is normal! p-value is ' + str(normal_p))

def tukey_test(data):
    data = data.dropna()
    x_melt = pd.melt(data)
    print(x_melt)
    posthoc = pairwise_tukeyhsd(
        x_melt['value'], x_melt['variable'],
        alpha=0.05)
    print(posthoc)
    fig = posthoc.plot_simultaneous()
    plt.savefig('tukey.png')


def get_lon_lat(errors):
    errors = errors[['county', 'MAE']]
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

def map_MAE(errors, dir):
    def marker_colour(num):
        if num > 0.1:
            return 'red'
        else:
            return 'green'
    errors = errors[['county', 'MAE']]
    errors['colour'] = errors['MAE'].apply(lambda x: marker_colour(x))
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

    red_patch = mpatches.Patch(color='red', label='MAE greater than 10%')
    green_patch = mpatches.Patch(color='green', label='MAE less than 10%')

    plt.legend(handles=[red_patch, green_patch])
    plt.savefig(f'{dir}/MAE_map.png')

def main(config):
    model = torch.load(f'./experiments/{config["name"]}/models/model-3000.pth') #change here for different nn models

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
    dir_MAE = f'./experiments/{config["name"]}/visuals/sorted_MAE'
    if not os.path.exists(dir):
        os.makedirs(dir)
    if not os.path.exists(dir_MAE):
        os.makedirs(dir_MAE)

    # store_visuals(actuals, results, cities, dir)
    MAEs = get_MAE(actuals_all, results_all, cities_all, dir_MAE, config)
    # MAEs_best15 = MAEs[-15:].reset_index(drop = True)
    # MAEs_worst15 = MAEs[:15]
    # plot_MAE(MAEs_best15, dir_MAE, 'predictions_most_accurate.png')
    # plot_MAE(MAEs_worst15, dir_MAE, 'predictions_most_inaccurate.png')
    plt.clf()
    plt.hist(MAEs['MAE'], bins = 20)
    plt.title('Histogram of mean absolute error')
    plt.savefig(f'{dir_MAE}/histogram.png')
    plt.clf()

    one_model_tests(MAEs['MAE'])
    # get_lon_lat(MSEs) #only run this once - will take 30 min and store a csv file of the coordinates
    map_MAE(MAEs, dir_MAE)

    # MAEs['MAE'].to_csv(f"MAE_data/{config['name']}.csv", index = False) #makes the csvs

    MAE_category = pd.read_csv('MAE_data/category-embedding-2.csv')
    MAE_ce_category = pd.read_csv('MAE_data/ce-category-embedding-1.csv')
    MAE_pca_category = pd.read_csv('MAE_data/pca-category-embedding-2.csv')
    MAE_ce_pca_category = pd.read_csv('MAE_data/ce-pca-category-embedding-1.csv')
    MAE_name = pd.read_csv('MAE_data/name-embedding-3.csv')
    MAE_ce_name = pd.read_csv('MAE_data/ce-name-embedding-1.csv')
    MAE_pca_name = pd.read_csv('MAE_data/pca-name-embedding-2.csv')
    MAE_ce_pca_name = pd.read_csv('MAE_data/ce-pca-name-embedding-1.csv')

    MAE_all_models = pd.concat([MAE_category, MAE_ce_category, MAE_pca_category, MAE_ce_pca_category,
                                MAE_name, MAE_ce_name, MAE_pca_name, MAE_ce_pca_name], axis = 1)
    MAE_all_models = MAE_all_models.set_axis(['category', 'ce_category', 'pca_category', 'ce_pca_category', 
                                              'name', 'ce_name', 'pca_name', 'ce_pca_name'], axis=1)
    tukey_test(MAE_all_models)

if __name__ == "__main__":
    yml_config_file = sys.argv[1]
    # print(yml_config_file)

    config = yaml.safe_load(open(yml_config_file))

    main(config)
