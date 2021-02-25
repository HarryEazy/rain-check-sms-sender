import requests
import os
from twilio.rest import Client

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ.get("SID")
auth_token = os.environ.get("AUTH_TOKEN")

# https://www.ventusky.com - precipitation - data to test code find area with heavy rain
# https://www.latlong.net/ - find lat lon of place where it is currently raining

# FUKUOKA JP LAT LON
# lat = 33.590355
# lon = 130.401718

# LONDON UK LAT LON
# "lat": 51.507351,
# "lon": -0.127758,

weather_params = {
    "lat": 51.507351,
    "lon": -0.127758,
    "appid": os.environ.get("API_KEY"),
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()

# slice list
hourly_weather_data = weather_data["hourly"][:12]

# loop solution
will_rain = False
hourly_weather_data = hourly_weather_data
message_to_send = ""
for hour in range(0, 12):
    weather_id = int(hourly_weather_data[hour]["weather"][0]["id"])
    if weather_id < 700:
        message_to_send += f"Bring umbrella - rain @ {hour + 8} Hours\n"
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=message_to_send,
        from_="",
        to=""
    )


