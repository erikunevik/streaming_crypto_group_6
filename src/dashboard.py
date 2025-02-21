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
import matplotlib.dates as mdates



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
            
    current_df["timestamp"] = pd.to_datetime(current_df["timestamp"])
    last_hour = current_df["timestamp"].max() - pd.Timedelta(hours=1)
    filtered_df = current_df[current_df["timestamp"] >= last_hour]
    colors = ['#155263', '#ff6f3c', '#ff9a3c', '#ffc93c']
    
    col1, col2 = st.columns(2)
    with col1:
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        ax1.plot(
                filtered_df["timestamp"],
                filtered_df["Percentage change in 1 hour"],
                color=colors[0],
                linestyle="-",
                linewidth=2,
                
        )
        ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=10)) 
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))  
        plt.xticks(rotation=45)  
        ax1.set_title(f"1 Hour Change - {crypto_choice}", fontsize=12, fontweight="bold")
        ax1.set_xlabel("Time", fontsize=12)
        ax1.set_ylabel("Change (%)", fontsize=12)
        ax1.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig1)
        


    with col2:
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.plot(
                current_df["timestamp"],
                current_df["Percentage change in 24 hours"],
                color=colors[1],
                linestyle="-",
                linewidth=2,
        )

        ax2.xaxis.set_major_locator(mdates.HourLocator(interval=1))  
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))  
        ax2.set_title(f"24 Hour Change - {crypto_choice}", fontsize=12, fontweight="bold")
        ax2.set_xlabel("Time(Hourly)", fontsize=12)
        ax2.set_ylabel("Change (%)", fontsize=12)
        ax2.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig2)
    col1, col2 = st.columns(2)
    with col1:
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        ax3.plot(
                current_df["timestamp"],
                current_df["Percentage change in 7 days"],
                color=colors[2],
                linestyle="-",
                linewidth=2,
        )
        ax3.xaxis.set_major_locator(mdates.DayLocator(interval=1))  
        ax3.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d")) 
        plt.xticks(rotation=45)
        ax3.set_title(f"7 days change - {crypto_choice}", fontsize=12, fontweight="bold")
        ax3.set_xlabel("Date", fontsize=12)
        ax3.set_ylabel("Change (%)", fontsize=12)
        ax3.grid(True, linestyle="--", alpha=0.5)
        
        st.pyplot(fig3)
    with col2:
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        ax4.plot(
                current_df["timestamp"],
                current_df["Percentage change in 30 days"],
                color=colors[3]
        )
       
        ax4.xaxis.set_major_locator(mdates.DayLocator(interval=5))  
        ax4.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d")) 
        plt.xticks(rotation=45)  
        ax4.set_title(f"30 days change - {crypto_choice}", fontsize=12, fontweight="bold")
        ax4.set_xlabel("Date", fontsize=12)
        ax4.set_ylabel("Change (%)", fontsize=12)
        ax4.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig4)

if __name__ == "__main__":
    board()