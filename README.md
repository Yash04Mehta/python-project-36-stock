# Stock News Alert System

A Python automation script that monitors stock price changes and sends you the latest news when significant movements occur.

## Features

- 📊 Fetches daily stock data from Alpha Vantage
- 📉 Detects price changes greater than 5%
- 📰 Retrieves top 3 relevant news articles using NewsAPI
- 📩 Sends SMS alerts via Twilio (optional)
- ⚡ Uses caching to reduce API calls and improve performance
- 🔐 Secure API key handling with environment variables

---

## Tech Stack

- Python
- requests
- requests-cache
- Twilio API
- Alpha Vantage API
- NewsAPI

---

## Installation

---
bash

git clone https://github.com/your-username/stock-news-alert.git

cd stock-news-alert

pip install -r requirements.txt

---

## Environment Variables

Create environment variables for the following:

. STOCKS_API=your_alpha_vantage_api_key

. NEWS_API=your_news_api_key

. TWILIO_ACC_ID=your_twilio_account_sid

. TWILIO_AUTH_TOKEN=your_twilio_auth_token

. SMS_FROM=your_twilio_phone_number

. SMS_TO=your_verified_phone_number

## Configuration

Inside the script:

STOCK = "TSLA"

COMPANY_NAME = "Tesla Inc"

SEND_SMS = False  # Set to True to enable SMS alerts

▶️ Usage

python main.py

## How It Works

---

Fetches daily stock prices

Calculates percentage change between last two trading days

If change ≥ 5%:

Fetches latest news articles

Sends SMS alerts (or prints to console)

---

## Example Output

TSLA: 🔺5.32%

Headline: Tesla stock surges after earnings beat

Brief: Tesla exceeded expectations...


## Notes

Alpha Vantage free tier has API limits (5 calls/minute)

NewsAPI may return limited results depending on query

SMS feature requires a verified Twilio account

## Future Improvements

Add support for multiple stocks

Schedule automatic execution (cron job)

Add email notifications

Build a web dashboard
