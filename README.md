import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
# Page config
st.set_page_config(
   page_title="My Awesome App",
   page_icon="🚀",
   layout="wide",
   initial_sidebar_state="expanded"
)
# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data Explorer", "About"])
if page == "Home":
   st.title("Welcome to My Streamlit App")
   st.markdown("# VED AKSHOBHYA AMBASTHA")
   col1, col2 = st.columns(2)
   with col1:
       st.metric("Users Today", "Vivek", "↑ Upasna")
   with col2:
       st.metric("Response Time", "Upasna", "↓ 3ms")
elif page == "Data Explorer":
   st.title("Data Explorer")
   # File uploader
   uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
   if uploaded_file:
       df = pd.read_csv(uploaded_file)
       st.dataframe(df, use_container_width=True)
       # Interactive filters
       col1, col2 = st.columns(2)
       with col1:
           numeric_col = st.selectbox("Select numeric column", df.select_dtypes(include="number").columns)
       with col2:
           color_col = st.selectbox("Color by", df.columns)
       fig = px.histogram(df, x=numeric_col, color=color_col,
                         title=f"Distribution of {numeric_col}")
       st.plotly_chart(fig, use_container_width=True)
else:
   st.title("About")
   st.info("Lets get started!")
# Footer
st.caption(f"Built on {datetime.now().strftime('%Y-%m-%d %H:%M')} | Powered by Vivek")
