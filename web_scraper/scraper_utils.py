import requests

from bs4 import BeautifulSoup
from bs4 import Tag


def parse_html(url: str) -> Tag | None: 
   page = requests.get(url)
   soup = BeautifulSoup(page.content, 'html.parser')
   results = soup.find(id='ResultsContainer')
   return results


def get_job_listings(parsed_html: Tag) -> list[list[str]] | None:
    if parsed_html is None:
        return None

    jobs = parsed_html.find_all('div', class_='card-content')
    listings = []
    for job in jobs:
       title = job.find("h2", class_="title")
       company = job.find("h3", class_="company")
       location = job.find("p", class_="location")
       link = job.find("a", string=lambda text: "Apply" in text)  # type: ignore
       url = link["href"]
       listings.append([title, company, location, url])
    return listings


def filter_job_listings(listings, keyword):
    filtered = []
    for job in listings:
        if keyword in job[0].text.strip().lower():
            filtered.append(job)
    return filtered


def display_job_listings(listings) -> None:
    for job in listings:
        print('Title:', job[0].text.strip())
        print('Company:', job[1].text.strip())
        print('Location:', job[2].text.strip())
        print('Apply:', job[3])
