import os
import json
import requests

from constants import GEOJSON_URL, GEOJSON_CACHE

def get_geojson(cache_path=GEOJSON_CACHE, url=GEOJSON_URL):
    
    """
    This code is the one tha fetches the GeoJSON data, and saves it in a specific path
    """
    
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch GeoJSON data: {response.status_code}")
    
    geojson_data = response.json()
    
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(geojson_data, f)
    
    return geojson_data