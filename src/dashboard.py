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

def import_dashboard(quotes):
    
    connection = connection = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"
    
    motor = create_engine(connection)
    
    refresh = st_autorefresh(interval=1000*10, limit=100)
    
    with motor.connect() as conn:
        df = pd.read_sql(quotes, conn)
    
    return df

def board():
    
    df = import_dashboard("SELECT * FROM quotes_coins;")
    
    st.markdown("# Bitcoin dashboard")
    
    st.image("husky.jpg", caption="Husky Dog", use_container_width=True)
    
    st.markdown("# See the latest data")
    
    st.dataframe(df.tail())  
    
    
    
if __name__== "__main__":
    board()
    
        
        
    