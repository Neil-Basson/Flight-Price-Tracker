import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client
import csv
from datetime import datetime
from config import (
    ORIGIN, DESTINATION, CURRENCY, ALERT_PRICE,
    DEPARTURE_DATE_FROM, DEPARTURE_DATE_TO,
    RETURN_DATE_FROM, RETURN_DATE_TO, CSV_PATH
)

load_dotenv()

def send_sms_alert(message_body):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
    recipient_number = os.getenv("RECIPIENT_PHONE_NUMBER")

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message_body,
        from_=twilio_number,
        to=recipient_number
    )
    print(f"✅ SMS sent: {message.sid}")


def search_flights():
    url = "https://kiwi-com-cheap-flights.p.rapidapi.com/round-trip"

    querystring = {
        "source": "City:amsterdam_nl",         # or Country:nl
        "destination": "City:cape-town_za",    # or Country:za
        "currency": "eur",
        "locale": "en",
        "adults": "1",
        "children": "0",
        "infants": "0",
        "cabinClass": "ECONOMY",
        "sortBy": "PRICE",
        "sortOrder": "ASCENDING",
        "limit": "3",
        "outboundDepartureDateStart": "2025-08-01T00:00:00",
        "outboundDepartureDateEnd": "2025-08-15T00:00:00",
        "inboundDepartureDateStart": "2025-08-15T00:00:00",
        "inboundDepartureDateEnd": "2025-09-15T00:00:00"
        }

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "kiwi-com-cheap-flights.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        print(f"❌ Failed to fetch flights: {response.status_code}")
        return

    flights = response.json().get("data", [])
    if not flights:
        print("No flights found.")
        return

    flight = flights[0]
    price = flight.get("price")
    route = flight.get("route", [])
    departure = route[0].get("local_departure")
    return_flight = route[-1].get("local_arrival")

    log_price(price, departure)

    if price <= ALERT_PRICE:
        message = (
            f"✈️ Round-trip deal! €{price}\n"
            f"{route[0].get('cityFrom')} → {route[0].get('cityTo')}\n"
            f"Departure: {departure}\n"
            f"Return: {return_flight}\n"
            f"Duration: {flight.get('fly_duration')}"
        )
        send_sms_alert(message)
    else:
        print(f"No alert. Cheapest round-trip flight today: €{price}")


def log_price(price, departure_date):
    file_exists = os.path.isfile(CSV_PATH)
    with open(CSV_PATH, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Timestamp", "Departure_Date", "Price"])
        writer.writerow([datetime.now(), departure_date, price])


if __name__ == "__main__":
    search_flights()
