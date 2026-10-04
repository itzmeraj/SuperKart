import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="SuperKart Sales Forecaster", layout="centered")

st.title("🛒 SuperKart Sales Forecasting Dashboard")
st.write("Enter product and store attributes to forecast the total sales revenue.")

# Backend URL (Flask API endpoint inside docker network or local development)
BACKEND_URL = "http://backend:5000/predict"

# Input fields grouped logically
st.header("Product Attributes")
col1, col2 = st.columns(2)
with col1:
    product_weight = st.number_input("Product Weight (kg)", min_value=1.0, max_value=30.0, value=12.5, step=0.1)
    product_sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar", "reg"])
with col2:
    product_allocated_area = st.number_input("Product Allocated Area Ratio", min_value=0.0, max_value=0.3, value=0.05, format="%.4f")
    product_mrp = st.number_input("Product MRP ($)", min_value=10.0, max_value=300.0, value=150.0, step=0.5)

product_type = st.selectbox("Product Category", [
    "Dairy", "Soft Drinks", "Meat", "Fruits and Vegetables", "Household", 
    "Baking Goods", "Snack Foods", "Frozen Foods", "Breakfast", 
    "Health and Hygiene", "Hard Drinks", "Canned", "Bread", "Starchy Foods", 
    "Others", "Seafood"
])

st.header("Store Attributes")
col3, col4 = st.columns(2)
with col3:
    store_size = st.selectbox("Store Size", ["Medium", "High", "Small"])
    store_city = st.selectbox("Store City Type", ["Tier 1", "Tier 2", "Tier 3"])
with col4:
    store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
    store_age = st.number_input("Store Age (Years)", min_value=1, max_value=50, value=10, step=1)

# Convert outputs to API-ready payload
input_data = {
    'Product_Weight': [product_weight],
    'Product_Sugar_Content': [product_sugar],
    'Product_Allocated_Area': [product_allocated_area],
    'Product_Type': [product_type],
    'Product_MRP': [product_mrp],
    'Store_Size': [store_size],
    'Store_Location_City_Type': [store_city],
    'Store_Type': [store_type],
    'Store_Age': [store_age]
}

if st.button("Forecast Sales", type="primary"):
    try:
        # Call the Flask API
        with st.spinner("Calculating forecast..."):
            response = requests.post(BACKEND_URL, json=input_data)
            response_data = response.json()

        if response.status_code == 200:
            prediction = response_data['predictions'][0]
            st.success(f"🎯 Projected Sales Revenue for this Product: ${prediction:,.2f}")
        else:
            st.error(f"API Error: {response_data.get('error', 'Unknown backend failure')}")
    except Exception as e:
        st.error(f"Could not connect to the forecasting backend. Error: {e}")