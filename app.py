import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time
from datetime import datetime
import sqlite3
import random

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Car Price Predictor", page_icon="🚗", layout="wide")

# =========================
# DATABASE BACKEND
# =========================
conn = sqlite3.connect("database.db", check_same_thread=False)
cur = conn.cursor()

# Updated table with username
cur.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    timestamp TEXT,
    present_price REAL,
    kms INT,
    fuel TEXT,
    seller TEXT,
    transmission TEXT,
    owner INT,
    age INT,
    predicted_price REAL,
    depreciation REAL
)
""")
conn.commit()

# =========================
# LOAD MODEL
# =========================
@st.cache_resource
def load_model():
    return joblib.load("car_price_model.pkl")

model = load_model()

# =========================
# UI STYLING
# =========================
st.markdown("""
<style>
.main-header {
    font-size: 3.5rem;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(-45deg,#667eea,#764ba2,#4facfe);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.prediction-card{
    background:linear-gradient(135deg,#667eea,#764ba2);
    padding:2rem;
    border-radius:15px;
    color:white;
    text-align:center;
}
.fun-fact{
    background:#f0f2f6;
    padding:1rem;
    border-radius:10px;
    border-left:4px solid #667eea;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown('<p class="main-header">🚗 AI Car Price Oracle</p>', unsafe_allow_html=True)
st.markdown("### Predict resale value using Machine Learning")

# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs(["🔮 Predict", "📈 History", "🎲 Compare"])

# ====================================================
# PREDICTION TAB
# ====================================================
with tab1:

    col1, col2 = st.columns(2)

    with col1:
        username = st.text_input("👤 Your Name", placeholder="Enter your name")
        present_price = st.number_input("Showroom Price (lakhs)", 0.0, 100.0, 5.0)
        kms_driven = st.number_input("Kilometers Driven", 0, 500000, 50000)
        car_age = st.number_input("Car Age (years)", 0, 30, 3)

    with col2:
        fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
        transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
        seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
        owner = st.selectbox("Previous Owners", [0,1,2,3])

    if st.button("🔮 Predict Price", use_container_width=True):

        if username.strip() == "":
            st.warning("Please enter your name before predicting!")
        else:
            with st.spinner("AI is calculating..."):
                time.sleep(1)

            data = pd.DataFrame({
                "Present_Price":[present_price],
                "Kms_Driven":[kms_driven],
                "Fuel_Type":[fuel_type],
                "Seller_Type":[seller_type],
                "Transmission":[transmission],
                "Owner":[owner],
                "Car_Age":[car_age]
            })

            prediction = float(model.predict(data)[0])
            depreciation = ((present_price - prediction) / present_price) * 100 if present_price else 0

            # SAVE TO DATABASE
            cur.execute("""
            INSERT INTO predictions 
            (username, timestamp, present_price, kms, fuel, seller, transmission, owner, age, predicted_price, depreciation)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (
                username,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                present_price,
                kms_driven,
                fuel_type,
                seller_type,
                transmission,
                owner,
                car_age,
                prediction,
                depreciation
            ))
            conn.commit()

            st.balloons()

            st.markdown(f"""
            <div class="prediction-card">
                <h1>₹ {round(prediction,2)} Lakhs</h1>
                <p>Estimated Resale Price</p>
            </div>
            """, unsafe_allow_html=True)

            colm1, colm2, colm3 = st.columns(3)
            colm1.metric("Depreciation", f"{round(depreciation,1)}%")
            colm2.metric("Car Age", f"{car_age} years")
            colm3.metric("Mileage", f"{kms_driven} km")

# ====================================================
# HISTORY TAB
# ====================================================
with tab2:

    df = pd.read_sql("""
    SELECT username, timestamp, predicted_price, depreciation, kms, age, fuel, transmission 
    FROM predictions ORDER BY id DESC
    """, conn)

    if not df.empty:

        fig = px.line(df, x="timestamp", y="predicted_price", color="username", title="Prediction Trend by User")
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df, use_container_width=True)

        if st.button("🗑️ Clear All History"):
            cur.execute("DELETE FROM predictions")
            conn.commit()
            st.rerun()
    else:
        st.info("No predictions yet!")

# ====================================================
# COMPARE TAB (basic)
# ====================================================
with tab3:
    st.info("Future enhancement: Compare multiple cars side by side")

# =========================
# SIDEBAR FUN FACTS
# =========================
with st.sidebar:
    facts = [
        "Cars lose 20% value in first year",
        "Low mileage increases resale value",
        "Diesel cars depreciate slower",
        "First owner cars sell faster",
        "Automatic cars have higher resale"
    ]
    st.info("💡 " + random.choice(facts))

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("Powered by Machine Learning + Database Backend")
st.caption("Developed by Manjit Samantaray")
st.markdown("© 2026 All rights reserved.")
