from ...models.base import get_conn
import requests
import pandas as pd

def main(api_url, username):
    query = user_tick_query(username)
    ticks_response = fetch_ob_ticks(api_url, query)
    write_raw_ob_ticks_to_csv(ticks_response)

def write_raw_ob_ticks_to_csv(response):
    data = response.json()['data']['userTicks']
    df = pd.DataFrame(data)
    df.to_csv('/app/csv_files/ticks_raw_ob.csv', index=False)

if __name__ == '__main__':
    main(ob_api_url, username)
