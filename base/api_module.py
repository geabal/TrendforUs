from django.conf import settings
import requests
from django.core.cache import cache

SEARCH_API_URL = settings.SEARCH_API_URL
TREND_API_URL = settings.TREND_API_URL
TREND_TTL = settings.CACHE_TTL["TREND"]
SEARCH_TTL = settings.CACHE_TTL["SEARCH"]

def get_search_result(user_query:str='', cache_key:str='', ttl=SEARCH_TTL):
    result = cache.get(cache_key)
    if not result:
        result = get_search_from_api(user_query)
        cache.set(cache_key, result, ttl)
    return result

def get_search_from_api(user_query=''):
    try:
        response = requests.get(SEARCH_API_URL, params={'q':user_query}, timeout=5)
        response.raise_for_status()
        results = response.json()
        return results
    except requests.exceptions.RequestException as e:
        raise e


def get_trend_result(today:str=''):
    try:
        response = requests.get(TREND_API_URL, params={'today':today}, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise e
