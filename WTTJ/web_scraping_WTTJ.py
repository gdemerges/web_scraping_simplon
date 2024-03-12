import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la page à scraper
url = "https://www.welcometothejungle.com/fr/jobs?refinementList%5Boffices.country_code%5D%5B%5D=FR&query=data%20engineer%20alternance&page=1"

# En-têtes HTTP pour simuler une visite depuis un navigateur web
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
}

# Effectuer la requête GET
response = requests.get(url, headers=headers)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Parser le contenu HTML de la page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Sélecteur CSS pour cibler les offres d'emploi
    # Note : Ce sélecteur doit être ajusté en fonction de la structure actuelle de la page
    job_offers_selector = '.sc-1wqurwm-0 div'

    # Trouver les éléments correspondant aux offres d'emploi
    job_offers = soup.select(job_offers_selector)

    # Liste pour stocker les données des offres d'emploi
    jobs_data = []

    for job_offer in job_offers:
        # Exemple d'extraction d'un titre d'offre d'emploi
        # Note : Ces sélecteurs doivent être ajustés en fonction des données spécifiques que vous souhaitez extraire
        job_title = job_offer.find("h4").text.strip()
        # Ajouter d'autres champs selon besoin

        # Ajouter les données à notre liste
        jobs_data.append({
            "Titre": job_title,
            # Ajoutez d'autres champs ici
        })

    # Convertir la liste en DataFrame
    df_jobs = pd.DataFrame(jobs_data)

    # Afficher les données extraites
    print(df_jobs)
else:
    print("Erreur lors de la récupération de la page.")
