import sys
import pandas as pd
import numpy as np
import os
import torch

from sklearn.model_selection import train_test_split

def load_data(config):
    embeddings_file = config['embeddings_file']
    demographics_file = config['demographics_normalized_file']

    cuisine_embeddings = pd.read_csv(embeddings_file)

    # the embedding is stored as a string, convert back to a numpy array 
    cuisine_embeddings['embedding'] = \
        cuisine_embeddings['embedding']\
            .apply(lambda x: np.fromstring(x, sep=','))

    demographics = pd.read_csv(demographics_file)
    # inner 'join' to make sure embedding cities match up to demographics

    join_on = []
    if (config['restaurant_data_source']=='Bing'):
        join_on = ['county']
    else :
        join_on = ['city', 'state']

    demographics = demographics.merge(cuisine_embeddings, left_on=join_on,\
        right_on=join_on, how='inner', suffixes=(False, False))
    
    cuisine_embeddings = pd.DataFrame(demographics['embedding'])
    demographics = demographics.drop(columns=['embedding'])

    print(demographics.head())
    print(cuisine_embeddings.head())

    return demographics, cuisine_embeddings

def prepare_data(county_cuisine_embeddings, county_demographics):
    X = np.stack(county_cuisine_embeddings['embedding'].values)
    Y = county_demographics[['county','white', 'black', 'asian',  'indigenous', 'pacific', 'hispanic', 'two_pop']].to_numpy()
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    train_cities = Y_train[:, :1]
    test_cities = Y_test[:, :1]

    print(type(train_cities))
    print(train_cities[:5])

    Y_train = Y_train[:, 1:]
    Y_test = Y_test[:, 1:]

    Y_train_numeric = Y_train.astype(float)  # Convert to float
    Y_test_numeric = Y_test.astype(float)

    #convert to tensors:
    X_train_tensor = torch.tensor(X_train, dtype=torch.float)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float)


    print(Y_train.shape)
    print(Y_train[:5])
    Y_train_tensor = torch.tensor(Y_train_numeric, dtype=torch.float)
    Y_test_tensor = torch.tensor(Y_test_numeric, dtype=torch.float)

    return X_train_tensor, X_test_tensor, Y_train_tensor, Y_test_tensor, train_cities, test_cities