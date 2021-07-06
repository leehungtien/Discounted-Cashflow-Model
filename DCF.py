import pandas as pd
import yfinance as yf
import datetime

# Prompt user for company ticker symbol
company = str(input("Please enter company's ticker symbol: "))

# Obtain Free Cash Flow Data from user (Can be obtained on Yahoo Finance)
cashFlow = input("Key in Free Cash Flow of the form 'Y1 Y2 Y3': ").split()
print(cashFlow)