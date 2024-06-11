import os
from icecream import ic
import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# The following 5 variables vary with user. Choose your own.
STOCK = os.getenv("STOCK")
COMPANY_NAME = os.getenv("COMPANY_NAME")
STOCK_PRICE_API_KEY = os.getenv("STOCK_PRICE_API_KEY")
STOCK_NEWS_API_KEY = os.getenv("STOCK_NEWS_API_KEY")
PRICE_CHANGE = int(os.getenv("PRICE_CHANGE"))
PRICE_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_PRICE_API_KEY
}

# Change in stock price
PRICE_URL = "https://www.alphavantage.co/query"
price_response = requests.get(url=PRICE_URL, params=PRICE_PARAMETERS)
price_status_code = price_response.status_code
price_data = price_response.json()["Time Series (Daily)"]

prev_2_days = list(price_data.items())[:2]
yesterday = float(prev_2_days[0][1]["4. close"])
yesterday2 = float(prev_2_days[1][1]["4. close"])
change_in_price = round((yesterday2 - yesterday), 5)
percentage_change = round(((change_in_price/yesterday) * 100), 2)
ic(percentage_change)
if change_in_price < 0:
    sign = "🔻"
else:
    sign = "🔺"
ic(yesterday)
ic(yesterday2)
ic(change_in_price)

# Get news
NEWS_URL = "https://newsapi.org/v2/everything"
PREV_DATE = prev_2_days[0][0]
ic(PREV_DATE)
NEWS_PARAMETER = {
    "q": "AMD",
    "sortBy": "popularity",
    "apiKey": STOCK_NEWS_API_KEY
}
news_response = requests.get(url=NEWS_URL, params=NEWS_PARAMETER)
news_status_code = news_response.status_code
news_data = news_response.json()
# ic(news_data)
top_header1 = news_data["articles"][0]["description"]
headline = news_data["articles"][0]["title"]
url = news_data["articles"][0]["url"]
ic(top_header1)


# Send news to phone number
# The following 4 variables vary with user. Choose your own.
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUM = os.getenv("TWILIO_NUM")
MY_NUM = os.getenv("MY_NUM")
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

if abs(change_in_price) > abs(PRICE_CHANGE):
    message = client.messages.create(body=f"AMD: {sign}{percentage_change}%\n\nHEADLINE: {headline}\n\nBRIEF: {top_header1}"
                                     f"\n\nURL: {url}",
                                     from_=TWILIO_NUM,
                                     to=MY_NUM)
    ic(message.sid)
