import requests
import time
from bs4 import BeautifulSoup
import json
import random


username = "your_opensky_username"
pw = "your_opensky_password"


def flight_locator():
    url = f"https://{username}:{pw}@opensky-network.org/api/states/all"
    lga_params = {
        "lamin": 40.651201,
        "lomin": -73.987562,
        "lamax": 40.675291,
        "lomax": -73.960080,
        "extended": 1
    }

    response = requests.get(url, params=lga_params)
    callsign = response.json()["states"][0][1]
    return callsign


def get_html(callsign):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Agency/93.8.2357.5",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.",
        "Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Viewer/99.9.8853.8",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.3"
    ]
    user_agent = random.choice(user_agents)
    headers = {'User-Agent': user_agent}
    response = requests.get(f"https://en.spotterlead.net/flights/{callsign}/", headers=headers)
    with open("site.html", mode="w") as file:
        file.write(response.text)
    with open("site.html", mode="r") as file:
        contents = file.read()
    soup = BeautifulSoup(contents, "html.parser")
    data = soup.find_all(type="application/ld+json")

    dict = data[1]
    reg_number = json.loads(dict.text)["aircraft"].rsplit(" ", 1)[1]
    plane_model = json.loads(dict.text)["aircraft"].rsplit(" ", 1)[0]
    print(f'Aircraft Model: {plane_model}\nRegistration: {reg_number}')
    print(f'Airline: {json.loads(dict.text)["provider"]["name"]}')

    # error handling for times when Spotterlead mixes up the arrival and departure airports
    if json.loads(dict.text)["departureAirport"]["iataCode"] == "LGA":
        print(f'Departing Airport: {json.loads(dict.text)["arrivalAirport"]["iataCode"]} - {json.loads(dict.text)["arrivalAirport"]["name"]}')
    else:
        print(f'Departing Airport: {json.loads(dict.text)["departureAirport"]["iataCode"]} - {json.loads(dict.text)["departureAirport"]["name"]}')


running = True
flight_number = ""
LAST_FLIGHT = ""
while running:
    try:
        flight_number = flight_locator()
        if flight_number != LAST_FLIGHT:
            print(f'Callsign: {flight_number}')
            LAST_FLIGHT = flight_number
        else:
            print("     same flight as before")
            time.sleep(10)
            continue
    except:
        print("     No flights in zone")
        time.sleep(4)
        print("     Re-running now")
    else:
        get_html(flight_number)
        time.sleep(10)

