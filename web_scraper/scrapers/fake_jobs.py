'''Scraper for extracting job listings from the Real Python fake jobs site.'''

from bs4 import Tag

from web_scraper.scraper_utils import parse_html

URL = 'https://realpython.github.io/fake-jobs/'


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
        if keyword.lower() in job[0].text.strip().lower():  # type: ignore
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


def run():
    parsed = parse_html(URL)

    if parsed is None:
        return
    
    listings = get_job_listings(parsed)
    filtered = filter_job_listings(listings, 'python')

    display_job_listings(filtered)
