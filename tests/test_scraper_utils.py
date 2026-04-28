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
