'''Entry point for scrapers.'''

from web_scraper.scrapers import fake_jobs
from web_scraper.scrapers import quotes

SCRAPERS = ['Fake Jobs', 'Quotes']


def main() -> None:
    print('Available scrapers:')
    for i, name in enumerate(SCRAPERS, start=1):
        print(f'{i}. {name}')
    line = int(input('Enter your choice: '))

    if line == 1:
        filter_choice = input('Enter yes or no to enable filtering: ').lower()
        if filter_choice == 'yes':
            keyword = input('Enter the keyword: ')
            fake_jobs.run(keyword)
        else:
            fake_jobs.run()
    elif line == 2:
        quotes.run()
    else:
        print(f'Invalid option. Please enter a number between 1 and {len(SCRAPERS)}.')
        # Implement loop to allow user to make another choice


if __name__ == '__main__':
    main()
