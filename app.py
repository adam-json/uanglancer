import streamlit as st
import pandas as pd

from tracker import (
    compute_totals,
    get_rate,
    compare_tax_schemes,
    get_current_balance,
    top_clients,
    count_connects,
    compute_roi_by_month,
)

from neonui import apply_theme, hide_streamlit_defaults
apply_theme("midnight")
hide_streamlit_defaults()

st.set_page_config(
    page_title="Uanglancer",
    page_icon="💼",
    layout="wide",
)

st.title("Uanglancer")
st.caption("Untuk freelancer Indonesia")
# Force headings to be bold, not italic
st.markdown(
    """
    <style>
    h1, h2, h3 {
        font-style: normal !important;
        font-weight: 700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Uanglancer")
st.caption("Untuk freelancer Indonesia")

uploaded = st.file_uploader("Upload your transaction_report.csv", type="csv")

if not uploaded:
    st.info("👆 Upload your Upwork transaction_report.csv to see your dashboard.")
else:
    df = pd.read_csv(uploaded)
    df['Date'] = pd.to_datetime(df['Date'])

    totals = compute_totals(df)
    rate = get_rate()
    gross_idr = totals['gross'] * rate
    schemes = compare_tax_schemes(gross_idr)

    # Sidebar
    st.sidebar.metric("USD → IDR", f"{rate:,.0f}")
    st.sidebar.caption("Live exchange rate")

    # Earnings (USD)
    st.subheader("💰 Earnings (USD)")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Gross", f"${totals['gross']:.2f}")
    col2.metric("Fees", f"${totals['fees']:.2f}")
    col3.metric("Connects", f"${abs(totals['connects']):.2f}")
    col4.metric("Net", f"${totals['net']:.2f}")
    st.caption(f"Connects used: {count_connects(df)}")

    st.divider()

    # Earnings (IDR)
    st.subheader("🇮🇩 Earnings (IDR)")
    col1, col2 = st.columns(2)
    col1.metric("Gross", f"Rp {gross_idr:,.0f}")
    col2.metric("Net", f"Rp {totals['net'] * rate:,.0f}")

    st.divider()

    # Current balance
    st.subheader("💵 Current Balance")
    st.metric("Upwork balance", f"${get_current_balance(df):.2f}")

    st.divider()

    # Tax
    st.subheader("🧾 Tax Estimate")
    col1, col2, col3 = st.columns(3)
    col1.metric("UMKM 0.5%", f"Rp {schemes['umkm']:,.0f}")
    col2.metric("NPPN", f"Rp {schemes['nppn']:,.0f}")
    col3.metric("Cheaper", schemes['cheaper'].upper())

    st.divider()

    st.subheader("🏆 Top Clients")
    clients = top_clients(df)
    clients_df = clients.reset_index()
    clients_df.columns = ['Client', 'Earned']
    clients_df['Earned'] = clients_df['Earned'].apply(lambda x: f"${x:.2f}")
    st.dataframe(clients_df, width='stretch', hide_index=True)

    st.divider()

    st.subheader("🎯 Connects ROI by Month")
    roi = compute_roi_by_month(df).reset_index()
    roi.columns = ['Month', 'Connects Spent', 'Earned', 'Net', 'ROI']
    roi['Month'] = roi['Month'].astype(str)
    roi['Connects Spent'] = roi['Connects Spent'].apply(lambda x: f"${x:.2f}")
    roi['Earned'] = roi['Earned'].apply(lambda x: f"${x:.2f}")
    roi['Net'] = roi['Net'].apply(lambda x: f"${x:.2f}")
    roi['ROI'] = roi['ROI'].apply(lambda x: f"{x:.2f}")
    st.dataframe(roi, width='stretch', hide_index=True)

    st.divider()

    # Monthly chart
    st.subheader("📊 Monthly Net")
    non_payments = df[df['Transaction type'] != 'Payment']
    monthly = non_payments.groupby(non_payments['Date'].dt.to_period('M'))['Amount $'].sum()
    monthly.index = monthly.index.astype(str)
    monthly.name = "Net (USD)"
    st.bar_chart(monthly, color="#4CAF50", height=300)

    st.divider()
    st.caption("Built with Python + Streamlit · [GitHub](https://github.com/adam-json/uanglancer)")