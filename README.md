# 🌕 Full Moon Notifier

A simple Python automation script that checks the lunar phase and sends an email notification one day before a full moon.

---

## ✨ Features

- Fetches real-time moon phase data from an external API
- Detects upcoming full moon (1 day before peak)
- Sends email notification automatically
- Prevents duplicate notifications within a cycle
- Logs execution status locally for debugging

---

## ⚙️ How it works

1. The script gets current and upcoming lunar data using an API
2. It compares moon phase values across 3 days:
   - today
   - tomorrow
   - day after tomorrow
3. If tomorrow is a full moon and has the peak illumination:
   - an email is sent
4. The script stores the last sent date to avoid duplicates

---

## 📦 Tech Stack

- Python 3
- Requests
- SMTP (email sending)
- python-dotenv
- External Moon Phase API

---

## 🔐 Environment Variables

Create a `.env` file in the project root and add the following variables:

```env
API_KEY=your_api_key

# Your location (set your own coordinates)
LOCATION_LATITUDE=your_latitude
LOCATION_LONGITUDE=your_longitude

# Email configuration
MY_EMAIL=your_email@gmail.com
MY_EMAIL_PASSWORD=your_app_password
DESTINATION_EMAIL=receiver_email@gmail.com

# Custom notification message
MSG=your_custom_notification_message
