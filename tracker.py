import os
import glob
import shutil
import requests
import pandas as pd


def get_rate():
    url = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(url)
    return response.json()["rates"]["IDR"]


def compute_totals(df):
    gross = df[df['Transaction type'].isin(['Fixed-price', 'Bonus'])]['Amount $'].sum()
    fees = df[df['Transaction type'] == 'Service Fee']['Amount $'].sum()
    connects = df[df['Transaction type'] == 'Connects']['Amount $'].sum()
    net = gross + fees + connects
    return {'gross': gross, 'fees': fees, 'connects': connects, 'net': net}


def save_summary(totals, rate, path):
    with open(path, "w") as f:
        f.write("Upwork Tracker Summary\n")
        f.write("=" * 30 + "\n\n")
        f.write(f"Gross:    ${totals['gross']:.2f}  (Rp {totals['gross'] * rate:,.0f})\n")
        f.write(f"Fees:     ${totals['fees']:.2f}  (Rp {totals['fees'] * rate:,.0f})\n")
        f.write(f"Connects: ${totals['connects']:.2f}  (Rp {totals['connects'] * rate:,.0f})\n")
        f.write(f"Net:      ${totals['net']:.2f}  (Rp {totals['net'] * rate:,.0f})\n")


def find_csv(script_dir):
    downloads_dir = os.path.expanduser("~/Downloads")
    data_dir = os.path.join(script_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    files = glob.glob(os.path.join(downloads_dir, "*transaction_report.csv"))

    if files:
        latest = max(files)
        csv_path = os.path.join(data_dir, os.path.basename(latest))
        if not os.path.exists(csv_path):
            for old_file in glob.glob(os.path.join(data_dir, "*transaction_report.csv")):
                os.remove(old_file)
            shutil.move(latest, csv_path)
    else:
        existing = glob.glob(os.path.join(data_dir, "*transaction_report.csv"))
        if not existing:
            print("No report found anywhere. Export from Upwork first.")
            exit()
        csv_path = max(existing)

    return csv_path

def load_csv(path):
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    csv_path = find_csv(script_dir)
    df = load_csv(csv_path)
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns")

    totals = compute_totals(df)
    rate = get_rate()

    print(f"Gross:    ${totals['gross']:.2f}")
    print(f"Fees:     ${totals['fees']:.2f}")
    print(f"Connects: ${totals['connects']:.2f}")
    print(f"Net:      ${totals['net']:.2f}")

    print(f"\nRate: 1 USD = {rate:,.2f} IDR")

    print(f"\n--- Summary in IDR ---")
    print(f"Gross:    Rp {totals['gross'] * rate:,.0f}")
    print(f"Fees:     Rp {totals['fees'] * rate:,.0f}")
    print(f"Connects: Rp {totals['connects'] * rate:,.0f}")
    print(f"Net:      Rp {totals['net'] * rate:,.0f}")

    output_path = os.path.join(script_dir, "output", "summary.txt")
    save_summary(totals, rate, output_path)
    print(f"\nSaved summary to {output_path}")

    non_payments = df[df['Transaction type'] != 'Payment']
    monthly = non_payments.groupby(non_payments['Date'].dt.to_period('M'))['Amount $'].sum()
    print("\n--- By Month ---")
    for month, amount in monthly.items():
        print(f"{month}:  ${amount:>8.2f}")


if __name__ == "__main__":
    main()