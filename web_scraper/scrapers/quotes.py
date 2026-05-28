'''Scraper for extracting quotes, authors, and tags from quotes.toscrape.com.'''

import requests
from typing import Literal

from bs4 import BeautifulSoup, Tag

URL = 'https://quotes.toscrape.com/'


def parse_quotes_html(url: str) -> BeautifulSoup | None:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Error fetching URL: {e}')
        return None

    return BeautifulSoup(response.content, 'html.parser')


def get_quotes(parsed_html: Tag) -> list[tuple[Tag, Tag, list[Tag]]]:
    quote_divs = parsed_html.find_all('div', class_='quote')
    quotes = []

    for quote_div in quote_divs:
       text = quote_div.find('span', class_='text') or 'N/A'
       author = quote_div.find('small', class_='author') or 'N/A'
       tag_links = quote_div.find_all('a', class_='tag')
       quotes.append((text, author, tag_links))

    return quotes


def filter_quotes(quotes: list[tuple[Tag, Tag, list[Tag]]], keyword: str, filter_type: Literal['text', 'author', 'tag']) -> list[tuple[Tag, Tag, list[Tag]]]:
    filtered = []
    keyword = keyword.lower()
    for quote in quotes:
        if filter_type == 'text':
            if keyword in quote[0].text.strip().lower():
                filtered.append(quote)
        elif filter_type == 'author':
            if keyword in quote[1].text.strip().lower():
                filtered.append(quote)
        elif filter_type == 'tag':
            for tag in quote[2]:
                if keyword in tag.text.lower():
                    filtered.append(quote)
    return filtered


def display_quotes(quotes: list[tuple[Tag, Tag, list[Tag]]]) -> None:
    for quote in quotes:
        print('Quote:', quote[0].text.strip())
        print('Author:', quote[1].text.strip())
        tags = ', '.join(tag.text.strip() for tag in quote[2])
        print('Tags:', tags, end='\n\n')


def run() -> None:
    parsed = parse_quotes_html(URL)

    if parsed is None:
        return

    quotes = get_quotes(parsed)
    # display_quotes(quotes)

    filtered1 = filter_quotes(quotes, 'Jane Austen', 'author')
    display_quotes(filtered1)

    text = 'I have not failed.'
    filtered2 = filter_quotes(quotes, '10,000', 'text')
    display_quotes(filtered2)
