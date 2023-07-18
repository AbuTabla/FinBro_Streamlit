
from pymongo import MongoClient
import getpass
import yfinance as yf
import requests


# Connect to your MongoDB cluster
client = MongoClient('mongodb+srv://hamoudehkareem88:yClFOe3bRO2NMNO8@cluster92347.nk8tpbv.mongodb.net/')

db = client['cbf']
collection = db['portfolios']


## Building the User's portfolio 


portfolio = {}

# Ask the user for username and password
username = input("Please enter your username: ")
password = getpass.getpass("Please enter your password: ")

# Ask the user for input in a loop
while True:
    # Ask for the stock abbreviation
    stock = input("Please enter the stock abbreviation (or 'quit' to finish): ")

    # Check if the user wants to quit
    if stock.lower() == 'quit':
        break

    # Check if the ticker exists
    try:
        stock = stock.upper()  # Convert to uppercase
        info = yf.Ticker(stock).info
    except (KeyError, requests.exceptions.HTTPError):
        print("Invalid ticker symbol. Please try again.")
        continue

    # Ask for the number of shares
    num_shares = input("Please enter the number of shares: ")
    
    # Error checking: Make sure it's a positive integer
    try:
        num_shares = int(num_shares)
        if num_shares <= 0:
            print("Number of shares should be a positive integer.")
            continue
    except ValueError:
        print("Number of shares should be a positive integer.")
        continue

    # Add the stock and number of shares to the portfolio
    portfolio[stock] = num_shares


# Build the document to be inserted into the MongoDB collection
document = {'username': username, 'password': password, 'portfolio': portfolio}

# Insert the document into the collection
collection.insert_one(document)
