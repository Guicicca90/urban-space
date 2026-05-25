<div align="center">

# urban-space

**Real estate ML for the São Paulo market — property pricing, intelligent matching, terrain scouting, and lead mining from public records.**

![Python](https://img.shields.io/badge/Python-0d1117?style=for-the-badge&logo=python&logoColor=58a6ff)
![scikit-learn](https://img.shields.io/badge/scikit--learn-0d1117?style=for-the-badge&logo=scikitlearn&logoColor=58a6ff)
![BigQuery](https://img.shields.io/badge/BigQuery-0d1117?style=for-the-badge&logo=googlebigquery&logoColor=58a6ff)
![pandas](https://img.shields.io/badge/pandas-0d1117?style=for-the-badge&logo=pandas&logoColor=58a6ff)

</div>

---

## `ml_busca_imoveis/` — KNN Property Matching Engine

A real estate recommendation system that matches buyer profiles to available listings using KNN similarity over normalized property features.

**How it works:**
1. **Parallel ingestion** — fetches listing data and buyer forms from BigQuery concurrently via `ThreadPoolExecutor`
2. **Hard filters** — categorical pre-filtering by `Tipo_Negocio`, `Tipo`, `SubTipo`, `Municipio`, `Bairro` to reduce the candidate space before running KNN
3. **Amenity normalization** — maps 80+ Portuguese amenity strings (e.g. `"Churrasqueira"`, `"Sala de Ginastica"`) to a canonical vocabulary via a lookup dictionary; handles list-valued amenities and unicode normalization with `unidecode`
4. **KNN with StandardScaler** — scales continuous features (`Area_Construida_m2`, `Preco`) independently per query; fits `NearestNeighbors` on the filtered candidate set; returns ranked similarity scores
5. **Output** — ranked recommendations with Google Maps links written back to BigQuery (`Warehouse.Recomendacoes`)

**Key design:** hard filters before KNN — avoids distance pollution from type/location mismatches while keeping the model lightweight and fast on large listing datasets.

---

## `notebooks/` — Property Pricing & Market Intelligence

### Pricing model (`1 - ml_precificacao.ipynb`)
Multilevel regression framework for fair value estimation integrating:
- **GeoSampa** — IPTU records, zoning, land use, urban density by parcel
- **RAIS** — labor market composition and wage levels by municipality
- **IPEA / ONU** — HDI, UDH, socioeconomic development indices
- **BCB / FipeZAP / IGMI-R** — Selic, IPCA, real estate price indices as temporal controls

Feature engineering: spatial lag variables, log-price normalization, interaction terms between zoning and socioeconomic indicators. Output: fair value bands with inequality pattern mapping across São Paulo districts.

### Automated terrain scouting (`pesquisas_iptu.ipynb`, `trataI_iptu_venal.ipynb`)
Geospatial ML pipeline built for São Paulo's 2023 urban densification plan:
- **PCA** — reduces dimensionality across IPTU fiscal value, lot area, zoning class, floor-area ratio, and socioeconomic features
- **KNN in PCA space** — finds underutilized lots structurally similar to known high-potential parcels
- Surfaces development opportunities from 11M+ IPTU records without manual inspection

### Lead mining pipeline (`01–04_*.ipynb`)
End-to-end owner contact extraction from public IPTU records:
1. Bulk IPTU query by neighborhood and property type
2. Owner name extraction and CPF inference
3. Contact lookup via SeekLoc API
4. Structured output: owner name, phone, email, property address — ready for outreach

---

## Data sources

| Source | Used for |
|--------|----------|
| GeoSampa (PMSP) | IPTU records, zoning, land use, 11M+ parcels |
| RAIS (MTE) | Labor market composition by municipality |
| IPEA | Socioeconomic indicators — HDI, income, education |
| ONU / UDH | Sub-municipal human development index |
| BCB / FipeZAP / IGMI-R | Real estate price indices and macro controls |
| VivaReal (scraped) | Active listing inventory with full feature set |

---

*Geodata enrichment: [bquant/geo](https://github.com/Guicicca90/bquant) — `GeoPipeline` produces the parquet files consumed here.*
*Rural counterpart: [solo-inteligente](https://github.com/Guicicca90/solo-inteligente).*
