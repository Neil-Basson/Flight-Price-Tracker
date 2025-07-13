#  Flight Price Tracker (AMS → CPT)

A Python script that tracks round-trip flight prices from **Amsterdam (AMS)** to **Cape Town (CPT)** using the Kiwi.com API. It sends SMS alerts via Twilio if a price drops below your threshold and logs prices daily to a CSV file.

## Features

- Monitors return flights between specific date ranges.
- Sends SMS alerts when a price is below the defined threshold.
- Logs daily price data to `prices.csv`.
- Supports daily automation with `launchctl` on macOS.

## File Overview

| File | Description |
|------|-------------|
| `tracker.py` | Core script that checks flights, sends alerts, logs prices |
| `config.py` | Stores trip settings, currency, and CSV path |
| `private.env` | Stores API keys and phone numbers (uses placeholder values in this public repo) |

## Example `.env` Configuration

Replace these placeholders with your own credentials when running locally:

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+12345678900
RECIPIENT_PHONE_NUMBER=+12345678900
RAPIDAPI_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
## Configuration (config.py)
```
ORIGIN = "City:amsterdam_nl"
DESTINATION = "City:cape-town_za"
CURRENCY = "EUR"
ALERT_PRICE = 750

DEPARTURE_DATE_FROM = "2025-08-01"
DEPARTURE_DATE_TO = "2025-08-15"
RETURN_DATE_FROM = "2025-08-15"
RETURN_DATE_TO = "2025-09-15"
CSV_PATH = "prices.csv"
```
## Scheduling on macOS

To run the tracker script automatically every day, use `launchctl` to create a scheduled task:

### Step 1: Create the LaunchAgent file

Create a file at this path (replace `neilbasson` with your Mac username):

```bash
nano ~/Library/LaunchAgents/com.neil.flighttracker.plist
```
paste the following
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" 
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.neil.flighttracker</string>

  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>/Users/neilbasson/Flight Price Tracker/tracker.py</string>
  </array>

  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>
    <integer>10</integer>
    <key>Minute</key>
    <integer>0</integer>
  </dict>

  <key>StandardOutPath</key>
  <string>/tmp/flighttracker.out</string>
  <key>StandardErrorPath</key>
  <string>/tmp/flighttracker.err</string>
</dict>
</plist>
```
Save with Control + O, press Enter, then exit with Control + X.
### Step 2: Load the schedule
Run this to load the LaunchAgent:
```
launchctl load ~/Library/LaunchAgents/com.neil.flighttracker.plist
```
### Step 3: Check it loaded
Verify it's scheduled:
```
launchctl list | grep flighttracker
```
You should see something like: 
```
diff
-       0       com.neil.flighttracker
```
The script will now run automatically at 10:00 every day.




