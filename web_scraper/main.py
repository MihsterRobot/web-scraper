'''Entry point for the job listings scraper.'''

from . import scraper_utils as s

URL = 'https://realpython.github.io/fake-jobs/'


def main() -> None:
    parsed = s.parse_html(URL)
    if parsed is None:
        return None
    
    listings = s.get_job_listings(parsed)
    filtered = s.filter_job_listings(listings, 'python')
    s.display_job_listings(filtered)


if __name__ == '__main__':
    main()
