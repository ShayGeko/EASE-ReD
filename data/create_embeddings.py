import os
import sys
import pandas as pd
import numpy as np
import torch
import csv
from tqdm import tqdm

from sentence_transformers import SentenceTransformer

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def is_file_empty(file_path):
    """Return True if file is empty or doesn't exist, False otherwise."""
    return not os.path.exists(file_path) or os.path.getsize(file_path) == 0



def append_to_csv_osm(output, embedding, city_name, state_name):
    # append to csv
    with open(output, 'a', newline='') as csvfile:
        # Define your CSV writer
        writer = csv.writer(csvfile)
        
        # If the file does not exist, write the header first
        if is_file_empty(output):
            # Write a header row, starting with 'city_name' and then dynamic column names for the array elements
            headers = ['city', 'state', 'embedding']
            writer.writerow(headers)
        
        array_as_string = np.array2string(embedding, separator=',', max_line_width=np.inf)[1:-1]
        # Write the row consisting of the city name and the array elements
        writer.writerow([city_name, state_name, array_as_string])



def generate_embeddings_from_bing_maps(model, input = "./bingMaps/counties/", output = "./embeddings/bing_embeddings.csv"):
    """
    Expects a list of .csv files in input directory
    Each file should be in format f"<city>-<state>.csv"
    Currently assumes that files are coming from Bing Maps and is parcing them
    """
    files = os.listdir(input)

    if(os.path.exists(output)):
        os.remove(output)

    all_embeddings = []
    counties = []
    for file in tqdm(files):
        if file.endswith(".csv"):
            df = pd.read_csv(input + file)

            df['Categories'] = df['Categories'].str.replace("[\[\]'']", '', regex=True)
            
            county_name = file[:-4]

            embeddings = model.encode(df['Categories'])

            if(embeddings.size == 0):
                continue

            
            counties.append(county_name)
            avg_embedding = np.mean(embeddings, axis=0)

            all_embeddings.append(avg_embedding)

            with open(output, 'a', newline='') as csvfile:
                # Define your CSV writer
                writer = csv.writer(csvfile)
                
                # If the file does not exist, write the header first
                if is_file_empty(output):
                    # Write a header row, starting with 'city_name' and then dynamic column names for the array elements
                    headers = ['county', 'embedding']
                    writer.writerow(headers)
                
                array_as_string = np.array2string(avg_embedding, separator=',', max_line_width=np.inf)[1:-1]
                # Write the row consisting of the city name and the array elements
                writer.writerow([county_name, array_as_string])
            
    all_embeddings_df = np.array(all_embeddings)

    pca = PCA(n_components = 50)
    pca_embeddings = pca.fit_transform(all_embeddings_df)
    
    pca_embeddings = [np.array2string(embedding, separator=',', max_line_width=np.inf)[1:-1]  for embedding in pca_embeddings]
    
    pca_embeddings = pd.DataFrame({'county' : counties,'embedding':pca_embeddings})
    pca_output = "./embeddings/pca_bing_embeddings.csv"
    pca_embeddings.to_csv(pca_output, index=False)

def generate_embeddings_from_osm(model, input="./osm/data/", output="./predictions_input/embeddings.csv"):
    """
    Expects a list of .json.gz files in input directory
    Each file should be in format f"<datasource>-<city>-<state>-<whatever>.json.gz"
    Currently assumes that files are coming from OSM and is parcing them
    """
    # should be a spark thingy probs
    files = os.listdir(input)
    cities = []

    pca_output = "./predictions_input/pca_embeddings.csv"

    all_embeddings = []
    for file in tqdm(files):
        if file.endswith(".json.gz"):
            df = pd.read_json(input + file, compression='gzip')

            # osm data is returned inside the "nodes" key
            if(file.startswith("osm")):
                nodes = df["nodes"] 
                df = pd.json_normalize(nodes)

            if(df.empty):
                print(f"{file} is empty. Skipping.")
                continue

            # this is osm specific but it's fine
            df.columns = df.columns.str.replace('tags.', '', regex=False)

            city_name = file.split("-")[1].title()
            state_name = file.split("-")[2].title()
            if(df.size > 0 and df.columns.__contains__("cuisine")):
                cities.append(city_name)
                cuisines = df['cuisine']
                df = cuisines.value_counts().reset_index(name='counts')
                cuisines = df['cuisine']
                counts = df['counts'].to_numpy()

                # get embeddings for each cuisine
                embeddings = model.encode(cuisines)

                # compute the weigted average of the embedding
                counts = counts.reshape(counts.shape[0], 1)
                embedding = np.sum(embeddings * counts, axis=0) / np.sum(counts)
                append_to_csv_osm(output, embedding, city_name, state_name)

    embeddings = pd.read_csv(output)
    pca_embeddings = PCA(n_components = 20).fit_transform(embeddings['embedding'].apply(lambda x: np.fromstring(x, sep=',')).to_list())
    pca_embeddings = pd.DataFrame(pca_embeddings)
    print(pca_embeddings.shape)
    pca_embeddings.to_csv(pca_output, index=False)


def main():
    print("Loading the embedding model. This might take a bit...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Model loaded. Generating embeddings.")
    # generate_embeddings_from_osm(model)
    generate_embeddings_from_bing_maps(model)

if __name__ == "__main__":
    main()