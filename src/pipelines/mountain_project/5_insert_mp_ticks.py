import pandas as pd
from pangres import upsert
from ...models.base import get_conn

def main():
    df = pd.read_csv("/app/csv_files/mp_ticks_cleaned.csv")
    df = df.set_index('route_id')
    df.index.name = 'route_id'
    engine, Session = get_conn()

    with Session() as session:
        upsert(engine, df, 'ticks', if_row_exists='update', add_new_columns=True)

if __name__ == '__main__':
    main()
