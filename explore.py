import pandas as pd

df = pd.read_csv("data/2026-10-12_transaction_report.csv")
print(df.head())
print()
print(df.columns.tolist())

earnings = df[df['Transaction type'] == 'Fixed-price']
print(earnings)

connects = df[df['Transaction type'] == 'Connects']
print("\nCONNECTS SPENT:")
print(connects[['Date', 'Amount $']])

total_earned = earnings['Amount $'].sum()
total_connects = connects['Amount $'].sum()
print(f"\nTotal earned: ${total_earned}")
print(f"Total connects: ${total_connects}")

fixed = df[df['Transaction type'] == 'Fixed-price']['Amount $'].sum()
bonus = df[df['Transaction type'] == 'Bonus']['Amount $'].sum()
fees = df[df['Transaction type'] == 'Service Fee']['Amount $'].sum()
connects = df[df['Transaction type'] == 'Connects']['Amount $'].sum()

gross = fixed + bonus
net = gross + fees + connects   # fees and connects are negative, so this subtracts them

print(f"Gross earnings:  ${gross:.2f}")
print(f"Service fees:    ${fees:.2f}")
print(f"Connects spent:  ${connects:.2f}")
print(f"Net earnings:    ${net:.2f}")

import requests

url = "https://open.er-api.com/v6/latest/USD"
response = requests.get(url)
rate = response.json()["rates"]["IDR"]

print(f"\nExchange rate: 1 USD = {rate:,.2f} IDR")
print(f"Gross in IDR:   Rp {gross * rate:,.0f}")
print(f"Net in IDR:     Rp {net * rate:,.0f}")