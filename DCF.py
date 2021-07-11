import pandas as pd
import yfinance as yf
import datetime
from statistics import mean

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
    FCF_NI_ratios.append(netIncome[i + 1] / cashFlow[i])
FCF_NI = min(FCF_NI_ratios)

# Prompt for Total Revenue (Can be obtained on Yahoo Finance)
totalRevenue = input("Key in Total Revenue of the format 'Current Year - 3 Current Year - 2 Current Year - 1 Analyst Estimates': ").split()

# Calculate Revenue Growth Rate
growthRates = []
for i in range(len(totalRevenue)):
    growthRates.append(totalRevenue[i + 1] / totalRevenue[i])
growthRate = min(growthRates)

# Project Total Revenue for YEARS
for i in range(YEARS):
    totalRevenue.append(totalRevenue[-1] * growthRate)

# Calculate Net Income Margins
NI_margins = []
for i in range(len(netIncome)):
    NI_margins.append(netIncome[i + 1] / totalRevenue[i])
NI_margin = 1 + min(NI_margins)

# Projected Net Income
for i in reversed(range(1, YEARS + 1)):
    netIncome.append(totalRevenue[-i] * NI_margin)

# Project Free Cash Flow
for i in reversed(range(1, YEARS + 1)):
    cashFlow.append(netIncome[-i] * FCF_NI)

# Weighted Average Cost to Capital
def weighedAverageCostToCaptial():

    # Prompt User for Interest Expense (Can be obtained from Income Statement on Yahoo Finance)
    interestExpense = int(input("Enter Interest Expense from Income Statement: "))

    # Prompt User for Current Debt (Can be obtained from Balance Sheet on Yahoo Finance)
    currentDebt = int(input("Enter Current Debt from Balance Sheet: "))

    # Prompt User for Long Term Debt (Can be obtained from Balance Sheet on Yahoo Finance)
    longTermDebt = int(input("Enter Long Term Debt from Balance Sheet: "))

    debtRate = interestExpense / (currentDebt + longTermDebt)
    
    incomebeforeTax = int(input('Enter Income Before Text from Income Statement: '))
    incomeTaxExpense = int(input('Enter Income Tax Expense from Income Statement: '))
    effectiveTaxRate = incomeTaxExpense / incomebeforeTax
    costofDebt = debtRate * (1 - effectiveTaxRate)

    def capitalAssetPricingModel():
        riskFreeRate = int(input('Enter 10 Year US Treasury Bond Rates from Yahoo Finance as Risk Free Rate: '))
        beta = int(input('Enter Beta Value from Yahoo Finance: '))
   