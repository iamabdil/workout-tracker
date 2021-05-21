import requests
from datetime import datetime
import os

GENDER = "Male"
WEIGHT_KG = 81
HEIGHT_CM = 179
AGE = 22

# APP_ID = "63c48190"
APP_ID = os.environ['APP_ID']
# API_KEY = "36924c0dc3e1dea5ddc559a75ad334e0"
API_KEY = os.environ['API_KEY']

USERNAME = ""
USERNAME = os.environ['USERNAME']
PROJECT_NAME = "Workout Tracking"
SHEET_NAME = ""

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = "https://api.sheety.co/dca6ac72c87dc84251d90fc67ef39e87/workoutTracking/workouts"

exercise_text = input("Tell me which exercise you did!")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

response = requests.post(exercise_endpoint, json=params, headers=headers)
response.raise_for_status()
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

sheety_response = requests.post(sheety_endpoint, json=sheet_inputs)

# Basic Authentication
sheety_response = requests.post(
    sheety_endpoint,
    json=sheet_inputs,
    auth=(
        USERNAME,
        "abc123"
    )
)

# Bearer Token Authentication
bearer_headers = {
    "Authorization": "Bearer bnVsbDpudWxa"
}
sheety_response = requests.post(
    sheety_endpoint,
    json=sheet_inputs,
    headers=bearer_headers,
)

print(sheety_response.text)

