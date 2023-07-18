# Streamlit Version of Financial Assistant Chatbot
# Kareem Hamoudeh

from neuralintents import GenericAssistant
import pickle
import os
import random
import base64
import streamlit as st
import datetime as dt
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

portfolio_path = "./data/portfolio.pkl"
today = dt.date.today()
yesterday = today - dt.timedelta(days = 1)

def load_portfolio():
    with open(portfolio_path, 'rb') as f:
        return pickle.load(f)

portfolio = load_portfolio()

def check_available(asset: str) -> bool:
    """
    Checks if an asset is available via the Yahoo Finance API.
    """
    info = yf.Ticker(asset).history(
        period='7d',
        interval='1d')
    # return == period value for more precise check but may
    # need more complex handling to take into account non-
    # trading days, holidays, etc.
    return len(info) > 0

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def greeting():
    st.write("Suuuuuuh Dude!")
    audio_directory = './data/audio/Suhs'
    audio_files = [f for f in os.listdir(audio_directory) if f.endswith('.mp3')]
    audio_file = random.choice(audio_files)
    audio_path = os.path.join(audio_directory, audio_file)
    autoplay_audio(audio_path)

def save_portfolio():
    with open(portfolio_path, 'wb') as f:
        pickle.dump(portfolio, f)


def add_portfolio():
    ticker = st.text_input("Enter the stock ticker that you would like to buy: ")
    amount = st.number_input("Enter how many shares you would like to buy: ", min_value=1, step=1)
    
    ticker = ticker.upper()

    if st.button('Execute'):   # Wait for the user to click this button before proceeding
        if not check_available(ticker):
            st.write("Invalid ticker symbol, please try again.")
        elif amount <= 0:
            st.write("Number of shares should be a positive integer.")
        else:
            if ticker in portfolio.keys():
                portfolio[ticker] += int(amount)
            else:
                portfolio[ticker] = int(amount)
            save_portfolio()
            show_portfolio()

def remove_portfolio():
    ticker = st.text_input("Enter the stock ticker that you would like to sell: ")
    amount = st.number_input("Enter how many shares you would like to sell: ", min_value=1, step=1)

    if st.button('Execute'):  # Wait for the user to click this button before proceeding
        if ticker:
            ticker = ticker.upper()  # Convert the ticker to uppercase
            if ticker in portfolio.keys():
                if amount <= portfolio[ticker]:
                    portfolio[ticker] -= amount
                    if portfolio[ticker] <= 0:
                        del portfolio[ticker]
                    save_portfolio()
                    show_portfolio()
                else: 
                    st.write("You don't have the facilities for that big man!")
            else:
                st.write(f"You don't own any shares of {ticker}")
        else:
            st.write("Please enter a valid ticker.")


def show_portfolio():
    st.write("Your Portfolio:")
    for ticker in portfolio.keys():
        st.write(f"You own {portfolio[ticker]} shares of {ticker}")

def portfolio_worth():
    total_value = 0
    for ticker, shares in portfolio.items():  # Get both the ticker and the number of shares
        data = yf.download(ticker, start=yesterday, end=yesterday)
        price = data['Close'].iloc[-1]
        total_value += price * shares  # Multiply the price by the number of shares
    st.write(f"Based on yesterday's closing prices, your portfolio is worth {total_value:.2f} USD")



def portfolio_gains():
    starting_date = pd.to_datetime(st.date_input("Enter a date for comparison: "))
    total_value_now = 0
    total_value_then = 0
    try:
        for ticker, shares in portfolio.items():
            data = yf.download(ticker, start=starting_date, end=yesterday)
            price_now = data['Close'].iloc[-1]
            price_then = data.loc[data.index == starting_date]['Close'].values[0]
            total_value_now += price_now * shares
            total_value_then += price_then * shares

        st.write(f"Relative Gains: {((total_value_now - total_value_then) / total_value_then) * 100:.2f}%")
        st.write(f"Absolute Gains: {total_value_now - total_value_then:.2f} USD")
    except IndexError:
        st.write("No Trading On This Day")




def plot_chart():
    ticker = st.text_input("Choose a Ticker Symbol:")
    starting_string = st.date_input("Choose a starting date", value=dt.date.today())
    if ticker and starting_string:
        try:
            start = starting_string
            end = dt.datetime.now()

            data = yf.download(ticker, start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'))

            if data.empty:
                st.write("Invalid ticker symbol or date. Please double check the ticker and make sure the date is not today.")
                return 

            fig = go.Figure(data=[go.Candlestick(x=data.index,
                                                 open=data['Open'],
                                                 high=data['High'],
                                                 low=data['Low'],
                                                 close=data['Close'])])

            fig.update_layout(
                title=(f'{ticker} Interactive Chart'),
                yaxis_title='Stock Price (USD per Shares)',
                xaxis_title='Date'
            )

            st.plotly_chart(fig)
        
        except ValueError:
            st.write("Wrong date format. Please enter the date in DD/MM/YYYY format.")


def bye():
    st.write("Peace Out Broski!")
    audio_directory = './data/audio/Ahaas'
    audio_files = [f for f in os.listdir(audio_directory) if f.endswith('.mp3')]
    audio_file = random.choice(audio_files)
    audio_path = os.path.join(audio_directory, audio_file)
    autoplay_audio(audio_path)


# Define assistant
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
assistant.load_model('Jafire','./data/ML_Models/')

# Define Streamlit layout
st.title('Financial Assistant Chatbot')
message = st.text_input("Enter your command:", value="", max_chars=None, key=None, type='default')
response = assistant.request(message)
st.write(response)
