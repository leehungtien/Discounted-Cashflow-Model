import pandas as pd
import yfinance as yf
import datetime

# Global variable for years of projection
YEARS = 3

# Prompt user for company ticker symbol
company = str(input("Please enter company's ticker symbol: "))

# Obtain Free Cash Flow Data from user (Can be obtained on Yahoo Finance)
cashFlow = list(map(lambda x: int(x), input("Key in Free Cash Flow of the format 'Current Year - 3 Current Year - 2 Current Year - 1': ").split()))

# Obtain Net Income Data from user (Can be obtained on Yahoo Finance)
netIncome = list(map(lambda x: int(x), input("Key in Net Income of the format 'Current Year - 3 Current Year - 2 Current Year - 1': ").split()))

# Calculate Free Cash Flow to Net Income Ratio
FCF_NI_ratios = []
for i in range(len(cashFlow)):
    FCF_NI_ratios.append(netIncome[i] / cashFlow[i])
FCF_NI = 1 + min(FCF_NI_ratios)

# Prompt for Total Revenue (Can be obtained on Yahoo Finance)
totalRevenue = input("Key in Total Revenue of the format 'Current Year - 3 Current Year - 2 Current Year - 1 Analyst Estimates': ").split()

# Calculate Revenue Growth Rate
growthRates = []
for i in range(len(totalRevenue)):
    growthRates.append(1 - totalRevenue[i + 1] / totalRevenue[i])
growthRate = 1 + min(growthRates)

# Project Total Revenue for YEARS
for i in range(YEARS):
    totalRevenue.append(totalRevenue[-1] * growthRate)

# Calculate Net Income Margins
NI_margins = []
for i in range(len(netIncome)):
    NI_margins.append(netIncome[i] / totalRevenue[i])
NI_margin = 1 + min(NI_margins)

# Projected Net Income
for i in reversed(range(1, YEARS + 1)):
    netIncome.append(totalRevenue[-i] * NI_margin)

# Project Free Cash Flow
for i in reversed(range(1, YEARS + 1)):
    cashFlow.append(netIncome[-i] * FCF_NI)
