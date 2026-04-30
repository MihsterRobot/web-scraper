'''Entry point for scrapers.'''

from web_scraper.scrapers import fake_jobs


def main() -> None:
    fake_jobs.run()


if __name__ == '__main__':
    main()
