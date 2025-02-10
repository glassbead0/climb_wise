import requests

# TODO: should this be an env variable? separate base url + username
tick_url = "https://www.mountainproject.com/user/107708526/aaron-glasenapp/tick-export"

# fetch data from MP, save a raw csv.
def main(tick_url):
    '''
    MountainProject used to have an API to get tick data, but they shut it down. 
    But download urls are not authenticated so, just use download url you want.
    TODO: build an OB pipeline to eventually replace MP
    '''
    response = requests.get(tick_url)
    response.raise_for_status()
    with open('/app/csv_files/mp_ticks_raw.csv', 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    main(tick_url)