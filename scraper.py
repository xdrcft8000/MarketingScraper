from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import json

app = FastAPI()

@app.get("/getTPXJobListings")
def get_tpx_job_listings():
    url = "https://careers.tpximpact.com/vacancies/vacancy-search-results.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Assuming job listings are contained within a specific HTML structure
    # You need to inspect the page to find the correct tags and classes
    job_listings = soup.find_all('a', class_='vacancy-title')  # Example class name
    jobs = []
    for job in job_listings:
        jobs.append(scrape_job(job['href']))

    return jobs

def scrape_job(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    description = soup.find_all('script', type='application/ld+json')
    json_data = json.loads(description[0].text)[0]
    return json_data