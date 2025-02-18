import requests
import os

ob_api_url = os.getenv("OB_API_URL", "https://api.openbeta.io/")

def open_beta_request(query):
    response = requests.post(
        ob_api_url,
        json={'query': query},
        headers={'content-type': 'application/json'}
    )
    response.raise_for_status()
    return response

