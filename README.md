<div align="center">

# urban-space

**Predicting property prices of Brazilian markets using machine learning on socioeconomic data.**

![Python](https://img.shields.io/badge/Python-0d1117?style=for-the-badge&logo=python&logoColor=58a6ff)
![scikit-learn](https://img.shields.io/badge/scikit--learn-0d1117?style=for-the-badge&logo=scikitlearn&logoColor=58a6ff)
![BigQuery](https://img.shields.io/badge/BigQuery-0d1117?style=for-the-badge&logo=googlebigquery&logoColor=58a6ff)
![pandas](https://img.shields.io/badge/pandas-0d1117?style=for-the-badge&logo=pandas&logoColor=58a6ff)

</div>

---

## The Problem

Brazilian real estate data is fragmented, unreliable, and expensive. Registry (cartório) records are incomplete. Price per square meter varies wildly not just by location but by economic cycle, labor market composition, zoning, and urban density — factors that traditional brokers price by gut feeling.

The core insight: since reliable transaction data is scarce, prices can be normalized by location using public socioeconomic indicators as a structural baseline. This creates a multiplier for price-per-square-meter that captures inequality patterns across the city.

---

## `ml_busca_imoveis/` — KNN Property Matching Engine

A recommendation system that matches buyer profiles to available listings using KNN similarity over normalized property features.

**Pipeline:**
1. **Parallel ingestion** — fetches listing inventory and buyer intake forms from BigQuery concurrently via `ThreadPoolExecutor`
2. **Hard filtering** — pre-filters by `Tipo_Negocio`, `Tipo`, `SubTipo`, `Municipio`, `Bairro` before running KNN, avoiding distance pollution from type/location mismatches
3. **Amenity normalization** — maps 80+ Portuguese amenity strings (`"Churrasqueira"`, `"Sala de Ginastica"`, `"Heliponto"`) to a canonical vocabulary; handles multi-valued amenities and unicode normalization with `unidecode`
4. **KNN with StandardScaler** — scales continuous features (`Area_Construida_m2`, `Preco`) per query; fits `NearestNeighbors` on filtered candidates; returns ranked similarity scores
5. **Output** — recommendations with Google Maps links written back to BigQuery (`Warehouse.Recomendacoes`)

---

## `notebooks/` — Pricing Model & Market Intelligence

### Property pricing model

Multilevel regression framework integrating two categories of features:

**Property-level features** (from GeoSampa / VivaReal):
- Type, subtype, zoning class, floor-area ratio, lot area, built area
- Rooms, suites, parking, amenities (pool, gym, gourmet space, etc.)
- IPTU fiscal value, condominium fee

**Macro & socioeconomic controls** (monthly, scraped from public sources):

| Indicator | Source | What it captures |
|-----------|--------|-----------------|
| FipeZAP | FIPE | Price/m² by city, type, rooms |
| IGMI-R | BCB | Real estate market profitability by capital |
| IGP-M | FGV | Rental inflation |
| Selic | BCB | Base interest rate (financing cost) |
| IPCA | IBGE | General inflation |
| INCC | FGV | Civil construction cost index |
| IBC-BR | BCB | GDP preview (economic cycle proxy) |
| IVG-R | BCB | Residential collateral value index |
| IIE-BR | FGV | Economic uncertainty indicator |
| CubSP | SINDUSCON | Construction cost in São Paulo |

FipeZAP matching logic: exact match by city/type/rooms → fallback to total rooms → residential type → state capital → national average.

### Automated terrain scouting

Built for São Paulo's 2023 urban densification plan, which opened zoning for higher-density construction near transit hubs — creating demand for buildable lots faster than traditional "perdigueiros" (manual scouts) could supply.

- **PCA** — dimensionality reduction across IPTU fiscal value, lot area, zoning class, floor-area ratio, and socioeconomic features
- **KNN in PCA space** — finds underutilized lots structurally similar to known high-potential parcels from 11M+ IPTU records
- Surfaces development opportunities at scale, replacing a labor-intensive manual process

### Lead mining pipeline

End-to-end owner contact extraction from public IPTU records:
1. Bulk IPTU query by neighborhood and property type
2. Owner name extraction and CPF inference
3. Contact lookup via SeekLoc API
4. Output: owner name, phone, email, property — ready for outreach

---

## Data sources

| Source | Used for |
|--------|----------|
| GeoSampa (PMSP) | 11M+ IPTU records, zoning, land use, spatial boundaries |
| RAIS (MTE) | Labor market composition and wage levels by municipality |
| IPEA | Socioeconomic development indices |
| ONU / UDH | Sub-municipal human development index |
| BCB / FipeZAP / IGMI-R / IGP-M | Real estate and macro price indices |
| VivaReal (scraped) | Active listing inventory with full feature set |

---

*Geodata enrichment: [bquant/geo](https://github.com/Guicicca90/bquant) — `GeoPipeline` produces the parquet files consumed here.*
*Rural counterpart: [solo-inteligente](https://github.com/Guicicca90/solo-inteligente).*
