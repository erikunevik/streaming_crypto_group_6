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

#-- Creating connection to psotgres

connection = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"

motor = create_engine(connection)

refresh = st_autorefresh(interval=1000 * 10, limit=100)

#--Fetching DF


def import_dashboard(quotes):
    with motor.connect() as conn:
        df = pd.read_sql(quotes, conn)

    return df


 # Creating currency converter for dashboard
def board():
    df = import_dashboard("SELECT * FROM quotes_coins;")
    df["price SEK"] = df["Price"] * currencies_dict["SEK"]
    df["price DKK"] = df["Price"] * currencies_dict["DKK"]
    df["price NOK"] = df["Price"] * currencies_dict["NOK"]
    df["price EUR"] = df["Price"]
    btc_df = df[df["Name"] == "Bitcoin"]
    sol_df = df[df["Name"] == "Solana"]
    
# ---- Main headline of dashboard

    st.markdown("# Crypto currency dashboard")
    st.divider()
   


 # --- Time stamp function to get latest update
    def get_latest_update():
        query = "SELECT MAX(timestamp) AS latest_update FROM quotes_coins;"
        df = pd.read_sql_query(query, motor)

        if df.empty or df["latest_update"][0] is None:
            return "No data available"

        latest_update = pd.to_datetime(df["latest_update"][0]).strftime("%Y-%m-%d %H:%M:%S")
        return latest_update

            
    latest_update = get_latest_update()
    st.markdown(f"##### 🕒 Latest Update: **{latest_update}**")

    
#---- Choose crypto and currency boxes


    st.divider()
    crypto_choice = st.selectbox("Choose crypto", ["Bitcoin", "Solana"])
    currency_choice = st.selectbox("Choose currency", ["SEK", "NOK", "DKK", "EUR"])
    
 #---- Getting the latest price

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
    
# ---- Current price chart
    
    with col1:
        
            current_price = line_chart(
                current_df["timestamp"],
                current_df[price_column],
                title=f"Current Price {crypto_choice} ({currency_choice})",
                xlabel="Time",
                ylabel="Price",
                label="Current Price",
            )
            st.pyplot(current_price)
# ---- team picture 
    with col2:
            img_path = Path(__file__).parent / "husky.jpg"
            st.image(img_path, use_container_width=True)
                
# ---- Piechart
    with col3:
                      
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
    
#---- Creating 4 change graphs
            

    colors = ["red", "blue", "green", "orange"]
    
    col1, col2 = st.columns(2)
    with col1:
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        ax1.plot(
                current_df["timestamp"],
                current_df["Percentage change in 1 hour"],
                #title=f"1 Hour Change - {crypto_choice}",
                #marker="o",
                linestyle="-",
                linewidth=2,
        )
        ax1.set_title(f"1 Hour Change - {crypto_choice}", fontsize=14, fontweight="bold")
        ax1.set_xlabel("Time", fontsize=12)
        ax1.set_ylabel("Change (%)", fontsize=12)
        ax1.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig1)
        


    with col2:
        fig2 = line_chart(
                current_df["timestamp"],
                current_df["Percentage change in 24 hours"],
                title=f"24 Hour Change - {crypto_choice}",
                xlabel="Time",
                hour_format=True # To enable adding minutes
                )
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

if __name__ == "__main__":
    board()