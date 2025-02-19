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
        st.metric("Latest Bitcoin price", f"{(df["Price"]*currencies_dict["SEK"]).iloc[-1]:,.2f} SEK", border=True)
        #price_chart0 = line_chart(x= df["timestamp"], y= df["Price"]*currencies_dict["SEK"], title="Current price")
        #st.pyplot(price_chart0)
    elif currency_choice == "NOK":
        st.metric("Latest Bitcoin price", f"{(df["Price"]*currencies_dict["NOK"]).iloc[-1]:,.2f} NOK", border=True)
        #price_chart0 = line_chart(x= df["timestamp"], y= df["Price"]*currencies_dict["NOK"], title="Current price")
        #st.pyplot(price_chart0)
    elif currency_choice == "DKK":
        st.metric("Latest Bitcoin price", f"{(df["Price"]*currencies_dict["DKK"]).iloc[-1]:,.2f} DKK", border=True)
        #price_chart0 = line_chart(x= df["timestamp"], y= df["Price"]*currencies_dict["DKK"], title="Current price")
        #st.pyplot(price_chart0)
    else:
        st.metric("Latest Bitcoin price", f"{(df["Price"]).iloc[-1]:,.2f} EUR", border=True)
        

# Highlighting the highest and lowest price points
    max_price_idx = df["Price"].idxmax()
    min_price_idx = df["Price"].idxmin()
    ax1.scatter(df["timestamp"][max_price_idx], df["Price"][max_price_idx], color="red", s=100, label="Max Price", zorder=3)
    ax1.scatter(df["timestamp"][min_price_idx], df["Price"][min_price_idx], color="green", s=100, label="Min Price", zorder=3)

# Set a beautiful Seaborn style
    sns.set_style("whitegrid")

    st.markdown("#Market Data Visualization")

### **Chart 1: Current Price Over Time**
    fig1,ax1 = plt.subplots(figsize=(12, 6))

# Plot current price trend
    ax1.plot(df["timestamp"], df["Price"], 
         label="Current Price", marker="o", markersize=4, 
         linestyle="-", linewidth=2, color="royalblue", alpha=0.8)

# Highlighting the highest and lowest price points
    max_price_idx = df["Price"].idxmax()
    min_price_idx = df["Price"].idxmin()
    ax1.scatter(df["timestamp"][max_price_idx], df["Price"][max_price_idx], color="red", s=100, label="Max Price", zorder=3)
    ax1.scatter(df["timestamp"][min_price_idx], df["Price"][min_price_idx], color="green", s=100, label="Min Price", zorder=3)

# X-Axis Formatting
    ax1.xaxis.set_major_locator(plt.MaxNLocator(8))
    ax1.set_xlabel("Timestamp", fontsize=12)
    ax1.set_ylabel("Price", fontsize=12)
    ax1.set_title("Current Price Over Time", fontsize=14, fontweight="bold")
    plt.xticks(rotation=45)

# Add grid & legend
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend()

### ** Chart 2: Percentage Change Over Time**
    fig2, ax2 = plt.subplots(figsize=(12, 6))

# Plot percentage changes
    ax2.plot(df["timestamp"], df["Percentage change in 7 days"], label="7 Days Change", marker="o", linestyle="-", color="purple")
    ax2.plot(df["timestamp"], df["Percentage change in 1 hour"], label="1 Hour Change", marker="s", linestyle="--", color="orange")
    ax2.plot(df["timestamp"], df["Percentage change in 24 hours"], label="24 Hours Change", marker="d", linestyle=":", color="teal")

# X-Axis Formatting
    ax2.xaxis.set_major_locator(plt.MaxNLocator(8))
    ax2.set_xlabel("Timestamp", fontsize=12)
    ax2.set_ylabel("Percentage Change (%)", fontsize=12)
    ax2.set_title("📊 Percentage Change Over Time", fontsize=14, fontweight="bold")
    plt.xticks(rotation=45)

# Add grid & legend
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend()
# Display in Streamlit
    st.pyplot(fig1)

# Display Second Chart
    st.pyplot(fig2)


    
    
# ---- Piechart 
    
    pie_chart_df = df[["Name", "Market cap dominance"]].iloc[-2:]

    total_dominance = pie_chart_df["Market cap dominance"].sum()
    others_dominance = 100 - total_dominance

    others_row = pd.DataFrame([{"Name": "Others", "Market cap dominance": others_dominance}])
    pie_chart_df = pd.concat([pie_chart_df, others_row], ignore_index=True)

    market_cap = pie_chart(labels=pie_chart_df["Name"], sizes=pie_chart_df["Market cap dominance"], title="Market capitalization")
        
    st.pyplot(market_cap)
    
    st.markdown("# Dataframe")
    st.dataframe(df.tail())  
    img_path = Path(__file__).parent /"husky.jpg"
    st.image(img_path, caption="Husky Dog", use_container_width=True)
    
if __name__== "__main__":
    board()
   