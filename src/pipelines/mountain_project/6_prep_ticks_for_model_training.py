import pandas as pd
from category_encoders import OrdinalEncoder
from ...models.base import get_conn
from ...models.tick import Tick
from ...models.route import Route
from ...helpers.tick_helper import ordinal_mapping

def main():
  '''
  fetch ticks from the db, remove unusable ticks, encode them, and save them to a csv for model training
  '''
  df = get_all_ticks()
  df = remove_unusalbe_data(df)
  df = consolidte_mixed_route_types(df)

  oe = OrdinalEncoder(mapping=ordinal_mapping(df))
  df_model_ready = oe.fit_transform(df)

  # save df_model_ready to csv using routeid as the index
  df_model_ready.set_index('route_id', inplace=True)
  df_model_ready.to_csv('/app/csv_files/mp_ticks_model_ready.csv')

def get_all_ticks():
  engine, Session = get_conn()
  with Session() as session:
    query = session.query(Tick.route_id, Tick.date, Tick.style, Tick.lead_style, Tick.attempts, Route.route_type, Route.alpine, Route.rating, Route.safety, Route.avg_stars, Route.pitches).join(Route, Tick.route_id == Route.route_id).statement
    return pd.read_sql(query, con=session.bind)


def consolidte_mixed_route_types(df):
  # Clean up mixed route types, and convert them to a single type (Sport, Trad)
  route_type_mapping = {'Sport, TR': 'Sport', 'Trad, TR': 'Trad', 'Trad, Sport': 'Trad'}
  df['route_type'] = df['route_type'].replace(route_type_mapping)

  return df

def remove_unusalbe_data(df):
  # remove obscure and uncommon route types
  remove_route_types = ["TR", "Trad, Aid", "Sport, Aid", "Sport, Aid, Boulder, Mixed", "Trad, Sport, TR", "Trad, TR, Boulder", "Trad, TR, Aid", "TR, Boulder", "TR, Boulder, Alpine", "Trad, Boulder"]
  df = df[~df['route_type'].isin(remove_route_types)]

  # only looking at Lead routes for now -  drop anything without a lead style, and drop boulders
  df = df[df['style'] == 'Lead']
  df = df.dropna(subset=['style', 'lead_style'])
  df = df.drop(columns=['style'])
  df = df[df['route_type'] != 'Boulder']

  return df

if __name__ == '__main__':
  main()