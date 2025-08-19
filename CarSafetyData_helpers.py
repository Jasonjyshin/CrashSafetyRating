import requests
import time
from collections import defaultdict

start_year = 1990
end_year = 2026


def get_all_brands(year):
    url = f"https://api.nhtsa.gov/SafetyRatings/modelyear/{year}?format=json"
    response = requests.get(url)
    results = response.json().get("Results", [])
    
    if not results:
        return []
    
    brands = set() #get all unique makes (brands)
    for item in results: 
        make = item.get("Make")
        if make:
            brands.add(make.lower()) #lowercase for consistency

    return sorted(list(brands))


def get_models_for_brand_year(year, make):
    url = f"https://api.nhtsa.gov/SafetyRatings/modelyear/{year}/make/{make}?format=json"
    response = requests.get(url)
    return response.json().get("Results", [])

def get_vehicle_ids_from_models(models):
    vehicle_ids = []
    for model in models:
        vehicle_id = model.get("VehicleId")
        if vehicle_id:
            vehicle_ids.append(vehicle_id)
    return vehicle_ids

def get_vehicle_rating(vehicle_id):
    url = f"https://api.nhtsa.gov/SafetyRatings/VehicleId/{vehicle_id}?format=json"
    response = requests.get(url)
    results = response.json().get("Results", [])
    if results: 
        return results[0].get("OverallRating")
    else:
        return None
    




#ask user for a year and fetch brands
year_input = int(input(f"Enter a year between {start_year} and {end_year}: "))
brands = get_all_brands(year_input)

if not brands:
    print("No brands found for that year")
else:
    print(f"Found {len(brands)} brands for {year_input}: ")
    print(brands[:10]) #show first 10 for preview





