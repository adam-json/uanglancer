import streamlit as st
import pandas as pd

from tracker import (
    compute_totals,
    get_rate,
    compare_tax_schemes,
    get_current_balance,
    top_clients,
    count_connects,
)

st.set_page_config(
    page_title="Upwork ID",
    page_icon="💼",
    layout="wide",
)

st.title("Upwork ID")
st.caption("Untuk freelancer Indonesia")

uploaded = st.file_uploader("Upload your transaction_report.csv", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)
    df['Date'] = pd.to_datetime(df['Date'])

    totals = compute_totals(df)
    rate = get_rate()
    from tracker import get_current_balance
    gross_idr = totals['gross'] * rate
    schemes = compare_tax_schemes(gross_idr)

    st.sidebar.metric("USD → IDR", f"{rate:,.0f}")
    st.sidebar.caption("Live exchange rate")

    st.divider()
    st.subheader("🏆 Top Clients")
    clients = top_clients(df)
    st.dataframe(clients, use_container_width=True)

    st.subheader("💰 Earnings (USD)")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Gross", f"${totals['gross']:.2f}")
    col2.metric("Fees", f"${totals['fees']:.2f}")
    col3.metric("Connects", f"${totals['connects']:.2f}")
    col4.metric("Net", f"${totals['net']:.2f}")
    col5.metric("Connects #", count_connects(df))

    st.divider()

    st.subheader("🇮🇩 Earnings (IDR)")
    col1, col2 = st.columns(2)
    col1.metric("Gross", f"Rp {gross_idr:,.0f}")
    col2.metric("Net", f"Rp {totals['net'] * rate:,.0f}")

    st.divider()
    st.subheader("💵 Current Balance")
    st.metric("Upwork balance", f"${get_current_balance(df):.2f}")

    st.divider()

    st.subheader("🧾 Tax Estimate")
    col1, col2, col3 = st.columns(3)
    col1.metric("UMKM 0.5%", f"Rp {schemes['umkm']:,.0f}")
    col2.metric("NPPN", f"Rp {schemes['nppn']:,.0f}")
    col3.metric("Cheaper", schemes['cheaper'].upper())

    st.divider()

    st.subheader("📊 Monthly Net")
    non_payments = df[df['Transaction type'] != 'Payment']
    monthly = non_payments.groupby(non_payments['Date'].dt.to_period('M'))['Amount $'].sum()
    monthly.index = monthly.index.astype(str)
    monthly.name = "Net (USD)"
    st.bar_chart(monthly, color="#4CAF50", height=300)

    st.divider()
    st.caption("Built with Python + Streamlit · [GitHub](https://github.com/adam-json/upwork-id)")
    
if not uploaded:
    st.info("👆 Upload your Upwork transaction_report.csv to see your dashboard.")