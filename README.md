# Projet Météo — Pipeline de données (architecture Médaillon)

Pipeline qui récupère la météo de plusieurs villes marocaines (Marrakech, Tanger, Dakhla, Essaouira) via l'API OpenWeatherMap, la stocke dans MinIO selon une architecture **Bronze / Silver / Gold**, orchestrée par **Apache Airflow**, et visualisée dans **Power BI**.

## Architecture

| Étape | Script | Rôle |
|---|---|---|
| Bronze | `ingest.py` | Appel API OpenWeatherMap → JSON bruts dans `bronze/weather_raw/` |
| Silver | `silver_transform.py` | Nettoyage / typage → CSV dans `silver/weather_clean/` |
| Gold | `gold_transform.py` | Score météo + classement des villes → CSV dans `gold/weather_analytics/` |
| Qualité | `quality_checks.py` | Vérifie que chaque couche contient des données |

Le DAG `airflow/dags/weather_pipeline.py` enchaîne les étapes tous les jours à 6 h :
`ingestion → silver_transform → gold_transform → quality_checks`

## Lancer le projet

1. Créer le fichier `.env` à partir du modèle et y mettre votre clé OpenWeatherMap :
   ```bash
   cp .env.example .env
   ```
2. Démarrer les services :
   ```bash
   docker compose up -d
   ```
3. Créer le bucket `bronze` dans la console MinIO : http://localhost:9001 (minioadmin / minioadmin)
4. Ouvrir Airflow : http://localhost:8080 (admin / admin) et activer le DAG `weather_pipeline`.

## Autres fichiers

- `suivi meteo.pbix` — tableau de bord Power BI
- `rapport_architecture_des_donnes.pdf` — rapport du projet
