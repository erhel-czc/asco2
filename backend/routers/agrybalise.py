from fastapi import APIRouter, HTTPException

import csv
import unicodedata

AGRYBALISE_CSV_PATH = "data/agribalyse-31-synthese.csv"

def normalize_string(input_string: str) -> str:
    """
    Normalize a string by removing accents and converting it to lowercase.
    """
    normalized_string = unicodedata.normalize('NFKD', input_string)
    return ''.join([c for c in normalized_string if not unicodedata.combining(c)]).lower()


router = APIRouter(prefix="/agrybalise", tags=["agrybalise"])

@router.get("/list_products")
def list_products():
    products = []
    with open(AGRYBALISE_CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # select the columns :
        for row in reader:
            product = {
                "code_ciqual": row["Code CIQUAL"],
                "food_group": row["Groupe d'aliment"],
                "sub_food_group": row["Sous-groupe d'aliment"],
                "product_name_fr": row["Nom du Produit en Français"],
                "climate_change": row["Changement climatique"],
            }
            products.append(product)

    return products

@router.get("/get_product/{code_ciqual}")
def get_product(code_ciqual: str):
    with open(AGRYBALISE_CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Code CIQUAL"] == code_ciqual:
                product = {
                    "code_ciqual": row["Code CIQUAL"],
                    "food_group": row["Groupe d'aliment"],
                    "sub_food_group": row["Sous-groupe d'aliment"],
                    "product_name_fr": row["Nom du Produit en Français"],
                    "climate_change": row["Changement climatique"],
                }
                return product

    raise HTTPException(status_code=404, detail="Product not found")

@router.get("/search_products")
def search_products(query: str):
    results = []
    with open(AGRYBALISE_CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if normalize_string(query) in normalize_string(row["Nom du Produit en Français"]):
                product = {
                    "code_ciqual": row["Code CIQUAL"],
                    "food_group": row["Groupe d'aliment"],
                    "sub_food_group": row["Sous-groupe d'aliment"],
                    "product_name_fr": row["Nom du Produit en Français"],
                    "climate_change": row["Changement climatique"],
                }
                results.append(product)

    if not results:
        raise HTTPException(status_code=404, detail="No products found matching the query")

    return results