# Data Documentation for the emission factors and carbon footprint calculations

## Agribalyse data
For the food-related data, we use the [Agribalyse database](https://data.ademe.fr/datasets/agribalyse-31-synthese). This database provides detailed information on the environmental impact of various food products, including their carbon footprint, water usage, and other environmental indicators.

The `/data/agribalyse-31-synthese.csv` files from Agribalyse contain the whole set of data, but we will focus on the following columns:
- `Code AGB`: Unique identifier for the food product.
- `Nom du Produit en Français`: Name of the food product in French.
- `Changement climatique` : Carbon footprint of the food product in kg CO2 equivalent per kg of product.

The file contains a large amount of columns, which can be explored in more detail in the Agribalyse documentation, but we won't use all of them for the moment.

## ImpactCO2 API
For the biggest part, the data used in this project comes from the [impactCO2 API](https://impactco2.fr/doc/api). This API provides emission factors and carbon footprint calculations for various activities, including food consumption, transportation, and digital usage.

The themes covered by the API include:
```json
{
  "data": [
    {
      "id": 1,
      "name": "Numérique",
      "slug": "numerique"
    },
    {
      "id": 2,
      "name": "Alimentation",
      "slug": "alimentation"
    },
    {
      "id": 3,
      "name": "Boisson",
      "slug": "boisson"
    },
    {
      "id": 4,
      "name": "Transport",
      "slug": "transport"
    },
    {
      "id": 5,
      "name": "Habillement",
      "slug": "habillement"
    },
    {
      "id": 6,
      "name": "Électroménager",
      "slug": "electromenager"
    },
    {
      "id": 7,
      "name": "Mobilier",
      "slug": "mobilier"
    },
    {
      "id": 8,
      "name": "Chauffage",
      "slug": "chauffage"
    },
    {
      "id": 9,
      "name": "Fruits et légumes",
      "slug": "fruitsetlegumes"
    },
    {
      "id": 10,
      "name": "Usage numérique",
      "slug": "usagenumerique"
    },
    {
      "id": 13,
      "name": "Cas pratiques",
      "slug": "caspratiques"
    }
  ]
}
```

### Basic doc for the impactCO2 API
Link to the API: [https://impactco2.fr/doc/api](https://impactco2.fr/doc/api)