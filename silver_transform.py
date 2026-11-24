import boto3
import json
import pandas as pd
from datetime import datetime
from io import BytesIO

# Connexion MinIO
s3 = boto3.client(
    "s3",
    endpoint_url="http://minio:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
)

BUCKET = "bronze"

# Lire les fichiers Bronze
response = s3.list_objects_v2(
    Bucket=BUCKET,
    Prefix="weather_raw/"
)

donnees = []

for obj in response.get("Contents", []):

    key = obj["Key"]

    # Lire fichier JSON
    fichier = s3.get_object(Bucket=BUCKET, Key=key)

    contenu = fichier["Body"].read()

    data = json.loads(contenu)

    try:
        ville = data["name"]
        temperature = float(data["main"]["temp"])
        humidite = int(data["main"]["humidity"])
        meteo = data["weather"][0]["description"]
        vent = float(data["wind"]["speed"])

        event_timestamp = datetime.fromtimestamp(data["dt"])

        ingestion_timestamp = datetime.now()

        donnees.append({
            "ville": ville,
            "temperature": temperature,
            "humidite": humidite,
            "meteo": meteo,
            "vent": vent,
            "event_timestamp": str(event_timestamp),
            "ingestion_timestamp": str(ingestion_timestamp)
        })

    except Exception as e:
        print(f"Erreur : {e}")

# Créer DataFrame
df = pd.DataFrame(donnees)

print(df)

# Sauvegarde CSV
csv_buffer = BytesIO()

df.to_csv(csv_buffer, index=False)

nom_fichier = f"silver/weather_clean/weather_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

s3.put_object(
    Bucket=BUCKET,
    Key=nom_fichier,
    Body=csv_buffer.getvalue()
)

print("✅ Silver Layer créé avec succès")