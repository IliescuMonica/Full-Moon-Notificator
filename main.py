# ---------------- IMPORT LIBRARIES ---------------- #

import requests
from datetime import datetime, timedelta
import os
import smtplib
from dotenv import load_dotenv

# ----------------LOAD DOTENV ---------------- #

load_dotenv()

# ---------------- CONFIGURATION & INITIALIZATION ---------------- #

LAST_SENT_FILE = "last_sent.txt"
API_KEY = os.getenv("API_KEY")
MOON_PHASE_URL = "https://astroapi.byhrast.com/moon.php?"
LOCATION_LATITUDE = os.getenv("LOCATION_LATITUDE")
LOCATION_LONGITUDE = os.getenv("LOCATION_LONGITUDE")
dt = datetime.now()
today = dt
tomorrow = dt + timedelta(days=1)
day_after = tomorrow + timedelta(days=1)
TIME_ZONE_TOMORROW = f"Europe%2FBucharest&date={tomorrow.day}%2F{tomorrow.month}%2F{tomorrow.year}&time=8:00"
TIME_ZONE_TODAY = f"Europe%2FBucharest&date={today.day}%2F{today.month}%2F{today.year}&time=8:00"
TIME_ZONE_DAY_AFTER = f"Europe%2FBucharest&date={day_after.day}%2F{day_after.month}%2F{day_after.year}&time=8:00"
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}

# ---------------- CHECK IF ALREADY SENT ---------------- #

def already_sent_this_cycle():
    if not os.path.exists(LAST_SENT_FILE):
        return False

    with open(LAST_SENT_FILE, "r") as f:
        last_str = f.read().strip()

    if not last_str:
        return False

    last = datetime.strptime(last_str, "%Y-%m-%d")
    now = datetime.now()

    return (now - last).days < 10

# ---------------- MARK SENT ---------------- #

def mark_sent_this_cycle():
    now = datetime.now()
    current = f"{now.year}-{now.month}-{now.day}"

    with open(LAST_SENT_FILE, "w") as f:
        f.write(current)

# ---------------- MOON CHECK ---------------- #

def is_tomorrow_full_moon():
    tomorrow_response = requests.get(f"{MOON_PHASE_URL}key={API_KEY}&latitude={LOCATION_LATITUDE}&longitude={LOCATION_LONGITUDE}&timezone={TIME_ZONE_TOMORROW}",headers=header)
    tomorrow_response.raise_for_status()
    tomorrow_data = tomorrow_response.json()
    tomorrow_moon_phase = tomorrow_data["phase"]
    tomorrow_moon_fraction = tomorrow_data["phase_details"]["fraction"]

    today_response = requests.get(f"{MOON_PHASE_URL}key={API_KEY}&latitude={LOCATION_LATITUDE}&longitude={LOCATION_LONGITUDE}&timezone={TIME_ZONE_TODAY}",headers=header)
    today_response.raise_for_status()
    today_data = today_response.json()
    today_moon_fraction = today_data["phase_details"]["fraction"]

    day_after_response = requests.get(f"{MOON_PHASE_URL}key={API_KEY}&latitude={LOCATION_LATITUDE}&longitude={LOCATION_LONGITUDE}&timezone={TIME_ZONE_DAY_AFTER}",headers=header)
    day_after_response.raise_for_status()
    day_after_data = day_after_response.json()
    day_after_moon_fraction = day_after_data["phase_details"]["fraction"]

    if (
            tomorrow_moon_phase == "Full Moon"
            and tomorrow_moon_fraction > today_moon_fraction
            and tomorrow_moon_fraction > day_after_moon_fraction
            and tomorrow_moon_fraction > 0.99
    ):
        return True
    else:
        return False

# ---------------- EMAIL INFO ---------------- #

my_email = os.getenv("MY_EMAIL")
password = os.getenv("MY_EMAIL_PASSWORD")
destination_email = os.getenv("DESTINATION_EMAIL")
msg = os.getenv("MSG")

# ---------------- MAIN ---------------- #

is_full_moon = is_tomorrow_full_moon()
already_sent = already_sent_this_cycle()

email_sent = False

if is_full_moon and not already_sent:
    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=destination_email,
            msg=msg
        )
    mark_sent_this_cycle()
    email_sent = True

else:
    with open("task_log.txt", "a") as f:
        f.write(f"Script executed successfully at {datetime.now()}\n")




