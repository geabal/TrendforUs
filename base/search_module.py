from django.conf import settings
import requests

SEARCH_API_URL = settings.SEARCH_API_URL

def get_search_result(user_query:str=''):
    try:
        response = requests.get(SEARCH_API_URL, params={'q':user_query}, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise e


