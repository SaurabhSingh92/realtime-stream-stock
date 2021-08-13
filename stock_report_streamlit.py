import datetime

import streamlit as st
import yfinance as yf
import pandas as pd


@st.cache(suppress_st_warning=True)
def get_data(nm):
    data = yf.download(tickers=nm, period='max').sort_index(ascending=False)
    return data

@st.cache(suppress_st_warning=True)
def get_daily(nm):
    data = yf.download(tickers=nm, period='1d', interval='1m').sort_index(ascending=False)
    return data

def main():
    st.set_page_config(page_title="Stock Report", layout="wide")
    st.title("Stock Report ")
    st.sidebar.title("Menu")
    nm = st.sidebar.text_input('Enter the Share Name', value="INFY.NS")
    if nm:
        stk = yf.Ticker(f'{nm}'.upper())
        detail = pd.json_normalize(stk.info)[['longName', 'sector', 'longBusinessSummary',
                                              'exchange', 'country', "regularMarketPrice"]]
        st.subheader(f"{detail['longName'][0]} ({nm})")
        st.subheader("Stock Basic Details")
        r1, r2, r3, r4, r5 = st.columns((1, 1, 1, 1, 1))
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
        df = get_daily(nm)
        desc = st.expander(label="Click to know more about the company !! ")
        desc.write(detail['longBusinessSummary'][0])
        latest = st.expander(label="Last 5 min stock price")
        latest.dataframe(df[:5])
        latest.write()
        st.title("Graphical Representation")
        temp = get_data(nm).reset_index()
        temp['Date'] = pd.to_datetime(temp['Date']).dt.date
        temp.set_index(keys='Date', inplace=True)
        temp.sort_index(ascending=True, inplace=True)
        plot_opt = st.multiselect(label="Select the feature", options=df.columns)
        plot_sld = st.empty()
        plot_yr = st.empty()
        if plot_opt:
            start, end = plot_sld.select_slider(label="Select the Date Range", options=temp.index, value=[temp.index[0],temp.index[-1]])
            temp = temp.loc[start:end]
            plot_yr.line_chart(data=temp[plot_opt], use_container_width=True)
            k1, k2, k3, k4, k5 = st.columns((1, 1, 1, 1, 1))
            with k1:
                if st.button(label="YTD"):
                    year = datetime.date.today().replace(month=1,day=1)
                    temp = temp.loc[year:temp.index[-1]]
            with k2:
                if st.button(label="Last 6 Months"):
                    year = temp.index[-180]
                    temp = temp.loc[year:temp.index[-1]]
            with k3:
                if st.button(label="Last 3 Months"):
                    year = temp.index[-90]
                    temp = temp.loc[year:temp.index[-1]]
            with k4:
                if st.button(label="Last 30 Days"):
                    year = temp.index[-30]
                    temp = temp.loc[year:temp.index[-1]]
            with k5:
                if st.button(label="Last 7 Day"):
                    year = temp.index[-7]
                    temp = temp.loc[year:temp.index[-1]]
            plot_yr.line_chart(data=temp[plot_opt], use_container_width=True)
        st.title("Know more about stock")
        opt_title = st.empty()
        opt = st.empty()
        b1, b2, b3, b4 = st.columns((1, 1, 2, 1))
        with b1:
            if st.button(label="Major Holder"):
                share = pd.DataFrame(stk.major_holders).rename(columns={0: "Percentage", 1: "Institutes"})
                share.set_index('Institutes', inplace=True)
                opt_title.subheader("Major Holder Details")
                opt.write(share)
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

        st.subheader("Click to rest the search")
        if st.button(label="Reset"):
            opt.empty()
            opt_title.empty()
            plot_sld.empty()
            plot_yr.empty()
            plot_opt.clear()


if __name__ == "__main__":
    main()
