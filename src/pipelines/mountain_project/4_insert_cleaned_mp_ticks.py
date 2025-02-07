import pandas as pd
from pangres import upsert
from ...models.base import get_conn

def main():
    df = pd.read_csv("/app/csv_files/cleaned_mp_ticks.csv")
    engine, Session = get_conn()

    with Session() as session:
        upsert(engine, df, 'ticks', if_row_exists='update', add_new_columns=True)

if __name__ == '__main__':
    main()
