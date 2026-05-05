import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CA House Price Predictor",
    page_icon="🏡",
    layout="wide",
)

# ── Session state init ────────────────────────────────────────────────────────
if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "last_input" not in st.session_state:
    st.session_state.last_input = None
if "history" not in st.session_state:
    st.session_state.history = []

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; font-family: 'Inter', sans-serif; }

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at top left, #0d1b2a 0%, #1b2838 40%, #0d1b2a 100%);
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,179,237,0.12);
    border: 1px solid rgba(99,179,237,0.3);
    color: #63b3ed;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    margin-bottom: 1rem;
}
.hero-title {
    font-size: clamp(2rem, 5vw, 3.2rem);
    font-weight: 800;
    background: linear-gradient(135deg, #e0f2fe 0%, #63b3ed 50%, #4299e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.15;
    margin-bottom: 0.6rem;
}
.hero-sub {
    color: rgba(255,255,255,0.4);
    font-size: 0.95rem;
    font-weight: 400;
}

/* ── Cards ── */
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(8px);
}
.glass-card:hover { border-color: rgba(99,179,237,0.2); }

.card-title {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #63b3ed;
    margin-bottom: 1.1rem;
}

/* ── Result card ── */
.result-card {
    background: linear-gradient(135deg,
        rgba(66,153,225,0.18) 0%,
        rgba(99,179,237,0.1) 100%);
    border: 1px solid rgba(99,179,237,0.45);
    border-radius: 24px;
    padding: 2.4rem 2rem;
    text-align: center;
    margin-bottom: 1rem;
}
.result-label {
    color: rgba(255,255,255,0.45);
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.result-price {
    font-size: clamp(2.4rem, 5vw, 3.6rem);
    font-weight: 800;
    background: linear-gradient(135deg, #e0f2fe, #63b3ed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.result-sub { color: rgba(255,255,255,0.3); font-size: 0.8rem; }

/* ── Pills ── */
.pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.4rem 0.9rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 600;
    margin-top: 1rem;
}
.pill-green  { background: rgba(72,187,120,0.15); border: 1px solid rgba(72,187,120,0.4); color: #68d391; }
.pill-yellow { background: rgba(246,173,85,0.15);  border: 1px solid rgba(246,173,85,0.4);  color: #f6ad55; }
.pill-red    { background: rgba(252,129,74,0.15);  border: 1px solid rgba(252,129,74,0.4);  color: #fc8150; }

/* ── Metric grid ── */
.metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.7rem;
    margin-top: 0.8rem;
}
.metric-tile {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 0.9rem 1rem;
}
.metric-tile:hover { background: rgba(99,179,237,0.07); }
.metric-name {
    font-size: 0.7rem;
    color: rgba(255,255,255,0.38);
    font-weight: 500;
    margin-bottom: 0.25rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.metric-value { font-size: 1.35rem; font-weight: 700; color: #e0f2fe; }
.metric-unit  { font-size: 0.7rem; color: rgba(255,255,255,0.3); margin-left: 2px; }

/* ── Insight rows ── */
.insight-list { display: flex; flex-direction: column; gap: 0.45rem; margin-top: 0.8rem; }
.insight-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0.8rem;
    background: rgba(255,255,255,0.03);
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.05);
}
.insight-key { color: rgba(255,255,255,0.5); font-size: 0.83rem; }
.insight-val { color: #63b3ed; font-weight: 600; font-size: 0.86rem; }

/* ── History ── */
.hist-row {
    display: grid;
    grid-template-columns: 1fr 1.2fr 1fr;
    gap: 0.5rem;
    align-items: center;
    padding: 0.55rem 0.8rem;
    border-radius: 10px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.05);
    font-size: 0.82rem;
    color: rgba(255,255,255,0.6);
    margin-bottom: 0.4rem;
}
.hist-price { color: #63b3ed; font-weight: 700; text-align: right; }

/* ── Streamlit overrides ── */
div[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: white !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: rgba(99,179,237,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,179,237,0.1) !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: white !important;
}
label { color: rgba(255,255,255,0.65) !important; font-size: 0.86rem !important; }
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #3182ce, #2b6cb0) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.7rem 1.4rem !important;
    box-shadow: 0 4px 15px rgba(49,130,206,0.3) !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(49,130,206,0.45) !important;
}
footer { display: none; }
.stAlert { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🤖 RandomForest · FastAPI · scikit-learn</div>
    <div class="hero-title">California House Price Predictor</div>
    <div class="hero-sub">1990 Census data · Fill in the block details below and hit Predict</div>
</div>
""", unsafe_allow_html=True)

# ── City preset ───────────────────────────────────────────────────────────────
CITIES = {
    "📍 Los Angeles":   (-118.25, 34.05),
    "📍 San Francisco": (-122.42, 37.77),
    "📍 San Diego":     (-117.16, 32.72),
    "📍 Sacramento":    (-121.49, 38.58),
    "📍 San Jose":      (-121.89, 37.34),
}
selected_city = st.selectbox("Quick city preset", list(CITIES.keys()), label_visibility="collapsed")
default_lon, default_lat = CITIES[selected_city]

# ── Layout ────────────────────────────────────────────────────────────────────
left, right = st.columns([1.05, 0.95], gap="large")

# ═══════════════════ LEFT ═══════════════════
with left:

    # Location
    st.markdown('<div class="glass-card"><div class="card-title">📍 Location</div>', unsafe_allow_html=True)
    lc1, lc2 = st.columns(2)
    with lc1:
        longitude = st.number_input("Longitude", min_value=-124.35, max_value=-114.31, value=default_lon, step=0.01, format="%.4f", key="longitude")
    with lc2:
        latitude  = st.number_input("Latitude",  min_value=32.54,   max_value=41.95,   value=default_lat, step=0.01, format="%.4f", key="latitude")
    ocean_proximity = st.selectbox("Ocean Proximity", ["<1H OCEAN", "INLAND", "ISLAND", "NEAR BAY", "NEAR OCEAN"], key="ocean")
    st.markdown('</div>', unsafe_allow_html=True)

    # Housing
    st.markdown('<div class="glass-card"><div class="card-title">🏠 Housing Characteristics</div>', unsafe_allow_html=True)
    hc1, hc2 = st.columns(2)
    with hc1:
        housing_median_age = st.slider("Median Housing Age (yrs)", 1, 52, 29, key="age")
    with hc2:
        median_income = st.slider("Median Income (×$10K)", 0.5, 15.0, 3.87, step=0.1, key="income")
    st.markdown('</div>', unsafe_allow_html=True)

    # Demographics
    st.markdown('<div class="glass-card"><div class="card-title">👥 Block Demographics</div>', unsafe_allow_html=True)
    dc1, dc2 = st.columns(2)
    with dc1:
        total_rooms    = int(st.number_input("Total Rooms",    min_value=1, max_value=40000, value=2635, step=10, key="rooms"))
        total_bedrooms = int(st.number_input("Total Bedrooms", min_value=1, max_value=7000,  value=537,  step=5,  key="bedrooms"))
    with dc2:
        population = int(st.number_input("Population", min_value=1, max_value=40000, value=1425, step=10, key="pop"))
        households = int(st.number_input("Households", min_value=1, max_value=7000,  value=499,  step=5,  key="households"))
    st.markdown('</div>', unsafe_allow_html=True)

    predict_btn = st.button("🔮  Predict House Price", use_container_width=True)

# ═══════════════════ RIGHT ═══════════════════
with right:

    # Live map — always visible
    st.markdown('<div class="glass-card"><div class="card-title">🗺️ Selected Location</div>', unsafe_allow_html=True)
    st.map(pd.DataFrame({"lat": [latitude], "lon": [longitude]}), zoom=8)
    st.markdown('</div>', unsafe_allow_html=True)

    # Prediction
    if predict_btn:
        errors = []
        if total_bedrooms > total_rooms:
            errors.append("Bedrooms cannot exceed total rooms.")
        if households > population:
            errors.append("Households cannot exceed population.")
        if errors:
            for e in errors:
                st.error(e)
            st.stop()

        input_data = {
            "longitude":          longitude,
            "latitude":           latitude,
            "housing_median_age": housing_median_age,
            "total_rooms":        total_rooms,
            "total_bedrooms":     total_bedrooms,
            "population":         population,
            "households":         households,
            "median_income":      median_income,
            "ocean_proximity":    ocean_proximity,
        }

        with st.spinner("Running model…"):
            try:
                resp = requests.post(f"{API_URL}/predict", json=input_data, timeout=10)
            except requests.exceptions.ConnectionError:
                st.error("⚠️ FastAPI backend is not running. Start it with: `uvicorn api:app --reload`")
                st.stop()
            except requests.exceptions.Timeout:
                st.error("⚠️ Request timed out.")
                st.stop()

        if resp.status_code != 200:
            st.error(f"API error {resp.status_code}: {resp.json().get('detail', 'Unknown error')}")
            st.stop()

        st.session_state.prediction = resp.json()["predicted_price"]
        st.session_state.last_input = input_data
        st.session_state.history.append({
            "city":  selected_city.replace("📍 ", ""),
            "ocean": ocean_proximity,
            "price": st.session_state.prediction,
        })

    # ── Display persisted result ──────────────────────────────────────────
    if st.session_state.prediction is not None:
        price = st.session_state.prediction
        inp   = st.session_state.last_input

        rooms_per_house   = inp["total_rooms"]    / inp["households"]
        bedrooms_per_room = inp["total_bedrooms"]  / inp["total_rooms"]
        people_per_house  = inp["population"]      / inp["households"]
        price_per_room    = price                  / inp["total_rooms"]
        income_annual     = inp["median_income"]   * 10_000
        pti_ratio         = price / income_annual
        CA_MEDIAN         = 233_000

        if price < CA_MEDIAN:
            pill_cls, pill_icon, tier = "pill-green",  "✅", "Below CA median"
        elif price < CA_MEDIAN * 1.5:
            pill_cls, pill_icon, tier = "pill-yellow", "⚡", "Near CA median"
        else:
            pill_cls, pill_icon, tier = "pill-red",    "🔥", "Above CA median"

        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">Estimated Median Home Value</div>
            <div class="result-price">${price:,.0f}</div>
            <div class="result-sub">CA dataset median ≈ $233,000</div>
            <div style="display:flex;justify-content:center;">
                <span class="pill {pill_cls}">{pill_icon} {tier}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-tile">
                <div class="metric-name">Rooms / Household</div>
                <div class="metric-value">{rooms_per_house:.1f}<span class="metric-unit">rooms</span></div>
            </div>
            <div class="metric-tile">
                <div class="metric-name">Bedroom Ratio</div>
                <div class="metric-value">{bedrooms_per_room:.1%}</div>
            </div>
            <div class="metric-tile">
                <div class="metric-name">People / Household</div>
                <div class="metric-value">{people_per_house:.1f}<span class="metric-unit">ppl</span></div>
            </div>
            <div class="metric-tile">
                <div class="metric-name">Price / Room</div>
                <div class="metric-value">${price_per_room:,.0f}</div>
            </div>
        </div>
        <div class="insight-list">
            <div class="insight-row">
                <span class="insight-key">Median household income</span>
                <span class="insight-val">${income_annual:,.0f} / yr</span>
            </div>
            <div class="insight-row">
                <span class="insight-key">Price-to-income ratio</span>
                <span class="insight-val">{pti_ratio:.1f}×</span>
            </div>
            <div class="insight-row">
                <span class="insight-key">Ocean proximity</span>
                <span class="insight-val">{inp["ocean_proximity"]}</span>
            </div>
            <div class="insight-row">
                <span class="insight-key">Housing median age</span>
                <span class="insight-val">{inp["housing_median_age"]} yrs</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── History ───────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.divider()
    st.markdown('<div class="card-title">🕘 Prediction History</div>', unsafe_allow_html=True)
    for entry in reversed(st.session_state.history[-6:]):
        st.markdown(f"""
        <div class="hist-row">
            <span>{entry["city"]}</span>
            <span>{entry["ocean"]}</span>
            <span class="hist-price">${entry["price"]:,.0f}</span>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("Frontend: Streamlit · Backend: FastAPI · Model: RandomForestRegressor · Data: CA Housing 1990 Census")