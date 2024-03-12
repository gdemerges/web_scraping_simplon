import requests
from bs4 import BeautifulSoup
import pandas as pd

#Fonction qui récupère les données des offres d'emploi
def fetch_jobs_data(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        jobs = soup.select('#search-results-list > ul:nth-child(1) li')
        return jobs
    else:
        print(f"Erreur lors de la récupération de la page : {response.status_code}")
        return []

#Fonction pour le scraping
def scrap_job_data(job):
    poste = job.find('h2').text.strip()
    job_location_total = job.find('span', class_="job-location")
    city, country = job_location_total.get_text().strip().split(', ') #Sépare la ville et le pays, on enlève la virgule
    job_date_posted = job.find('span', class_="job-date-posted").text.strip()
    return {'Poste': poste, "Ville": city, "Pays": country, "Date": job_date_posted}

def main(n):
    url_base = 'https://fr.jobs.sanofi.com/recherche-d%27offres?k=data+engineer&orgIds=20874&page='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'Accept-Language': 'FR, en;q=0.5',
    }

    jobs_data = []

    #Permet de parcourir les pages
    for page_num in range(0, n):
        url = f"{url_base}{page_num}"
        jobs = fetch_jobs_data(url, headers)
        for job in jobs:
            job_data = scrap_job_data(job)
            jobs_data.append(job_data)

    if jobs_data:
        df_jobs = pd.DataFrame(jobs_data)
        print(df_jobs.to_string())
        #Créer un CSV reprenant les données récupérées
        df_jobs.to_csv('data/jobs_sanofi.csv', index=False)
    else:
        print("Aucune donnée d'emploi récupérée.")

#Appelle la fonction main et on passe en paramètre le nombre de pages souhaité
main(2)
