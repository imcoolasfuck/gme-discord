# Remember to replace the Discord Token, Alpha Vantage API Key and the selected Discord Channel ID in order for this to work.
#
# V1 RELEASE
# Provides real time $GME Stock Price Data every 1 hours
# Shows Percentage Difference using +/- depending on the current price differentiating with the previous day closing price
# Uses US Time Clock and Date of when the data was pulled, this shows that the bot is using real time data.

import discord
import requests
import asyncio
from datetime import datetime, timezone, timedelta

client = discord.Client()
TOKEN = "REPLACE_DISCORD_TOKEN" # Replace with your Discord bot's token
ALPHA_VANTAGE_API_KEY = "REPLACE_ALPHA_KEY" # Replace with your Alpha Vantage API Key
TARGET_CHANNEL_ID = REPLACE_CHANNEL_ID  # Replace with your target channel ID

def get_previous_day_closing_price():
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": "GME",
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    latest_date = sorted(data["Time Series (Daily)"].keys())[-2]  # Get the second last date (previous day)
    closing_price = data["Time Series (Daily)"][latest_date]["4. close"]
    return float(closing_price)

def get_gme_stock_price():
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": "GME",
        "interval": "1min",
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    latest_data = data["Time Series (1min)"]
    latest_timestamp = list(latest_data.keys())[0]
    latest_price = latest_data[latest_timestamp]["1. open"]
    return float(latest_price)

def us_format(dt):
    return dt.strftime('%d %b %Y @ %H:%M')

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

async def send_gme_price():
    await client.wait_until_ready()
    channel = client.get_channel(TARGET_CHANNEL_ID)
    
    while not client.is_closed():
        previous_closing_price = get_previous_day_closing_price()
        current_price = get_gme_stock_price()

        percentage_difference = ((current_price - previous_closing_price) / previous_closing_price) * 100

        us_time = datetime.now(timezone(timedelta(hours=-4)))

        rocket_emoji = "🚀"  # Rocket emoji
        monkey_emoji = "🐵"  # Monkey emoji
        banana_emoji = "🍌"  # Banana emoji

        if percentage_difference >= 0:
            percentage_change_text = f"{monkey_emoji} **Percentage Change**: +{percentage_difference:.2f}% {monkey_emoji}"
        else:
            percentage_change_text = f"{monkey_emoji} **Percentage Change**: -{abs(percentage_difference):.2f}% {monkey_emoji}"

        message = f"{rocket_emoji} **Current GME Stock Price**: ${current_price:.2f} {rocket_emoji}\n" \
                  f"{percentage_change_text}\n" \
                  f"{banana_emoji} **US Update Time**: {us_format(us_time)} {banana_emoji}\n" \
                  f"\n[Superstonk on Reddit](https://reddit.com/r/Superstonk) | " \
                  f"[@Z4A on Twitter](https://twitter.com/Z4A)"

        await channel.send(message, embed=None)

        print(f"Sent message: {message}")

        await asyncio.sleep(3600)

# I don't care if this gets leeched, but please give me credit if you use this or add my code to your work etc.


client.loop.create_task(send_gme_price())
client.run(TOKEN)
