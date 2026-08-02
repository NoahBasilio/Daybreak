from dotenv import load_dotenv
import os
import requests
import json
import datetime


load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

clear_command = "cls" if os.name == "nt" else "clear"




def validCity(city, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return "valid"
    elif response.status_code == 401:
        return "bad_key"
    elif response.status_code == 404:
        return "bad_city"
    else:
        return "unknown_error"


script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config.json")

if os.path.exists(config_path):
    with open(config_path, "r") as f:
        config = json.load(f)
    user_city = config["city"]
    user_api_key = config["api_key"]
    user_name = config["user_name"]
    user_units = config["user_units"]
else:
    os.system(clear_command)
    print("Welcome to Daybreak! Let's get you set up.\n---------------------------------------------\n")
    print("Please create a FREE API key on OpenWeatherMap and paste it in here! It is required to use this app.\n")
    user_api_key = input("What is your API key? ")

    os.system(clear_command)

    city_exists = False
    while not city_exists:
        user_city = input("What city do you live in? ")
        result = validCity(user_city, user_api_key)
        print("Checking city...")
        
        if result == "valid":
            city_exists = True
            print("\nThat is a valid city! (Press enter to continue)\n")
            input()
        elif result == "bad_key":
            print("\nYour API key seems invalid. Please check it and restart Daybreak.\n")
            break
        elif result == "bad_city":
            print("\nThat isn't a valid city, try again.\n")
        else:
            print("\nSomething went wrong, please try again.\n")
    units_set = False
    while not units_set:
        os.system(clear_command)
        user_units = input("Do you use Imperial units (°F), or Metric (°C)? (imperial/metric) ").lower()
        if user_units == "imperial" or user_units == "metric":
            units_set = True
        else:
            print("Try again, that isn't a unit.\n")
    os.system(clear_command)
    user_name = input("What is your name? (Or what we should call you?) ")
    print("\n---------------------------------------------\nThank you! Configuration for Daybreak now complete. Enjoy! (Press enter to continue)\n---------------------------------------------\n")
    input()

config = {
    "city": user_city,
    "api_key": user_api_key,
    "user_name": user_name,
    "user_units": user_units
}

with open(config_path, "w") as f:
    json.dump(config, f)

def displayMenu(city, api_key, user_name, user_units):

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": user_units}
    
    response = requests.get(url, params=params)
    data = response.json()
    # print(data) shows all the data we can work with here, obviously wont use everything


    now = datetime.datetime.now()
    hour = now.hour

    if hour < 12:
        greeting = "Good morning"
    elif hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    temp = round(data["main"]["temp"])
    high = round(data["main"]["temp_max"])
    low = round(data["main"]["temp_min"])
    condition = data["weather"][0]["description"]

    os.system(clear_command)
    print("===========================")
    print(f"{greeting}, {user_name}!")
    print("===========================")

    # Weather
    print(f"\n📍 Weather ({user_city})\n")
    if user_units == "imperial":
        print(f"Currently: {temp}°F, {condition.title()}")
        print(f"High: {high}°F     Low: {low}°F")
    else:
        print(f"Currently: {temp}°C, {condition.title()}")
        print(f"High: {high}°C     Low: {low}°C")

    print("\n\n===========================")
    print(f"Have a great day, {user_name}!")
    print("===========================")

displayMenu(user_city, user_api_key, user_name, user_units)

