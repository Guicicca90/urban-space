# urban-space

Real estate ML for the São Paulo market — property pricing, inequality mapping, and lead mining from public records.

---

## What it does

**Property pricing model**
Nationwide framework for predicting Brazilian property fair values. Integrates:
- Public socioeconomic data: IPEA, ONU, RAIS
- Macroeconomic indicators: Selic, IPCA, IGPM, FIPEZAP, IGMI-R
- Geospatial features from GeoSampa (zoning, land use, urban density)

Applies multilevel regression and feature engineering to estimate fair values and identify structural inequality patterns in urban markets.

**Automated terrain scouting**
Geospatial ML pipeline built for São Paulo's 2023 urban densification plan:
- PCA + KNN similarity across IPTU and zoning datasets
- Automatically detects underutilized lots with development potential
- Turns manual scouting into a scalable, data-driven system

**Lead mining**
Owner contact extraction from IPTU public records — building a prospecting pipeline for the São Paulo real estate market.

---

## Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikitlearn&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=white)
![Google Cloud](https://img.shields.io/badge/GCP-4285F4?style=flat&logo=googlecloud&logoColor=white)

---

## Data sources

| Source | Used for |
|--------|----------|
| GeoSampa (PMSP) | Zoning, IPTU, land use |
| IPEA | Socioeconomic indicators |
| RAIS | Labor market by municipality |
| BCB / FipeZAP | Real estate price indices |

---

*Geodata enrichment utilities live in [bquant/geo](https://github.com/MaxPower90/bquant).*
