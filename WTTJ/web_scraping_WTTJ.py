import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.welcometothejungle.com/fr/jobs?refinementList%5Boffices.country_code%5D%5B%5D=FR&query=data%20engineer%20alternance&page=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
}

response = requests.get(url, headers=headers)
htmlData = response.content

if response.status_code == 200:
    soup = BeautifulSoup(htmlData, 'html.parser')

    job_offers = soup.select('.sc-1wqurwm-0 div')
    print (job_offers)

    jobs_data = []

    for job_offer in job_offers:
        job_title = job_offer.find("h4").text.strip()

        jobs_data.append({
            "Titre": job_title,
        })

    df_jobs = pd.DataFrame(jobs_data)

    print(df_jobs)
else:
    print("Erreur lors de la récupération de la page.")
