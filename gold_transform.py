import boto3
import pandas as pd
from io import BytesIO
from datetime import datetime

# Connexion MinIO
s3 = boto3.client(
    "s3",
    endpoint_url="http://minio:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
)

BUCKET = "bronze"

# Lire dernier fichier Silver
response = s3.list_objects_v2(
    Bucket=BUCKET,
    Prefix="silver/weather_clean/"
)

fichiers = response.get("Contents", [])

dernier_fichier = fichiers[-1]["Key"]

obj = s3.get_object(
    Bucket=BUCKET,
    Key=dernier_fichier
)

df = pd.read_csv(obj["Body"])

# KPI météo
df["score_meteo"] = (
    df["temperature"]
    - (df["humidite"] * 0.1)
    - (df["vent"] * 0.5)
)

# Classement
df = df.sort_values(
    by="score_meteo",
    ascending=False
)

df["classement"] = range(1, len(df) + 1)

# Meilleure ville
df["meilleure_ville"] = df["classement"] == 1

# Ajouter date
df["date"] = datetime.now().date()

print(df)

# Sauvegarde CSV
csv_buffer = BytesIO()

df.to_csv(csv_buffer, index=False)

nom_fichier = f"gold/weather_analytics/weather_gold_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

s3.put_object(
    Bucket=BUCKET,
    Key=nom_fichier,
    Body=csv_buffer.getvalue()
)

print("✅ Gold Layer créé avec succès")