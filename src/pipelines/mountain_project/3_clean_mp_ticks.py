import pandas as pd

def main():
    '''
    starts with mp_ticks_raw.csv
    writes mp_ticks_cleaned.csv
    '''
    df_raw = pd.read_csv("/app/csv_files/mp_ticks_raw.csv")
    df = initial_data_cleaning(df_raw.copy())
    df = cleanup_multipitch_routes(df)
    df = group_by_route(df)
    df.to_csv('/app/csv_files/mp_ticks_cleaned.csv', index=False)

def initial_data_cleaning(df):
    df.columns = normalize_column_names(df)
    df['route_name'] = df['route']
    df['attempts'] = 1
    df['source'] = 'MP'

    df = process_generic_area_ticks(df)

    # Get RouteID from URL
    df['routeid'] = df['url'].apply(lambda x: x.split('/')[-2])

    return df    

def process_generic_area_ticks(df):
    '''
    I used chatgpt to extract the route names from the generic area notes, and put the new data into chatgpt_processed_generic_route_ticks.csv
    The CSV also has generated routeid values in the url that don't overlap with MP ids.
    TODO: automate the chatGPT processing? that would definitly be an interesting challenge.
    '''
    df_generic = pd.read_csv("/app/csv_files/generic_mp_ticks_processed.csv")
    df_generic.columns = normalize_column_names(df_generic)

    df_non_generic = df[~df['location'].str.contains('Generic Area')]
    df = pd.concat([df_non_generic, df_generic], ignore_index=True)

def cleanup_multipitch_routes(df):
    ''' This is messy logic here....
        a 2 pitch Onsight Row, means it is a 2pitch route, 1 attempt
        a 2 pitch Flash row means it is a 2 pitch route, 1 attempt
        a 2 pitch Redpoint row, means it was a 1 pitch route with 2 attempts, 1 Fell/Hung, and 1 Redpoint.
        a 2 pitch Fell/Hung row, means it was a 1 pitch route with 2 attempts, each a Fell/Hung
        if 'Route Type' == trad, in rmp & fmp, that mean means pitches remains uncahnged, and attempts = 1
        if 'Route Type' == sport, in rmp/fmp, set attempts = pitches, and pitches = 1.
    '''
    # mprfhs mean multi-pitch redpoint fell/hung sport
    mprfhs = df[(df['pitches'] > 1) & 
                    (df['lead_style'].isin(['Redpoint', 'Fell/Hung'])) & 
                    (df['route_type'] == 'Sport') &
                    (~df['route_name'].isin(['The Richness of It All', 'Lost in Space', 'Not One Of Us']))] # these are the 3 excepions to my logic...
    mprfhs.loc[:, 'attempts'] = mprfhs['pitches']
    mprfhs.loc[:, 'pitches'] = 1

    df.loc[mprfhs.index, 'attempts'] = mprfhs['attempts']
    df.loc[mprfhs.index, 'pitches'] = mprfhs['pitches']
    return df

def group_by_route(df):
    # Reorder columns and drop unnecessary columns
    df = df[['routeid', 'route_name', 'date', 'lead_style', 'attempts', 'source']]

    df = df.groupby('routeid').agg({'route_name': 'first', 'date': 'last', 'source': 'first',
                                    'lead_style': 'min',   'attempts': 'sum'}).reset_index()

    return df

if __name__ == '__main__':
    main()