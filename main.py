import requests
import itertools
from twilio.rest import Client


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
api_key = "CU9I8IJU83KC8R9O"


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
TWILIO_SID = "ACccc8c3e64e70c50ed7e16f08faabd5cf"
TWILIO_AUTH_TOKEN = "aefc68ef17fec37964b50851be7df67c"


    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": api_key,
}
data = requests.get(url="https://www.alphavantage.co/query", params=parameters)
daily_data = data.json()["Time Series (Daily)"]
data_list = [value for (key, value) in daily_data.items()]
yesterday_price = data_list[0]
yesterday_closing_price = yesterday_price["4. close"]


#TODO 2. - Get the day before yesterday's closing stock price

two_days_ago_price = data_list[1]
two_days_ago_closing_price = two_days_ago_price["4. close"]

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
price_difference = float(yesterday_closing_price) - float(two_days_ago_closing_price)
price_difference = abs(price_difference)
print(price_difference)

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

percent_difference = (price_difference / float(two_days_ago_closing_price)) * 100
percent_difference = "{:.2f}".format(percent_difference)
print(percent_difference)
#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

if float(percent_difference) > 4:
   # print("Get News!")

    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
    news_api_key = "e5fe219021b04e25b089cf855bfd39fe"
    news_parameters = {
        "q": COMPANY_NAME,
        "from": '2022 - 09 - 25',
        "sortBy": "popularity",
        "apiKey": news_api_key
    }
#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    news = requests.get(url="https://newsapi.org/v2/everything", params=news_parameters)
    TSLA_news = news.json()["articles"]
    #news_data = TSLA_news["description"]
    #news_data_list = [news_value for (news_key, news_value) in TSLA_news.items()]

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    first_three_items = TSLA_news[:3]
    #print(first_three_items)

## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
   #[New item for item in list]
    formatted_articles = [f"Headline: {article['title']} \nBrief: {article['description']} "for article in first_three_items]

#TODO 9. - Send each article as a separate message via Twilio. 
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+19592712358",
            to="+2348101535488",
        )



#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

