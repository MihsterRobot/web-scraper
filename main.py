import requests
from bs4 import BeautifulSoup


URL = "https://realpython.github.io/fake-jobs/"
# Issue HTTP GET request to retrieve HTML data
page = requests.get(URL) 
# Print HTML data as text
print(page.text) 

# Using .content instead of .text avoids issues with character encoding
# .content holds raw bytes, which can be decoded better than text representation
# html.parser ensures the appropriate parser is used for HTML content
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")  # Find specific HTML element by ID

# prettify() formats the parse tree such that each tag is on its own separate line with indentation
print(results.prettify())

# find_all() returns iterable containing all HTML for all job listings displayed on page
job_elements = results.find_all("div", class_="card-content")

for job_element in job_elements:
    print(job_element.prettify(), end="\n"*2)
print()

for job_element in job_elements:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip(), "\n")

# Passing anonymous function (lambda) to string=, which looks at each
# <h2> element, converts it to lowercase, and checks for substring "python"
python_jobs = results.find_all("h2", string=lambda text: "python" in text.lower())

# Using list comprehension ["expression" for "member" in "iterable"]
python_job_elements = [h2_element.parent.parent.parent for h2_element in python_jobs]

print("Number of Python jobs: ", end="")
print(len(python_jobs))

for job_element in python_job_elements:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    print()
 
# Print URL for applying to Python jobs
for job_element in python_job_elements:
    links = job_element.find_all("a", string=lambda text: "Apply" in text)
    for link in links:
        link_url = link["href"]
        print(f"Apply here: {link_url}n")
