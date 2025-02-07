import pandas as pd
from category_encoders import OrdinalEncoder
from ...models.base import get_conn
from ...models.tick import Tick
from ...helpers.tick_helper import ordinal_mapping

def main():
  '''
  fetch ticks from the db, remove unusable ticks, encode them, and save them to a csv for model training
  '''
  df = get_all_ticks()
  remove_unusalbe_data(df)
  something()
  something2()

  oe = OrdinalEncoder(mapping=ordinal_mapping(df))
  df_ordinal = oe.fit_transform(df)

  df_model_ready = df_ordinal.copy()
  
  # save df_model_ready to csv using routeid as the index
  df_model_ready.set_index('routeid', inplace=True)
  df_model_ready.to_csv('/app/csv_files/mp_ticks_model_ready.csv')

# TODO: need to join on route to get a few columns from the route table: grade..etc
# make this fetch only teh columns that the model needs:
# tick table: routeid, date, lead_style, attempts   
#route table columns: route_type, alpine, rating, safety, avg_stars, pitches
def get_all_ticks():
  engine, Session = get_conn()
  with Session() as session:
    tick_statment = session.query(Tick).statement
    return pd.read_sql(tick_statment, con=session.bind)


def something2():
    # Convert the Lead Style column to a categorical type with the specified order (Onsight, Flash, Redpoint, Fell/Hung)
    df['lead_style'] = pd.Categorical(df['lead_style'], categories=['Onsight', 'Flash', 'Redpoint', 'Fell/Hung'], ordered=True)

def something():
  # Organize Route Type entries this 
    route_type_mapping = {'Sport, TR': 'Sport', 'Trad, TR': 'Trad', 'Trad, Sport': 'Trad', 'TR, Boulder': 'Boulder'}
    df['route_type'] = df['route_type'].replace(route_type_mapping)


def remove_unusalbe_data(df):
  # remove obscure and uncommon route types
  remove_route_types = ["TR", "Trad, Aid", "Sport, Aid", "Sport, Aid, Boulder, Mixed", "Trad, Sport, TR", "Trad, TR, Boulder", "Trad, TR, Aid", "TR, Boulder, Alpine", "Trad, Boulder"]
  df = df[~df['route_type'].isin(remove_route_types)]

  # A bit dirty, but replace Topropes with Fell/Hung to better capture redpoint attempts, but this also skews routes that I TR'd once cleanly and never lead... :/
  # df.loc[df['Style'] == 'Toprope', 'Lead Style'] = 'Fell/Hung'
  # df.loc[df['Style'] == 'Toprope', 'Style'] = 'Lead'

  # only lookig at Lead routes for now, and drop anything without a lead style
  df = df[df['style'] == 'Lead']
  df = df.dropna(subset=['style', 'lead_style'])
  df = df.drop(columns=['style'])
  
  # drop boulders (may be redundant with the route type removal)
  df = df[df['route_type'] != 'Boulder']

  # set up a column for attempts
  return df
