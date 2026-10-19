import time 
import requests
from bs4 import BeautifulSoup
from config import HEADERS, SLEEP_SECONDS
from RateLimitError import RateLimitError

def get_soup(url, sleep=SLEEP_SECONDS, max_retries=3):

    """
    We use this code for the HTML table and page in general to be redable and understandable for the code in python making it easier to clean and save in the csv.
    """
    
    for attempt in range(1, max_retries + 1):
        response = requests.get(url, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            time.sleep(sleep)
            return BeautifulSoup(response.content, "html.parser")
 
        if response.status_code == 429:
            raise RateLimitError(f"Error in {url}: {response.status_code} - {response.reason}. You have been rate limited. Please try again later.")
        
        if response.status_code >= 500:
            time.sleep(sleep * attempt)
            continue
        
        raise RuntimeError(f"Error in {url}: {response.status_code} - {response.reason}.")
    raise RuntimeError(f"Could not retrieve {url} after {max_retries} attempts")