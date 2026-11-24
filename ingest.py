import os
import requests
import boto3
import json
from datetime import datetime

# Clé API OpenWeatherMap lue depuis la variable d'environnement (fichier .env)
API_KEY = os.environ["OPENWEATHER_API_KEY"]

VILLES = ["Marrakech", "Tanger", "Dakhla", "Essaouira"]

# Connexion à MinIO
s3 = boto3.client(
    "s3",
    endpoint_url="http://minio:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
)

date = datetime.now().strftime("%Y-%m-%d")
heure = datetime.now().strftime("%Hh")

for ville in VILLES:

    url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    data = response.json()

    nom_fichier = f"city={ville}/date={date}/data_{heure}.json"

    s3.put_object(
        Bucket="bronze",
        Key=f"weather_raw/{nom_fichier}",
        Body=json.dumps(data)
    )

    print(f"✅ {ville} sauvegardé dans MinIO")

print("✅ Ingestion terminée !")