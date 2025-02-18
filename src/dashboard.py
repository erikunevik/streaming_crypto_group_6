import streamlit as st
from constants import (
POSTGRES_DBNAME,
POSTGRES_HOST,
POSTGRES_PASSWORD,
POSTGRES_PORT,
POSTGRES_USER,    
)
from sqlalchemy import create_engine
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from currencies import get_latest_exchange_rate
from charts import line_chart, pie_chart




connection = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"
    
motor = create_engine(connection)
    
refresh = st_autorefresh(interval=1000*10, limit=100)

def import_dashboard(quotes):
    with motor.connect() as conn:
        df = pd.read_sql(quotes, conn)
    
    return df

#def latest
def board():
    
    df = import_dashboard("SELECT * FROM quotes_coins;")

    st.markdown("# Crypto currency dashboard")
    
    currency_choice = st.selectbox("Choose crypto", ["Bitcoin","Solana"])
    currency_choice = st.selectbox("Choose currency", ["SEK", "NOK", "DKK", "EUR"])

    
    if currency_choice == "SEK":
        st.metric("Latest Bitcoin price", f"{(df["Price"]*get_latest_exchange_rate()["SEK"]).iloc[-1]:,.2f} SEK", border=True)
        price_chart0 = line_chart(x= df["timestamp"], y= df["Price"]*get_latest_exchange_rate()["SEK"], title="Current price")
        st.pyplot(price_chart0)
    elif currency_choice == "NOK":
        st.metric("Latest Bitcoin price", f"{(df["Price"]*get_latest_exchange_rate()["NOK"]).iloc[-1]:,.2f} NOK", border=True)
        price_chart0 = line_chart(x= df["timestamp"], y= df["Price"]*get_latest_exchange_rate()["NOK"], title="Current price")
        st.pyplot(price_chart0)
    elif currency_choice == "DKK":
        st.metric("Latest Bitcoin price", f"{(df["Price"]*get_latest_exchange_rate()["DKK"]).iloc[-1]:,.2f} DKK", border=True)
        price_chart0 = line_chart(x= df["timestamp"], y= df["Price"]*get_latest_exchange_rate()["DKK"], title="Current price")
        st.pyplot(price_chart0)
    else:
        st.metric("Latest Bitcoin price", f"{(df["Price"]).iloc[-1]:,.2f} EUR", border=True)
        price_chart0 = line_chart(x= df["timestamp"], y= df["Price"], title="Current price")
        st.pyplot(price_chart0)
    
    st.markdown("# Percent change")
    price_chart1 = line_chart(x= df["timestamp"], y= df["Percentage change in 7 days"], title="Percentage change in 7 days")
    price_chart2 = line_chart(x= df["timestamp"], y= df["Percentage change in 1 hour"], title="Percentage change in 1 hour")
    price_chart3 = line_chart(x= df.index, y= df["Percentage change in 24 hours"], title="Percentage change in 24 hours")
    
    st.pyplot(price_chart2)
    st.pyplot(price_chart1)
    st.pyplot(price_chart3)
    
    pie_chart_df = df[["Name", "Market cap dominance"]].iloc[-2:]

    market_cap = pie_chart(labels=pie_chart_df["Name"], sizes=pie_chart_df["Market cap dominance"], title="Market capitalization")
    st.pyplot(market_cap)
 
    st.markdown("# Dataframe")
    st.dataframe(df.tail())  
 
    st.image("husky.jpg", caption="Husky Dog", use_container_width=True)
    
if __name__== "__main__":
    board()
   