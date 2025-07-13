# ✈️ Flight Price Tracker (AMS → CPT)

A Python script that tracks round-trip flight prices from **Amsterdam (AMS)** to **Cape Town (CPT)** using the Kiwi.com API. It sends SMS alerts via Twilio if a price drops below your threshold and logs prices daily to a CSV file.

## 🔧 Features

- Monitors return flights between specific date ranges.
- Sends SMS alerts when a price is below the defined threshold.
- Logs daily price data to `prices.csv`.
- Supports daily automation with `launchctl` on macOS.

## 📁 File Overview

| File | Description |
|------|-------------|
| `tracker.py` | Core script that checks flights, sends alerts, logs prices |
| `config.py` | Stores trip settings, currency, and CSV path |
| `private.env` | Stores API keys and phone numbers (uses placeholder values in this public repo) |

## 🔑 Example `.env` Configuration

Replace these placeholders with your own credentials when running locally:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+12345678900
RECIPIENT_PHONE_NUMBER=+12345678900
RAPIDAPI_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
