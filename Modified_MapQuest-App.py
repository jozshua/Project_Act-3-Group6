import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
weather_api_key = "TLulG8sBnteXPQR6UYbtbjW2LFoHAjhL"  # Replace with your actual weather API key

def display_route(json_data, units, orig, dest):
    print("=============================================")
    print(f"Directions from {orig} to {dest}")
    print(f"Trip Duration:   {json_data['route']['formattedTime']}")
    
    distance_units = "Kilometers" if units == "kilometers" else "Miles"
    distance = json_data['route']['distance'] * 1.61 if units == "kilometers" else json_data['route']['distance']
    print(f"{distance_units}:      {str('{:.2f}'.format(distance))}")
    
    print("=============================================")
    for each in json_data['route']['legs'][0]['maneuvers']:
        distance = each['distance'] * 1.61 if units == "kilometers" else each['distance']
        print(f"{each['narrative']} ({str('{:.2f}'.format(distance))} {distance_units.lower()})")
    print("=============================================\n")

def estimate_fuel_cost(distance, fuel_efficiency, fuel_price_per_unit):
    fuel_cost = (distance / fuel_efficiency) * fuel_price_per_unit
    return fuel_cost

while True:
    orig = input("Starting Location: ")
    if orig.lower() == "quit" or orig.lower() == "q":
        break
    
    dest = input("Destination: ")
    if dest.lower() == "quit" or dest.lower() == "q":
        break
    
    units = input("Select units (miles/kilometers): ").lower()
    if units not in ["miles", "kilometers"]:
        print("Invalid unit selection. Defaulting to miles.")
        units = "miles"

    # Fetch the route information
    url = main_api + urllib.parse.urlencode({"key": weather_api_key, "from": orig, "to": dest})
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]
    
    if json_status == 0:
        print(f"API Status: {json_status} = A successful route call.\n")
        display_route(json_data, units, orig, dest)  # Pass orig and dest to display_route

        # Estimate fuel cost
        distance = json_data['route']['distance'] * 1.61 if units == "kilometers" else json_data['route']['distance']
        fuel_efficiency = float(input("Enter your vehicle's fuel efficiency (miles per gallon or kilometers per liter): "))
        fuel_price_per_unit = float(input("Enter the current fuel price per unit: "))

        fuel_cost = estimate_fuel_cost(distance, fuel_efficiency, fuel_price_per_unit)
        print(f"Estimated Fuel Cost: ${fuel_cost:.2f}\n")

    else:
        print(f"API Status: {json_status} = Unable to retrieve route information.\n")
