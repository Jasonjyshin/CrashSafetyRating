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
    return results #return full results to access both description and ID



#Select vehicle model to see the available trims and their vehicleID
model_selection = input("Select a model to view trim levels: ").upper()
trim_data = vehicle_trims(year_input, brand_input, model_selection)
if model_selection not in brand_year_models:
    print("Invalid model selection")
else:
    #display available trims with indices
    print(f"\nAvailable trims for a {year_input} {brand_input} {model_selection} are: ")
    for i, trim in enumerate(trim_data, 1):
        print(f"{i}. {trim['VehicleDescription']}")

    while True:
        try:
            trim_choice = int(input("\nSelect trim number: ")) - 1 
            if 0 <= trim_choice < len(trim_data):
                selected_trim = trim_data[trim_choice]
                vehicle_id = selected_trim['VehicleId']
                print(f"\nSelected: {selected_trim['VehicleDescription']}")
                break
            else:
                print("Invalid selection. Please choose a number from the list")
        except ValueError:
            print("Please enter a valid number")


#NEXT STEPS - Below is the output so far. Next function should be requesting safety rating using VehicleID selected below. 
# Select a model to view trim levels: rx 350

#Available trims for a 2021 lexus RX 350 are:
#1. 2021 Lexus RX 350 SUV FWD Later Release
#2. 2021 Lexus RX 350 SUV AWD Later Release
#3. 2021 Lexus RX 350 SUV AWD Early Release
#4. 2021 Lexus RX 350 SUV FWD Early Release

#Select trim number: 2

#Selected: 2021 Lexus RX 350 SUV AWD Later Release


    

#fields from the CSV that are relevant:  
# 68     OVERALL_STARS                  CHAR(40)                       Overall Stars Rating
# 71     FRNT_DRIV_STARS                CHAR(40)                       Frontal Impact Driver Stars Rating
# 72     FRNT_PASS_STARS                CHAR(40)                       Frontal Impact Passenger Stars Rating
# 77     OVERALL_FRNT_STARS             CHAR(40)                       Frontal Impact Overall Stars Rating
# 96     SIDE_DRIV_STARS                CHAR(40)                       Side Impact Driver Stars Rating
# 97     SIDE_PASS_STARS                CHAR(40)                       Side Impact Passenger Stars Rating
# 100    COMB_REAR_STAR                 CHAR(40)                       Side Impact Combined Rear Stars Rating
# 105    OVERALL_SIDE_STARS             CHAR(40)                       Side Impact Overall Stars Rating







