import requests

from bs4 import BeautifulSoup
from bs4 import Tag


def parse_html(url: str) -> Tag | None:
   try:
        response = requests.get(url)
        response.raise_for_status()
   except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

   soup = BeautifulSoup(response.content, 'html.parser')
   results = soup.find(id='ResultsContainer')
   return results


def is_apply_link(text: str) -> bool:
    return "Apply" in text


def get_job_listings(parsed_html: Tag) -> list[list[Tag | str]]:
    jobs = parsed_html.find_all('div', class_='card-content')
    listings = []

    for job in jobs:
       title = job.find("h2", class_="title") or 'N/A'
       company = job.find("h3", class_="company") or 'N/A'
       location = job.find("p", class_="location") or 'N/A'
       link = job.find("a", string=is_apply_link)  # type: ignore
       url = link['href'] if link is not None else 'N/A'
       listings.append([title, company, location, url])

    return listings


def filter_job_listings(listings: list[list[Tag | str]], keyword: str) -> list[list[Tag | str]]:
    filtered = []
    for job in listings:
        if keyword in job[0].text.strip().lower():  # type: ignore
            filtered.append(job)
    return filtered


def display_job_listings(listings: list[list[Tag | str]]) -> None:
    for job in listings:
        print('Title:', job[0].text.strip())  # type: ignore
        print('Company:', job[1].text.strip())  # type: ignore
        print('Location:', job[2].text.strip())  # type: ignore
        print('Apply:', job[3])
