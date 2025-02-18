import pandas as pd
from pangres import upsert
from ...models.base import get_conn
from ...helpers.tick_helper import normalize_column_names, extract_route_id_from_url

def main():
    '''
    Insert generic routes into the route table, so they can be used as foreign keys.
    '''
    df = pd.read_csv("/app/csv_files/generic_mp_ticks_processed.csv")
    df = normalize_column_names(df)
    df = extract_route_id_from_url(df)
    df = df[['route_id', 'route_name', 'url', 'location', 'pitches', 'avg_stars', 'route_type', 'length', 'rating']]
    df['url'] = 'Generic'
    df = df.set_index('route_id')
    df.index.name = 'route_id'
    duplicates = df.index[df.index.duplicated(keep=False)]
    print(duplicates)
    
    engine, Session = get_conn()
    with Session() as session:
      upsert(engine, df, 'routes', if_row_exists='update')
  
if __name__ == '__main__':
    main()