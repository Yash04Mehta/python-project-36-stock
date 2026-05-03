import requests
import requests_cache
from twilio.rest import Client
import os

# ---------------- CONFIG ----------------

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_URL = "https://www.alphavantage.co/query"
NEWS_URL = "https://newsapi.org/v2/everything"

ACCOUNT_SID = os.getenv("TWILIO_ACC_ID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

SEND_SMS = False


# ---------------- CACHE SETUP ----------------

requests_cache.install_cache(
    "stock_news_cache",
    expire_after=3600
)


# ---------------- STOCK DATA FUNCTION ----------------

def get_stock_prices():

    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": os.getenv("STOCKS_API"),
    }

    response = requests.get(STOCK_URL, params=stock_params)
    response.raise_for_status()

    data = response.json()
    print(data)  # DEBUG

    if "Time Series (Daily)" not in data:
        raise Exception("API Error: ", data)

    daily_data = data["Time Series (Daily)"]

    dates = list(daily_data.keys())

    yesterday = dates[0]
    previous_day = dates[1]

    yesterday_close = float(daily_data[yesterday]["4. close"])
    previous_close = float(daily_data[previous_day]["4. close"])

    return yesterday, previous_close, yesterday_close


# ---------------- PRICE CHANGE FUNCTION ----------------

def check_price_change(previous_close, yesterday_close):

    difference = yesterday_close - previous_close
    percent_change = abs(difference / previous_close) * 100

    if percent_change >= 5:

        if difference > 0:
            return "🔺", round(percent_change, 2)

        else:
            return "🔻", round(percent_change, 2)

    return None, None


# ---------------- NEWS FETCH FUNCTION ----------------

def get_news(yesterday):

    news_params = {
        "qInTitle": COMPANY_NAME,
        "from": yesterday,
        "sortBy": "publishedAt",
        "apiKey": os.getenv("NEWS_API")
    }

    response = requests.get(NEWS_URL, params=news_params)
    response.raise_for_status()

    print("News cached:", response.from_cache)

    return response.json()["articles"][:3]


# ---------------- SMS FUNCTION ----------------

def send_sms(symbol, percent, articles):

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    for article in articles:

        headline = article["title"]
        brief = article["description"]

        body = (
            f"{STOCK}: {symbol}{percent}%\n"
            f"Headline: {headline}\n"
            f"Brief: {brief}"
        )

        if SEND_SMS:

            message = client.messages.create(
                body=body,
                from_= os.getenv("SMS_FROM"),
                to = os.getenv("SMS_TO")
            )

            print(message.sid)

        else:
            print(body)



# ---------------- MAIN PROGRAM ----------------

def main():

    yesterday, previous_close, yesterday_close = get_stock_prices()

    symbol, percent = check_price_change(previous_close, yesterday_close)

    if symbol:

        articles = get_news(yesterday)

        send_sms(symbol, percent, articles)

    else:

        print("Price change < 5%. No news fetched.")


# ---------------- RUN SCRIPT ----------------
main()
