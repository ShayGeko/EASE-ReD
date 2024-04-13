from dask.distributed import Client
import dask.dataframe as dd
import pandas as pd

def calculate_fractions(group):
    total_population = group['TOT_POP'].sum()
    return pd.Series({
        'White': (group['NHWA_MALE'].sum() + group['NHWA_FEMALE'].sum()) / total_population,
        'Black': (group['BA_MALE'].sum() + group['BA_FEMALE'].sum()) / total_population,
        'Asian': (group['AA_MALE'].sum() + group['AA_FEMALE'].sum()) / total_population,
        'Indigenous': (group['IA_MALE'].sum() + group['IA_FEMALE'].sum()) / total_population,
        'Pacific': (group['NA_MALE'].sum() + group['NA_FEMALE'].sum()) / total_population,
        'Hispanic': (group['H_MALE'].sum() + group['H_FEMALE'].sum()) / total_population,
        'Two_Pop': (group['TOM_MALE'].sum() + group['TOM_FEMALE'].sum()) / total_population,
    })

def main():
    client = Client(n_workers=4, threads_per_worker=1, memory_limit='2GB')
    print("Dask Dashboard is available at:", client.dashboard_link)

    data = dd.read_csv('cc-est2019-alldata.csv', encoding='latin-1', assume_missing=True, blocksize=25e6)
    data_2019 = data[data['YEAR'] == 12]
    grouped_data = data_2019.groupby(['STNAME', 'CTYNAME'])

    meta = {
        'White': 'float64',
        'Black': 'float64',
        'Asian': 'float64',
        'Indigenous': 'float64',
        'Pacific': 'float64',
        'Hispanic': 'float64',
        'Two_Pop': 'float64'
    }

    county_fractions = grouped_data.apply(calculate_fractions, meta=meta).compute()
    county_fractions.reset_index(inplace=True)

    county_fractions.columns = [col.lower() for col in county_fractions.columns]
    county_fractions['county'] = (county_fractions['ctyname'] + " " + county_fractions['stname']).str.replace(" County", "", regex=True)
    county_fractions = county_fractions[['county', 'white', 'black', 'asian', 'indigenous', 'pacific', 'hispanic', 'two_pop']]
    county_fractions = county_fractions.sort_values('county')

    print(county_fractions.head())
    county_fractions.to_csv('county_ethnicity_fractions_2019.csv', index=False)

if __name__ == '__main__':
    main()
