import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://fr.jobs.sanofi.com/recherche-d%27offres?k=data+engineer&orgIds=20874'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Accept-Language': 'FR, en;q=0.5',
}

response = requests.get(url, headers=headers)
htmlData = response.content
if response.status_code == 200:
    soup = BeautifulSoup(htmlData, 'html.parser')

    jobs = soup.select('#search-results-list > ul:nth-child(1) li')

    jobs_data = []

    for job in jobs:

        poste = job.find('h2').text
        job_location_total = job.find('span', class_ = "job-location")
        city = job_location_total.get_text().split(',')[0]
        country = job_location_total.get_text().split()[1]

        job_date_posted = job.find('span', class_ = "job-date-posted").text

        jobs_data.append({'Poste': poste, "Ville ": city, "Pays": country, "Date": job_date_posted})

    df_jobs = pd.DataFrame(jobs_data)
    print(df_jobs.to_string())
    df_jobs.to_csv('jobs_sanofi.csv', index=False)
else:
    print(f"Erreur lors de la récupération de la page : {response.status_code}")
