'''Shared utility functions for web scrapers.'''

import requests

from bs4 import BeautifulSoup, Tag


def parse_html(url: str) -> Tag | None:
    '''Fetch and parse HTML content from the given URL.
    
    Args:
        url: The URL to fetch.
    
    Returns:
        A BeautifulSoup Tag containing the results container,
        or None if the request fails or the element is not found.
    '''
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Error fetching URL: {e}')
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find(id='ResultsContainer')
    return results
