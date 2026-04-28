import pytest
from bs4 import BeautifulSoup

from web_scraper import scraper_utils as s


@pytest.fixture
def sample_listings():
    job1 = BeautifulSoup('<h2>Python Backend Developer</h2>', 'html.parser')
    tag1 = job1.find('h2')
    listing1 = [tag1, 'Aerospace', 'USA', 'www.aerospace.com']

    job2 = BeautifulSoup('<h2>Fullstack Developer Python</h2>', 'html.parser')
    tag2 = job2.find('h2')
    listing2 = [tag2, 'Infinity', 'London', 'www.infinity.com']

    job3 = BeautifulSoup('<h2>Embedded Systems Engineer C++</h2>', 'html.parser')
    tag3 = job3.find('h2')
    listing3 = [tag3, 'NASA', 'USA', 'www.nasa.com']

    return [listing1, listing2, listing3]


def test_filter_returns_matching_listings(sample_listings):
    result = s.filter_job_listings(sample_listings, keyword='python')
    expected_output = [sample_listings[0], sample_listings[1]]
    assert result == expected_output


def test_filter_returns_empty_list_for_no_matches(sample_listings):
    result = s.filter_job_listings(sample_listings, keyword='AI')
    expected_output = []
    assert result == expected_output


def test_filter_returns_empty_list_for_empty_input(sample_listings):
    result = s.filter_job_listings([], keyword='robotics')
    expected_output = []
    assert result == expected_output


def test_filter_is_case_insensitive(sample_listings):
    result = s.filter_job_listings(sample_listings, keyword='Backend')
    expected_output = [sample_listings[0]]
    assert result == expected_output
