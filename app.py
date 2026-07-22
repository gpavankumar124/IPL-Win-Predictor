import streamlit as st
import pickle
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="IPL Win Predictor",
    page_icon="🏏",
    layout="centered"
)


st.markdown("""
<style>

/* ===========================
   Main Background
=========================== */

.stApp{
    background-color:#0E1117;
}

/* ===========================
   Text
=========================== */

html, body{
    color:white;
}

h1,h2,h3,h4,h5,h6{
    color:white !important;
}

label{
    color:white !important;
    font-weight:600;
}

/* ===========================
   Buttons
=========================== */

.stButton>button{
    width:100%;
    background:#2563EB;
    color:white;
    border:none;
    border-radius:12px;
    height:3.2em;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#1D4ED8;
}

/* ===========================
   Select Boxes
=========================== */

div[data-baseweb="select"]{
    background:#1E293B !important;
    border-radius:10px;
}

/* Selected value */
div[data-baseweb="select"] span{
    color:white !important;
}

/* Placeholder */
div[data-baseweb="select"] input{
    color:white !important;
}

/* Dropdown arrow */
div[data-baseweb="select"] svg{
    color:white !important;
}

/* Dropdown menu */
ul{
    background:#1E293B !important;
}

li{
    color:white !important;
}

li:hover{
    background:#334155 !important;
}

/* ===========================
   Number Inputs
=========================== */

.stNumberInput input{
    background:#1E293B !important;
    color:white !important;
}

/* ===========================
   Metric Cards
=========================== */

div[data-testid="metric-container"]{

    background:#1E293B;

    border-radius:15px;

    padding:18px;

    border:1px solid #374151;

}

/* Metric Label */

div[data-testid="metric-container"] label{

    color:#D1D5DB !important;

    font-size:16px;

}

/* Metric Value */

div[data-testid="metric-container"] div{

    color:white !important;

    font-size:30px;

    font-weight:bold;

}

/* ===========================
   Progress
=========================== */

.stProgress > div > div{

    border-radius:20px;

}

/* ===========================
   Alerts
=========================== */

div[data-testid="stAlert"]{

    border-radius:12px;

}

/* ===========================
   Divider
=========================== */

hr{

    border:1px solid #374151;

}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Team and City Lists
# -----------------------------
teams = [
    'Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Kings XI Punjab',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Delhi Capitals'
]

cities = [
    'Hyderabad',
    'Bangalore',
    'Mumbai',
    'Indore',
    'Kolkata',
    'Delhi',
    'Chandigarh',
    'Jaipur',
    'Chennai',
    'Cape Town',
    'Port Elizabeth',
    'Durban',
    'Centurion',
    'East London',
    'Johannesburg',
    'Kimberley',
    'Bloemfontein',
    'Ahmedabad',
    'Cuttack',
    'Nagpur',
    'Dharamsala',
    'Visakhapatnam',
    'Pune',
    'Raipur',
    'Ranchi',
    'Abu Dhabi',
    'Sharjah',
    'Mohali',
    'Bengaluru'
]

logo_paths = {
    "Chennai Super Kings": "assets/logos/csk.png",
    "Delhi Capitals": "assets/logos/dc.jpg",
    "Kolkata Knight Riders": "assets/logos/kkr.jpg",
    "Mumbai Indians": "assets/logos/mi.jpg",
    "Kings XI Punjab": "assets/logos/pbks.png",
    "Royal Challengers Bangalore": "assets/logos/rcb.jpg",
    "Rajasthan Royals": "assets/logos/rr.png",
    "Sunrisers Hyderabad": "assets/logos/srh.jpg"
}

# -----------------------------
# Load Model
# -----------------------------
pipe = pickle.load(open('pipe.pkl', 'rb'))

# -----------------------------
# Title
# -----------------------------
st.title("🏏 IPL Win Predictor")
st.markdown("### Predict the winning probability of the chasing team")

st.divider()

# -----------------------------
# Team Selection
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox(
        "🏏 Batting Team",
        sorted(teams)
    )

with col2:
    bowling_team = st.selectbox(
        "🎯 Bowling Team",
        sorted(teams)
    )

if batting_team == bowling_team:
    st.error("Batting Team and Bowling Team cannot be the same.")
    st.stop()


# -----------------------------
# Team Logos
# -----------------------------
st.divider()

st.subheader("🏏 Match")

logo_col1, logo_col2, logo_col3 = st.columns([3, 1, 3])

with logo_col1:
    st.image(logo_paths[batting_team], width=170)
    st.markdown(
        f"<h4 style='text-align:center'>{batting_team}</h4>",
        unsafe_allow_html=True
    )

with logo_col2:
    st.markdown(
        """
        <h1 style='text-align:center; margin-top:70px;'>VS</h1>
        """,
        unsafe_allow_html=True
    )

with logo_col3:
    st.image(logo_paths[bowling_team], width=170)
    st.markdown(
        f"<h4 style='text-align:center'>{bowling_team}</h4>",
        unsafe_allow_html=True
    )

st.divider()    

# -----------------------------
# City
# -----------------------------
selected_city = st.selectbox(
    "📍 Host City",
    sorted(cities)
)

# -----------------------------
# Target
# -----------------------------
target = st.number_input(
    "🎯 Target Score",
    min_value=1,
    step=1
)

st.divider()

# -----------------------------
# Match Inputs
# -----------------------------
col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input(
        "Current Score",
        min_value=0,
        step=1
    )

with col4:
    overs = st.number_input(
        "Overs Completed",
        min_value=0.0,
        max_value=20.0,
        step=0.1,
        format="%.1f"
    )

with col5:
    wickets = st.number_input(
        "Wickets Out",
        min_value=0,
        max_value=10,
        step=1
    )

st.divider()

# -----------------------------
# Prediction Button
# -----------------------------
if st.button("🚀 Predict Winning Probability", use_container_width=True):

    over = int(overs)
    ball = int(round((overs - over) * 10))

    if ball > 5:
        st.error("❌ Invalid Overs! Decimal part must be between 0 and 5.")
        st.stop()

    balls_bowled = over * 6 + ball
    balls_left = 120 - balls_bowled

    runs_left = target - score
    wickets_left = 10 - wickets

    if runs_left < 0:
        st.success(f"🎉 {batting_team} has already won the match!")
        st.stop()

    if balls_left < 0:
        st.error("Invalid overs entered.")
        st.stop()

    # Current Run Rate
    if balls_bowled == 0:
        crr = 0
    else:
        crr = score * 6 / balls_bowled

    # Required Run Rate
    if balls_left == 0:
        rrr = 0
    else:
        rrr = runs_left * 6 / balls_left

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [selected_city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets': [wickets_left],
        'total_runs_x': [target],
        'crr': [crr],
        'rrr': [rrr]
    })

    result = pipe.predict_proba(input_df)

    loss = result[0][0]
    win = result[0][1]

    # -----------------------------
    # Match Summary
    # -----------------------------
    st.subheader("📊 Match Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric("Runs Left", runs_left)
    c2.metric("Balls Left", balls_left)
    c3.metric("Wickets Left", wickets_left)

    c4, c5 = st.columns(2)

    c4.metric("Current RR", f"{crr:.2f}")
    c5.metric("Required RR", f"{rrr:.2f}")

    st.divider()

    # -----------------------------
    # Prediction
    # -----------------------------
    st.subheader("🏆 Winning Probability")

    st.write(f"### 🏏 {batting_team}")

    st.progress(float(win))

    st.success(f"{win*100:.2f}%")

    st.write(f"### 🎯 {bowling_team}")

    st.progress(float(loss))

    st.error(f"{loss*100:.2f}%")

    st.divider()

    if win > loss:
        st.balloons()
        st.success(f"🎉 {batting_team} is more likely to win!")
    else:
        st.info(f"🏏 {bowling_team} is more likely to defend the target!")