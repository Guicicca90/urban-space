<div align="center">

# urban-space

**Real estate ML for the São Paulo market — property pricing, inequality mapping, and lead mining from public records.**

![Python](https://img.shields.io/badge/Python-0d1117?style=for-the-badge&logo=python&logoColor=58a6ff)
![scikit-learn](https://img.shields.io/badge/scikit--learn-0d1117?style=for-the-badge&logo=scikitlearn&logoColor=58a6ff)
![pandas](https://img.shields.io/badge/pandas-0d1117?style=for-the-badge&logo=pandas&logoColor=58a6ff)
![Google Cloud](https://img.shields.io/badge/GCP-0d1117?style=for-the-badge&logo=googlecloud&logoColor=58a6ff)

</div>

---

## `ml_busca_imoveis/` — Property Pricing Model

Nationwide framework for predicting Brazilian property fair values.

**Features engineered from:**
- GeoSampa: zoning, land use, urban density, IPTU records
- RAIS: labor market composition by municipality
- IPEA / ONU: socioeconomic development indices (HDI, UDH)
- BCB / FipeZAP / IGMI-R: macroeconomic and real estate price indices

**Methods:** multilevel regression, feature normalization, spatial cross-validation. Estimates fair values and surfaces structural inequality patterns in urban markets.

---

## `notebooks/` — Automated Terrain Scouting

Geospatial ML pipeline built for São Paulo's 2023 urban densification plan.

- **PCA** — reduces dimensionality across IPTU, zoning, and socioeconomic features
- **KNN similarity** — finds lots structurally similar to known high-potential parcels
- Automatically detects underutilized land with development potential
- Turns a manual scouting process into a scalable, data-driven system

---

## Lead Mining

Owner contact extraction from IPTU public records — builds a prospecting pipeline for the São Paulo real estate market without requiring paid data brokers.

---

## Data sources

| Source | Used for |
|--------|----------|
| GeoSampa (PMSP) | Zoning, IPTU, land use, spatial boundaries |
| IPEA | Socioeconomic indicators by municipality |
| RAIS (MTE) | Labor market composition |
| BCB / FipeZAP / IGMI-R | Real estate and macro price indices |

---

*Geodata enrichment utilities live in [bquant/geo](https://github.com/Guicicca90/bquant).*
*Rural counterpart: [solo-inteligente](https://github.com/Guicicca90/solo-inteligente).*
