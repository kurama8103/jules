import streamlit as st
import arbitrage_calculator
import trade_analyzer

st.title("Jules's Crypto Analysis Dashboard")

st.write("""
Welcome to the dashboard. Please select an analysis to run.
""")

# --- Arbitrage Calculator ---
st.header("1. Arbitrage Calculator")
st.write("Calculates the current arbitrage opportunity between spot and futures.")
if st.button("Run Arbitrage Calculation"):
    with st.spinner("Fetching live market data..."):
        result_text = arbitrage_calculator.get_arbitrage_analysis()
        st.code(result_text)

# --- Trade Analyzer ---
st.header("2. Trade Analyzer")
st.write("Fetches the latest trades, saves them to a local database, and generates a chart of spot price, futures price, and the spread between them.")
if st.button("Generate Analysis Graph"):
    with st.spinner("Analyzing trades... This may take a moment."):
        fig = trade_analyzer.run_trade_analysis()
        if fig:
            st.pyplot(fig)
        else:
            st.warning("Could not generate plot. No trade data might be available.")
