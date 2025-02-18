import pandas as pd
from pangres import upsert
from ...helpers.tick_helper import normalize_column_names, extract_route_id_from_url
from ...models.base import get_conn

# Currently it's required to manually get this csv file from https://www.kaggle.com/datasets/pdegner/mountain-project-rotues-and-forums?select=mp_routes.csv
# before runing this script
# TODO: separarte cleaning and inserting into two scripts

csv_path = '/app/csv_files/mp_routes_raw.csv'

def main(csv_path):
  df = clean_raw_mp_data(csv_path)
  insert_routes_in_batches(df)

def clean_raw_mp_data(raw_csv_path):
    '''
    Read raw data from csv, add a route_id column, handle unnamed routes and other data cleaning.
    This requires the csv file to be in the correct location. TODO: use a Kaggle URL to fetch the data, or better yet switch to OpenBeta.
    '''
    df = pd.read_csv(raw_csv_path).drop(columns=['Unnamed: 0'])
    df = normalize_column_names(df)
    df = extract_route_id_from_url(df)
    df = extract_alpine(df)
    df = extract_safety_rating(df)
    df = handle_unnamed_routes(df)
    df = df.set_index('route_id')
    df.index.name = 'route_id'

    return df

def extract_alpine(df):
    '''separate out 'Alpine' from the 'Style' column'''
    df['alpine'] = df['route_type'].str.contains(r'Alpine').astype(int)
    df['alpine'] = df['alpine'].fillna(0).astype(bool)
    df['route_type'] = df['route_type'].str.replace(r', Alpine', '', regex=True)
    return df

def extract_safety_rating(df):
    '''separate safety rating from main rating (PG13, R, X)'''
    df['safety'] = df['rating'].str.extract(r'(PG13|R|X)', expand=False)
    df['safety'] = df['safety'].fillna('G')
    df['rating'] = df['rating'].str.replace(r' (PG13|R|X)', '', regex=True)
    df['safety'] = df['safety'].fillna('G')
    return df

def handle_unnamed_routes(df):
    '''
    Some routes are unnamed, which means the extracted routid will be 0 from the tick_helper.
    Correctly set the route_id using the last element of the url.
    Set the name to "Unknown".
    '''
    unnamed_routes = df[df['route_id']==0]
    unnamed_routes = extract_route_id_from_url(unnamed_routes, -1)
    unnamed_routes['route_name'] = "Unknown"
    df.update(unnamed_routes)

    return df

def insert_routes_in_batches(df, batch_size=5000):
  engine, Session = get_conn()

  with Session() as session:
    for i in range(0, len(df), batch_size):
      chunk = df.iloc[i:i + batch_size]
      upsert(engine, chunk, 'routes', if_row_exists='update')

if __name__ == '__main__':
    main(csv_path)
