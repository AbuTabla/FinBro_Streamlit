# Import streamlit
import streamlit as st
import os
from neuralintents import GenericAssistant
import matplotlib.pyplot as plt 
import pandas as pd 
import pandas_datareader as pdr
import mplfinance as mpf 
import pickle 
import datetime as dt 

st.title("Financial Assistant Chatbot")

portfolio_path = './data/portfolio.pkl'
portfolio = {}
if os.path.exists(portfolio_path):
    with open(portfolio_path, 'rb') as f:
        portfolio = pickle.load(f)

def greeting():
    st.write("Suuuuuuh Dude!")

def save_portfolio():
    with open('portfolio.pkl', 'wb') as f:
        pickle.dump(portfolio, f)

def add_portfolio(ticker, amount):
    if ticker in portfolio.keys():
        portfolio[ticker] += int(amount)
    else:
        portfolio[ticker] = int(amount)

    save_portfolio()

def remove_portfolio(ticker, amount):
    if ticker in portfolio.keys():
        if int(amount) <= portfolio[ticker]:
            portfolio[ticker] -= int(amount)
            save_portfolio()
        else: 
            st.write("You don't have the facilities for that big man!")
    else:
        st.write(f"You don't own any shares of {ticker}")

def show_portfolio():
    st.write("Your Portfolio:")
    for ticker in portfolio.keys():
        st.write(f"You own {portfolio[ticker]} shares of {ticker}")

def portfolio_worth():
    sum = 0 
    for ticker in portfolio.keys():
        data = pdr.Datareader(ticker, 'yahoo')
        price = data['Close'].iloc[-1]
        sum += price 

    st.write(f"Your portfolio is worth {sum} USD")

def portfolio_gains(starting_date):
    sum_now = 0
    sum_then = 0

    try: 
        for ticker in portfolio.keys():
            data = pdr.DataReader(ticker, 'yahoo')
            price_now = data['Close'].iloc[-1]
            price_then = data.loc[data.index == starting_date]['Close'].values[0]
            sum_now += price_now
            sum_then += price_then
        
        st.write(f"Relative Gains: {((sum_now-sum_then)/sum_then)* 100}%")
        st.write(f"Absolute Gains: {sum_now-sum_then} USD")
    except IndexError:
        st.write("No Trading On This Day")

import yfinance as yf

def plot_chart(ticker, starting_string):
    plt.style.use('dark_background')

    start = dt.datetime.strptime(starting_string, "%d/%m/%Y")
    end = dt.datetime.now()

    data = yf.download(ticker, start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'))

    colors = mpf.make_marketcolors(up = '#00ff00', down = '#ff0000', wick = 'inherit', edge = 'inherit', volume = 'in')
    mpf_style = mpf.make_mpf_style(base_mpf_style = 'nightclouds', marketcolors = colors)
    mpf.plot(data, type = 'candle', style = mpf_style, volume = True)
    st.pyplot(plt)

mappings = {
    'greeting': greeting,
    'plot_chart' : plot_chart,
    'add_portfolio': add_portfolio,
    'remove_portfolio': remove_portfolio,
    'show_portfolio': show_portfolio,
    'portfolio_worth': portfolio_worth,
    'portfolio_gains': portfolio_gains,
}
assistant = GenericAssistant('intents.json', mappings, "Jafire")

assistant.load_model()

user_message = st.text_input("Your message:")
assistant.request(user_message)
