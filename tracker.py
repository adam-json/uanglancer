import os
import requests
import pandas as pd
import glob
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))

downloads_dir = os.path.expanduser("~/Downloads")
print(f"Downloads folder: {downloads_dir}")

pattern = os.path.join(downloads_dir, "*transaction_report.csv")
files = glob.glob(pattern)
print(f"Found {len(files)} report(s) in Downloads")

data_dir = os.path.join(script_dir, "data")
os.makedirs(data_dir, exist_ok=True)

if files:
    latest = max(files)
    print(f"Newest in Downloads: {os.path.basename(latest)}")
    csv_path = os.path.join(data_dir, os.path.basename(latest))
    
    if os.path.exists(csv_path):
        print(f"Already in data/, using it")
    else:
        for old_file in glob.glob(os.path.join(data_dir, "*transaction_report.csv")):
            os.remove(old_file)
            print(f"Removed old: {os.path.basename(old_file)}")
        shutil.move(latest, csv_path)
        print(f"Moved to: {csv_path}")
else:
    existing = glob.glob(os.path.join(data_dir, "*transaction_report.csv"))
    if not existing:
        print("No report found anywhere. Export from Upwork first.")
        exit()
    csv_path = max(existing)
    print(f"No new report in Downloads. Using existing: {os.path.basename(csv_path)}")
df = pd.read_csv(csv_path)
print(f"Loaded {len(df)} rows and {len(df.columns)} columns")

gross = df[df['Transaction type'].isin(['Fixed-price', 'Bonus'])]['Amount $'].sum()
fees = df[df['Transaction type'] == 'Service Fee']['Amount $'].sum()
connects = df[df['Transaction type'] == 'Connects']['Amount $'].sum()
net = gross + fees + connects   

print(f"Gross:    ${gross:.2f}")
print(f"Fees:     ${fees:.2f}")
print(f"Connects: ${connects:.2f}")
print(f"Net:      ${net:.2f}")

url = "https://open.er-api.com/v6/latest/USD"
response = requests.get(url)
rate = response.json()["rates"]["IDR"]

print(f"\nRate: 1 USD = {rate:,.2f} IDR")

print(f"\n--- Summary in IDR ---")
print(f"Gross:    Rp {gross * rate:,.0f}")
print(f"Fees:     Rp {fees * rate:,.0f}")
print(f"Connects: Rp {connects * rate:,.0f}")
print(f"Net:      Rp {net * rate:,.0f}")

output_path = os.path.join(script_dir, "output", "summary.txt")

with open(output_path, "w") as f:
    f.write("Upwork Tracker Summary\n")
    f.write("=" * 30 + "\n\n")
    f.write(f"Gross:    ${gross:.2f}  (Rp {gross * rate:,.0f})\n")
    f.write(f"Fees:     ${fees:.2f}  (Rp {fees * rate:,.0f})\n")
    f.write(f"Connects: ${connects:.2f}  (Rp {connects * rate:,.0f})\n")
    f.write(f"Net:      ${net:.2f}  (Rp {net * rate:,.0f})\n")

print(f"\nSaved summary to {output_path}")

df['Date'] = pd.to_datetime(df['Date'])
print(df['Date'].head())
print(df['Date'].dtype)

monthly = df.groupby(df['Date'].dt.to_period('M'))['Amount $'].sum()
print("\n--- By Month (all transactions) ---")
print(monthly)

non_payments = df[df['Transaction type'] != 'Payment']
monthly = non_payments.groupby(non_payments['Date'].dt.to_period('M'))['Amount $'].sum()
print("\n--- By Month (excluding transfers) ---")
print(monthly)