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
from currencies import currencies_dict
from charts import line_chart, pie_chart
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt



st.set_page_config(layout="wide")

connection = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"

motor = create_engine(connection)

refresh = st_autorefresh(interval=1000 * 10, limit=100)



def import_dashboard(quotes):
    with motor.connect() as conn:
        df = pd.read_sql(quotes, conn)

    return df


   
def board():
    df = import_dashboard("SELECT * FROM quotes_coins;")
    df["price SEK"] = df["Price"] * currencies_dict["SEK"]
    df["price DKK"] = df["Price"] * currencies_dict["DKK"]
    df["price NOK"] = df["Price"] * currencies_dict["NOK"]
    df["price EUR"] = df["Price"]
    btc_df = df[df["Name"] == "Bitcoin"]
    sol_df = df[df["Name"] == "Solana"]

    st.markdown("# Crypto currency dashboard")
    st.divider()
   


#  Function to fetch the latest timestamp
    def get_latest_update():
        query = "SELECT MAX(timestamp) AS latest_update FROM quotes_coins;"
        df = pd.read_sql_query(query, motor)
        return df["latest_update"][0] if not df.empty else "No data available"



#  Display the latest timestamp
    latest_update = get_latest_update()
    st.markdown(f"##### 🕒 Latest Update: **{latest_update}**")


    st.divider()
    crypto_choice = st.selectbox("Choose crypto", ["Bitcoin", "Solana"])
    currency_choice = st.selectbox("Choose currency", ["SEK", "NOK", "DKK", "EUR"])

    price_column = f"price {currency_choice}"
    if crypto_choice == "Bitcoin":
        current_df = btc_df
    elif crypto_choice == "Solana":
        current_df = sol_df
    st.markdown("## Latest price")
    st.metric(
        f"{crypto_choice}",
        f"{current_df[price_column].iloc[-1]:,.2f} {currency_choice}",
        border=True,
    )


    col1, col2, col3= st.columns(3)
    with col1:
        with col1:
            current_price = line_chart(
                current_df["timestamp"],
                current_df["Price"],
                title=f"Current Price {crypto_choice} ({currency_choice})",
                xlabel="Time",
                ylabel="Price",
                label="Current Price",
            )
            st.pyplot(current_price)
        with col2:
            img_path = Path(__file__).parent / "husky.jpg"
            st.image(img_path, caption="Husky Dog", use_container_width=True)
        with col3:
            # ---- Piechart
            pie_chart_df = df[["Name", "Market cap dominance"]].iloc[-2:]

            total_dominance = pie_chart_df["Market cap dominance"].sum()
            others_dominance = 100 - total_dominance

            others_row = pd.DataFrame(
                [{"Name": "Others", "Market cap dominance": others_dominance}]
            )
            pie_chart_df = pd.concat([pie_chart_df, others_row], ignore_index=True)

            market_cap = pie_chart(
                labels=pie_chart_df["Name"],
                sizes=pie_chart_df["Market cap dominance"],
                title="Market capitalization",
            )

            st.pyplot(market_cap)
    
    col1, col2 = st.columns(2)
    with col1:
        fig1 = line_chart(
                current_df["timestamp"],
                current_df["Percentage change in 1 hour"],
                title=f"1 Hour Change - {crypto_choice}",
                xlabel="Time")
        st.pyplot(fig1)
    with col2:
        fig2 = line_chart(
                current_df["timestamp"],
                current_df["Percentage change in 24 hours"],
                title=f"24 Hour Change - {crypto_choice}",
                xlabel="Time")
        st.pyplot(fig2)
    col1, col2 = st.columns(2)
    with col1:
        fig3 = line_chart(
                current_df["timestamp"],
                current_df["Percentage change in 7 days"],
                title=f"7 Days Change - {crypto_choice}",
                xlabel="Time")
        st.pyplot(fig3)
    with col2:
        fig4 = line_chart(
                current_df["timestamp"],
                current_df["Percentage change in 30 days"],
                title=f"30 Days Change - {crypto_choice}",
                xlabel="Time")
        st.pyplot(fig4)

    #st.markdown("# Dataframe")
    #st.dataframe(df.tail())


if __name__ == "__main__":
    board()