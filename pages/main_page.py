import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st


st.title('Amarican Stock Visualize Application')


st.sidebar.write("""
# GAFA Stock Price
This is the stock visulization tool. Choose show days from the option below.
""")

st.sidebar.write("""
##  Select the show days
""")

days = st.sidebar.slider('the number of days', 1, 50, 20)
st.write(f"""
## GAFA stock prices for **the latest {days} days**.
""")

@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df,hist])
    return df
try:
    st.sidebar.write("""
    ## Selection the range of stock prices
    """)

    ymin, ymax = st.sidebar.slider("""
    Please select the range of stock prices.
    """,
    0.0, 3500.0, (0.0, 3500.0)
    )

    tickers = {
        'apple': 'AAPL',
        'meta': 'META',
        'google': 'GOOGL',
        'microsoft': 'MSFT',
        'netflix': 'NFLX',
        'amazon': 'AMZN'
    }

    df = get_data(days,tickers)
    # Default companies' list.
    companies = st.multiselect(
        'Please select the names of companies.',
        # Show the list of companies you don't select.
        list(df.index),
        ['google','amazon','meta','apple']
    )
    # Users don't select the company, show error message.
    if not companies:
        st.error('Please select at least one company.')
    else:
        data = df.loc[companies]
        # Show the sheet of data by data.sort_index()
        st.write('### Stock prices(USD)',data.sort_index())
        # Transpose the data shape.
        data = data.T.reset_index()
        data = pd.melt(data, id_vars =['Date']).rename(
            columns = {'value': 'Stock Prices(USD)'}
        )
        # Select the graph you'd like to emphasize.
        selection = alt.selection_multi(fields=['Name'], bind='legend')
        chart = alt.Chart(data).mark_line(opacity= 0.8,clip=True).encode(
                x='Date:T',
                y=alt.Y('Stock Prices(USD):Q', stack=None, scale =alt.Scale(domain=[ymin,ymax])),
                color='Name:N',
                opacity=alt.condition(selection, alt.value(1), alt.value(0.1))
            ).add_selection(
                selection
            )
        # Show the detail data where you adjust the graph.
        hover = alt.selection_single(
            fields=["Date"],
            nearest=True,
            on="mouseover",
            empty="none",
        )
        chart_temp = (
            alt.Chart(data)
            .encode(
                x="Date:T",
                y="Stock Prices(USD):Q",
                color="Name:N",
            )
        )
        points = chart_temp.transform_filter(hover).mark_circle(size=50)

        # Display the tooltips when hovering.
        tooltips = (
            alt.Chart(data)
            .mark_rule()
            .encode(
                x="Date:T",
                y="Stock Prices(USD):Q",
                opacity=alt.condition(hover, alt.value(0.1), alt.value(0)),
                # Show toolkip, "Date:T": the date, "Stock Prices(USD):Q"
                tooltip=[
                    alt.Tooltip("Date:T", title="Date"),
                    alt.Tooltip("Stock Prices(USD):Q", title="Stock Prices(USD)"),
                    alt.Tooltip("Name", title="Name"),
                ],
            )
            .add_selection(hover)
        )
        # Show the chart with points and toolkips.
        st.altair_chart((chart + points + tooltips).interactive(), use_container_width=True)

except:
    st.error(
    """
    Oops! Something wrong happens!!
    """
    )
