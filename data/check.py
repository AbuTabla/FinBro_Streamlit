import pickle

with open('portfolio.pkl', 'rb') as f:
    portfolio = pickle.load(f)

print(portfolio)