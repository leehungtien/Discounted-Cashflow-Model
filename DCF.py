import pandas as pd
import yfinance as yf
import datetime
from statistics import mean

# Global variable for years of projection
YEARS = 2

# Global Variable for stock margin of safety
MARGIN_OF_SAFETY = 0.1

# Prompt user for company ticker symbol
company = str(input("Please enter company's ticker symbol: "))

# Obtain Free Cash Flow Data from user (Can be obtained on Yahoo Finance)
cashFlow = list(map(lambda x: float(x), input("Key in Free Cash Flow of the format 'Current Year - 3 Current Year - 2 Current Year - 1': ").split()))

# Obtain Net Income Data from user (Can be obtained on Yahoo Finance)
netIncome = list(map(lambda x: float(x), input("Key in Net Income of the format 'Current Year - 3 Current Year - 2 Current Year - 1': ").split()))

# Calculate Free Cash Flow to Net Income Ratio
FCF_NI_ratios = []
for i in range(len(cashFlow)):
    if (i + 1 == len(cashFlow)):
        break
    FCF_NI_ratios.append(netIncome[i + 1] / cashFlow[i])
FCF_NI = mean(FCF_NI_ratios)

# Prompt for Total Revenue (Can be obtained on Yahoo Finance)
totalRevenue =  list(map(lambda x: float(x), input("Key in Total Revenue of the format 'Current Year - 3 Current Year - 2 Current Year - 1 Analyst Estimates': ").split()))

# Calculate Revenue Growth Rate
growthRates = []
for i in range(len(totalRevenue)):
    if (i + 1 == len(totalRevenue)):
        break
    growthRates.append(totalRevenue[i + 1] / totalRevenue[i])
growthRate = mean(growthRates)

# Project Total Revenue for YEARS
for i in range(YEARS):
    totalRevenue.append(totalRevenue[-1] * growthRate)

# Calculate Net Income Margins
NI_margins = []
for i in range(len(netIncome)):
    if (i + 1 == len(netIncome)):
        break
    NI_margins.append(netIncome[i + 1] / totalRevenue[i])
NI_margin = mean(NI_margins)

# Projected Net Income
for i in reversed(range(1, YEARS + 1)):
    netIncome.append(totalRevenue[-i] * NI_margin)

# Project Free Cash Flow
for i in reversed(range(1, YEARS + 1)):
    cashFlow.append(netIncome[-i] * FCF_NI)

# Weighted Average Cost to Capital
def weighedAverageCostToCapital():

    # Prompt User for Interest Expense (Can be obtained from Income Statement on Yahoo Finance)
    interestExpense = float(input("Enter Interest Expense from Income Statement: "))

    # Prompt User for Current Debt (Can be obtained from Balance Sheet on Yahoo Finance)
    currentDebt = float(input("Enter Current Debt from Balance Sheet: "))

    # Prompt User for Long Term Debt (Can be obtained from Balance Sheet on Yahoo Finance)
    longTermDebt = float(input("Enter Long Term Debt from Balance Sheet: "))

    totalDebt = currentDebt + longTermDebt

    debtRate = interestExpense / totalDebt
    
    incomebeforeTax = float(input('Enter Income Before Tax from Income Statement: '))
    incomeTaxExpense = float(input('Enter Income Tax Expense from Income Statement: '))
    effectiveTaxRate = incomeTaxExpense / incomebeforeTax
    costofDebt = debtRate * (1 - effectiveTaxRate)

    def capitalAssetPricingModel():
        riskFreeRate = float(input('Enter 10 Year US Treasury Bond Rates from Yahoo Finance as Risk Free Rate: '))
        beta = float(input('Enter Beta Value from Yahoo Finance: '))
        expectedMarketReturn = float(input('Enter the expected Market Return (10 Yr Average return of S&P500): '))
        return riskFreeRate + beta * (expectedMarketReturn - riskFreeRate)

    marketCap = float(input('Enter Market Cap of company: '))
    weightDebt = totalDebt / (totalDebt + marketCap)
    weightEquity = marketCap / (totalDebt + marketCap)
    return (weightDebt * costofDebt + weightEquity * capitalAssetPricingModel()) / 100

rateOfReturn = weighedAverageCostToCapital()
sharesOutstanding = float(input('Enter Shares Outstanding from 10K (Note if the shares are in thousands and change to match data set): '))
perpetualGrowthRate = float(input('Enter Perpetual Growth Rate in percent (2.5% is a good rate): ')) / 100
sharesOutstanding = 4601075
perpetualGrowthRate = 2.5 / 100

# Calculate the Free Cash Flow at the END of the 4th Year Projection
terminalValue = cashFlow[-1] * (1 + perpetualGrowthRate) / (rateOfReturn - perpetualGrowthRate)
cashFlow.append(terminalValue)

discountFactor = []

# Current Year cash flow info is at index 2
for i in range(2, len(cashFlow)):

    # Add Discount Factor for Terminal value which is the same as the discount factor of the last year
    if (i == (len(cashFlow) - 1)):
        discountFactor.append((1 + rateOfReturn) ** (i - 1))
        continue

    discountFactor.append((1 + rateOfReturn) ** i)

todaysValue = 0
for i in range(2, len(cashFlow)):
    todaysValue += cashFlow[i] / discountFactor[i - 2]

intrinsicValue = todaysValue / sharesOutstanding
print(f'''#############################################
INTRINISC VALUE OF {company} is: {intrinsicValue}
BUY IN PRICE SHOULD BE {(1 - MARGIN_OF_SAFETY) * intrinsicValue}''')

