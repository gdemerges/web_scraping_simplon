import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_jobs_data(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        Data = response.content
        soup = BeautifulSoup(Data, 'html.parser')
        jobs = soup.select('ul.crushed li')
        return jobs
    else:
        print(f"Erreur lors de la récupération de la page : {response.status_code}")
        return []

def parse_job_data(job):
    job_employer = job.find('span', class_='tw-mr-2').text.strip()
    job_name = job.find('a').text.strip()
    contract_type = job.find('span', class_='tw-w-max')
    texte_contract = contract_type.get_text().strip() if contract_type else 'Non Spécifié'
    location = job.find('span', class_="tw-text-ellipsis tw-whitespace-nowrap tw-block tw-overflow-hidden 2xsOld:tw-max-w-[20ch]")
    texte_location = location.get_text().strip() if location else 'Non Spécifié'
    teletravail = job.find('span', attrs={"data-cy": "teleworkInfo"})
    teletravail_t = teletravail.get_text(strip=True) if teletravail else 'Non Spécifié'
    salaire = job.find('span', attrs={"class": "tw-text-jobsCandidacy tw-typo-s"})
    salaire_text = salaire.get_text(strip=True).replace('\u202f', '') if salaire else 'Non Spécifié'
    publish_date = job.find('span', attrs={"class": "md:tw-mt-0 tw-text-xsOld"}).get_text().strip()
    return {'Emploi': job_name, 'Employeur': job_employer, 'Type de Contrat': texte_contract,
            'Lieu': texte_location, 'Télétravail': teletravail_t, 'Salaire': salaire_text,
            'Date de publication': publish_date}

def main(n):
    url_base = 'https://www.hellowork.com/fr-fr/emploi/recherche.html?k=Data+scientist&l=Lyon+69000&p='
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept-Language': 'FR, en;q=0.5',
        }

    jobs_data = []

    for page_num in range(1, n + 1):
        url = f"{url_base}{page_num}&mode=pagination"
        jobs = fetch_jobs_data(url, headers)
        for job in jobs:
            job_data = parse_job_data(job)
            jobs_data.append(job_data)

    if jobs_data:
        df_jobs = pd.DataFrame(jobs_data)
        print(df_jobs.to_string())
        df_jobs.to_csv('jobs_hellowork.csv', index=False)
    else:
        print("Aucune donnée d'emploi récupérée.")

main(2)
