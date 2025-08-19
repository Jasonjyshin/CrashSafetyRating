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

#test for above
#ask user for a year and fetch brands
year_input = int(input(f"Enter a year between {start_year} and {end_year}: "))
brands = get_all_brands(year_input)

if not brands:
    print("No brands found for that year")
else:
    print(f"Found {len(brands)} brands for {year_input}: ")
    print(brands)



def get_models_for_brand_year(year, make):
    url = f"https://api.nhtsa.gov/SafetyRatings/modelyear/{year}/make/{make}?format=json"
    response = requests.get(url)
    results = response.json().get("Results", [])
    return [model["Model"] for model in results] if results else []

#test for above
brand_input = input(f"Select an available brand from the year {year_input}: ").lower()
brand_year_models = get_models_for_brand_year(year_input, brand_input)
if brand_input not in brands:
    print(f"{brand_input} crash data is not available for the year {year_input}")
else:
    print(f"Available models for {brand_input} in the year {year_input} are: {brand_year_models}")



#return example [{'VehicleDescription': '2021 Jeep Compass SUV 4WD', 'VehicleId': 15500}, {'VehicleDescription': '2021 Jeep Compass SUV FWD', 'VehicleId': 15469}]
def vehicle_trims(year, make, model):
    url = f"https://api.nhtsa.gov/SafetyRatings/modelyear/{year}/make/{make}/model/{model}"
    response = requests.get(url)
    results = response.json().get("Results", [])  
    return [vehicleDescription["VehicleDescription"] for vehicleDescription in results]



#Select vehicle model to see the available trims and their vehicleID
model_selection = input("Select a model to view trim levels: ").upper()
vehicle_trims = vehicle_trims(year_input, brand_input, model_selection)
if model_selection not in brand_year_models:
    print("Invalid model selection")
else:
    print(f"Available trims for a {year_input} {brand_input} {model_selection} are: {vehicle_trims}")



    

#fields from the CSV that are relevant:  
# 68     OVERALL_STARS                  CHAR(40)                       Overall Stars Rating
# 71     FRNT_DRIV_STARS                CHAR(40)                       Frontal Impact Driver Stars Rating
# 72     FRNT_PASS_STARS                CHAR(40)                       Frontal Impact Passenger Stars Rating
# 77     OVERALL_FRNT_STARS             CHAR(40)                       Frontal Impact Overall Stars Rating
# 96     SIDE_DRIV_STARS                CHAR(40)                       Side Impact Driver Stars Rating
# 97     SIDE_PASS_STARS                CHAR(40)                       Side Impact Passenger Stars Rating
# 100    COMB_REAR_STAR                 CHAR(40)                       Side Impact Combined Rear Stars Rating
# 105    OVERALL_SIDE_STARS             CHAR(40)                       Side Impact Overall Stars Rating







