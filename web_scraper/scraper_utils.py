'''Utility functions for scraping job listings from a target URL.'''

import requests

from bs4 import BeautifulSoup
from bs4 import Tag


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


def is_apply_link(text: str) -> bool:
    """Return True if the given text contains the word 'Apply'."""
    return 'Apply' in text


def get_job_listings(parsed_html: Tag) -> list[list[Tag | str]]:
    '''Extract all job listings from the parsed HTML.
    
    Args:
        parsed_html: A BeautifulSoup Tag containing the results container.
    
    Returns:
        A list of job listings, where each listing is a list of
        [title, company, location, url].
    '''
    jobs = parsed_html.find_all('div', class_='card-content')
    listings = []

    for job in jobs:
       title = job.find('h2', class_='title') or 'N/A'
       company = job.find('h3', class_='company') or 'N/A'
       location = job.find('p', class_='location') or 'N/A'
       link = job.find('a', string=is_apply_link)  # type: ignore
       url = link['href'] if link is not None else 'N/A'
       listings.append([title, company, location, url])

    return listings


def filter_job_listings(listings: list[list[Tag | str]], keyword: str) -> list[list[Tag | str]]:
    '''Filter job listings by keyword match against the job title.
    
    Args:
        listings: A list of job listings returned by get_job_listings.
        keyword: The keyword to search for in job titles.
    
    Returns:
        A filtered list of job listings whose titles contain the keyword.
    '''
    filtered = []
    for job in listings:
        if keyword in job[0].text.strip().lower():  # type: ignore
            filtered.append(job)
    return filtered


def display_job_listings(listings: list[list[Tag | str]]) -> None:
    '''Print title, company, location, and apply URL for each job listing.
    
    Args:
        listings: A list of job listings returned by get_job_listings
                  or filter_job_listings.
    '''
    for job in listings:
        print('Title:', job[0].text.strip())  # type: ignore
        print('Company:', job[1].text.strip())  # type: ignore
        print('Location:', job[2].text.strip())  # type: ignore
        print('Apply:', job[3])
