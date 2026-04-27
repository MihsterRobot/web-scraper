'''Entry point for the job listings scraper.'''

from . import scraper_utils as s

URL = 'https://realpython.github.io/fake-jobs/'


def main() -> None:
    parsed = s.parse_html(URL)
    if parsed is None:
        return None


if __name__ == '__main__':
    main()
