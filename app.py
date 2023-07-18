
# Financial Assistant Chatbot

### Kareem Hamoudeh

from neuralintents import GenericAssistant
import matplotlib.pyplot as plt 
import pandas as pd 
import pandas_datareader as pdr
import mplfinance as mpf 
import pickle 
import sys
import datetime as dt 
import yfinance as yf
import plotly.graph_objects as go
import pygame
import os
import random


with open('./data/portfolio.pkl', 'rb') as f:
    portfolio = pickle.load(f)



def greeting():
    print("Suuuuuuh Dude!")
    audio_directory = './data/audio/Suhs'
    audio_files = [f for f in os.listdir(audio_directory) if f.endswith('.mp3')]
    audio_file = random.choice(audio_files)
    audio_path = os.path.join(audio_directory, audio_file)
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def save_portfolio():
    with open('portfolio.pkl', 'wb') as f:
        pickle.dump(portfolio, f)

import yfinance as yf

def add_portfolio():
    ticker = input("Which are you adding: ")
    amount = input("How many shares are we adding: ")

    # Check if ticker exists using yfinance
    stock_info = yf.Ticker(ticker)

    if stock_info.info['regularMarketPrice'] is None:
        print(f"{ticker} does not exist.")
        return 

    if ticker in portfolio.keys():
        portfolio[ticker] += int(amount)
    else:
        portfolio[ticker] = int(amount)

    save_portfolio()

def remove_portfolio():
    ticker = input ("Which stock do you want to sell: ")
    amount = input ("How many shares do you want to sell: ")

    if ticker in portfolio.keys():
        if int(amount) <= portfolio[ticker]:
            portfolio[ticker] -= int(amount)
            save_portfolio
        else: 
            print("You don't have the facilities for that big man!")
    else:
        print(f"You don't own any shares of {ticker}")


def show_portfolio():
    print("Your Portfolio:")
    for ticker in portfolio.keys():
        print(f"You own {portfolio[ticker]} shares of {ticker}")


def portfolio_worth():
    today = dt.date.today()
    yesterday = today - dt.timedelta(days = 1)
    sum = 0
    for ticker in portfolio.keys():
        data = yf.download('GOOG', start=yesterday, end=yesterday)
        price = data['Close'].iloc[-1]
        sum +=price
    print(f"Based on yesterday's closing prices, your portfolio is worth {sum:.2f} USD")


def portfolio_gains():
    starting_date = input("Enter a date for comparison (YYY-MM-DD): ")
    sum_now = 0
    sum_then = 0
    try: 
        for ticker in portfolio.keys():
            data = pdr.DataReader(ticker, 'yahoo')
            price_now = data['Close'].iloc[-1]
            price_then = data.loc[data.index == starting_date]['Close'].values[0]
            sum_now += price_now
            sum_then += price_then
        
        print(f"Relative Gains: {((sum_now-sum_then)/sum_then)* 100}%")
        print(f"Absolute Gains: {sum_now-sum_then} USD")
    except IndexError:
        print("No Trading On This Day")




def plot_chart():
    while True:
        try:
            ticker = input("Choose a Ticker Symbol: ")
            starting_string = input("Choose a starting date (DD/MM/YYYY): ")

            start = dt.datetime.strptime(starting_string, "%d/%m/%Y")
            end = dt.datetime.now()

            data = yf.download(ticker, start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'))
            fig = go.Figure(data=[go.Candlestick(x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'])])

            fig.update_layout(
                title='Interactive candlestick chart',
                yaxis_title='Stock Price (USD per Shares)',
                xaxis_title='Date'
            )

            fig.show()
            
            break
        
        except ValueError:
            print("Wrong date format. Please enter the date in DD/MM/YYYY format.")
        except KeyError:
            print("Invalid ticker symbol. Please try again.")

def bye():
    print("Peace Out Broski!")
    audio_directory = './data/audio/Ahaas'
    audio_files = [f for f in os.listdir(audio_directory) if f.endswith('.mp3')]
    audio_file = random.choice(audio_files)
    audio_path = os.path.join(audio_directory, audio_file)
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    sys.exit(0)     # Delete this line when making it a web application, keep for terminal application



mappings = {
    'greeting': greeting,
    'plot_chart' : plot_chart,
    'add_portfolio': add_portfolio,
    'remove_portfolio': remove_portfolio,
    'show_portfolio': show_portfolio,
    'portfolio_worth': portfolio_worth,
    'portfolio_gains': portfolio_gains,
    'bye': bye
}
assistant = GenericAssistant('intents.json', mappings, "Jafire")

assistant.load_model()

while True:
    message = input("Go: ")
    assistant.request(message)

