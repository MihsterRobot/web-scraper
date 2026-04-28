import requests

import pytest
from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock

from web_scraper import scraper_utils as s


@pytest.fixture
def sample_parsed_html():
    html = '''
        <div id='ResultsContainer'>
            <div class='card-content'>
                <h2 class="title">Python Backend Developer</h2>
                <h3 class='company'>NASA</h3>
                <p class='location'>USA</p>
                <a href='www.nasa.com'>Apply</a>
            </div>
            <div class='card-content'>
                <h2 class="title">Kryptonite Engineer</h2>
                <h3 class='company'>Luthor Corp</h3>
                <p class='location'>Metropolis</p>
                <a href='www.luthorcorp.com'>Apply</a>
            </div>
             <div class='card-content'>
                <h2 class="title">Systems Architect C#</h2>
                <h3 class='company'>Neon</h3>
                <p class='location'>Neptune</p>
                <a href='www.neon.com'>Apply</a>
            </div>
        </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find(id='ResultsContainer')


@pytest.fixture
def sample_listings():
    job1 = BeautifulSoup('''
        <h2 class='title'>Python Backend Developer</h2>
        <h3 class='company'>NASA</h3>
        <p class='location'>USA</p>
    ''', 'html.parser')
    title1 = job1.find('h2')
    company1 = job1.find('h3')
    location1 = job1.find('p')
    listing1 = [title1, company1, location1, 'www.nasa.com']

    job2 = BeautifulSoup('''
        <h2 class='title'>Kryptonite Engineer</h2>
        <h3 class='company'>Luthor Corp</h3>
        <p class='location'>Metropolis</p>
    ''', 'html.parser')
    title2 = job2.find('h2')
    company2 = job2.find('h3')
    location2 = job2.find('p')
    listing2 = [title2, company2, location2, 'www.luthorcorp.com']

    job3 = BeautifulSoup('''
        <h2 class='title'>Systems Architect C#</h2>
        <h3 class='company'>Neon</h3>
        <p class='location'>Neptune</p>
    ''', 'html.parser')
    title3 = job3.find('h2')
    company3 = job3.find('h3')
    location3 = job3.find('p')
    listing3 = [title3, company3, location3, 'www.neon.com']

    return [listing1, listing2, listing3]


def test_parse_html_success():
    # Create a MagicMock object to represent a requests response.
    mock_response = MagicMock()

    # Fake HTTP response body containing a ResultsContainer div.
    mock_response.content = b'''
        <div id='ResultsContainer'>
            <div class='card-content'>
                <h2 class='title'>Sixer</h2>
                <h3 class='company'>IOI</h3>
                <p class='location'>Ohio</p>
            </div>
        </div>
    '''

    # Replace requests.get in scraper_utils with the mock_response to imitate a network request by parse_html.
    with patch("web_scraper.scraper_utils.requests.get", return_value=mock_response):
        result = s.parse_html('http://fake-url.com')

    assert result is not None
    assert result.get('id') == 'ResultsContainer'


def test_parse_html_returns_none_on_network_error():
    # Use side_effect instead of return_value because a network error prevents
    # requests.get() from returning a response; it raises an exception directly,
    # triggering parse_html's 'except' block.
    with patch("web_scraper.scraper_utils.requests.get", side_effect=requests.exceptions.RequestException):
        result = s.parse_html("http://fake-url.com")
    assert result is None


def test_parse_html_returns_none_on_bad_status_code():
    mock_response = MagicMock()
    mock_response.content = b'''
        <div id='ResultsContainer'>
            <div class='card-content'>
                <h2 class='title'>Differential Inspector</h2>
                <h3 class='company'>Alt Industries</h3>
                <p class='location'>Texas</p>
            </div>
        </div>
    '''

    # raise_for_status() raises an HTTPError on bad status codes,
    # triggering parse_html's 'except' block to return None.
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError

    # Return mock_response to parse_html so raise_for_status() can be called on it.
    with patch("web_scraper.scraper_utils.requests.get", return_value=mock_response):
        result = s.parse_html('http://fake-url.com')
    
    assert result is None


def test_get_listings_returns_correct_number_of_listings(sample_parsed_html):
    result = s.get_job_listings(sample_parsed_html)
    assert len(result) == 3


def test_get_listings_returns_matching_listings(sample_parsed_html):
    result = s.get_job_listings(sample_parsed_html)

    assert result[0][0].text.strip() == 'Python Backend Developer'  # type: ignore
    assert result[0][1].text.strip() == 'NASA' # type: ignore
    assert result[0][2].text.strip() == 'USA' # type: ignore
    assert result[0][3] == 'www.nasa.com'

    assert result[1][0].text.strip() == 'Kryptonite Engineer'  # type: ignore
    assert result[1][1].text.strip() == 'Luthor Corp'  # type: ignore
    assert result[1][2].text.strip() == 'Metropolis'  # type: ignore
    assert result[1][3] == 'www.luthorcorp.com'

    assert result[2][0].text.strip() == 'Systems Architect C#'  # type: ignore
    assert result[2][1].text.strip() == 'Neon'  # type: ignore
    assert result[2][2].text.strip() == 'Neptune'  # type: ignore
    assert result[2][3] == 'www.neon.com'


def test_filter_returns_matching_listings(sample_listings):
    result = s.filter_job_listings(sample_listings, keyword='python')
    expected_output = [sample_listings[0]]
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


def test_display_listings_output(capsys, sample_listings):
    s.display_job_listings(sample_listings)
    captured = capsys.readouterr()
    
    assert 'Python Backend Developer' in captured.out
    assert 'NASA' in captured.out
    assert 'USA' in captured.out
    assert 'www.nasa.com' in captured.out
