import streamlit as st
import yfinance as yf
import pandas as pd

@st.cache(suppress_st_warning=True)
def get_data(nm):
    data = yf.download(tickers=nm, period='1d', interval='1m').sort_index(ascending=False).head(5)
    return data

def main():
    st.set_page_config(page_title="Stock Report", layout="wide")
    st.title("Stock Report - ML/AI")
    st.sidebar.title("Menu")
    nm = st.sidebar.text_input('Share Name', value="INFY.NS")
    if nm:
        stk = yf.Ticker(f'{nm}'.upper())
        detail = pd.json_normalize(stk.info)[['longName', 'sector', 'longBusinessSummary',
                                                        'exchange', 'country', "regularMarketPrice"]]
        st.subheader(f"{detail['longName'][0]} ( {nm})")
        #st.write(yf.Ticker(nm).info)
        st.subheader("Stock Basic Details")
        r1,r2,r3,r4,r5 = st.columns((1,1,1,1,1))
        with r1:
            st.text_area(label='Full Name', value=detail['longName'][0])
        with r2:
            st.text_area(label="Sector", value=detail['sector'][0])
        with r3:
            st.text_area(label="Exchange Name", value=detail['exchange'][0])
        with r4:
            st.text_area(label="Base Country", value=detail['country'][0])
        with r5:
            st.text_area(label="Regular Stock Price", value=detail["regularMarketPrice"][0])
        desc = st.expander(label="Click to know more about the company !! ")
        desc.write(detail['longBusinessSummary'][0])
        latest = st.expander(label="Last 5 min stock price")
        latest.dataframe(get_data(nm))
        latest.write()
        opt_title = st.empty()
        opt = st.empty()
        b1,b2,b3,b4,b5 = st.columns((1,1,2,1,1))
        with b1:
            if st.button(label="Major Holder"):
                share = pd.DataFrame(stk.major_holders).rename(columns={0: "Percentage", 1: "Institutes"})
                opt_title.subheader("Major Holder Details")
                opt.table(share)
        with b2:
            if st.button(label="Events"):
                event = pd.DataFrame(stk.calendar)
                opt_title.subheader("Event Details")
                opt.write(event)
        with b3:
            if st.button(label="Quarterly Balance sheet"):
                qty_balance = pd.DataFrame(stk.quarterly_balance_sheet)
                opt_title.subheader("Quarterly Balance Sheet")
                opt.write(qty_balance.transpose())
        with b4:
            if st.button(label="Balance sheet"):
                balance = pd.DataFrame(stk.balancesheet)
                opt_title.subheader("Yearly Balance Sheet")
                opt.write(balance.transpose())
        with b5:
            if st.button(label="Reset"):
                opt.empty()
                opt_title.empty()


if __name__ == "__main__":
    main()