import boto3
import pandas as pd

s3 = boto3.client(
    "s3",
    endpoint_url="http://minio:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
)

BUCKET = "bronze"

# Vérification Bronze
bronze = s3.list_objects_v2(
    Bucket=BUCKET,
    Prefix="weather_raw/"
)

assert "Contents" in bronze

print("✅ Bronze OK")

# Vérification Silver
silver = s3.list_objects_v2(
    Bucket=BUCKET,
    Prefix="silver/weather_clean/"
)

assert "Contents" in silver

print("✅ Silver OK")

# Vérification Gold
gold = s3.list_objects_v2(
    Bucket=BUCKET,
    Prefix="gold/weather_analytics/"
)

assert "Contents" in gold

print("✅ Gold OK")

print("✅ Tous les tests sont validés")