import pandas as pd
import streamlit as st

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Fitness Calorie Tracker", page_icon="🔥", layout="wide")

# =========================
# SESSION STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================
# LOAD USERS
# =========================
@st.cache_data
def load_users():
    return pd.read_csv("data/users.csv")

def save_user(username, password):
    df = load_users()
    new_user = pd.DataFrame([[username, password]], columns=["username", "password"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv("data/users.csv", index=False)

# =========================
# LOGIN / SIGNUP SCREEN
# =========================
if not st.session_state.logged_in:
    st.title("🔐 Login / Signup")

    option = st.radio("Choose Option", ["Login", "Signup"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    users_df = load_users()

    if option == "Login":
        if st.button("Login"):
            user = users_df[
                (users_df["username"] == username) &
                (users_df["password"] == password)
            ]
            if not user.empty:
                st.session_state.logged_in = True
                st.success("Login successful ✅")
                st.rerun()
            else:
                st.error("Invalid username or password ❌")

    else:  # Signup
        if st.button("Signup"):
            if username in users_df["username"].values:
                st.error("Username already exists ❌")
            else:
                save_user(username, password)
                st.success("Signup successful! Now login.")

# =========================
# MAIN APP (AFTER LOGIN)
# =========================
else:
    # =========================
    # LOAD FOOD CALORIE CSV
    # =========================
    @st.cache_data
    def load_food_data():
        return pd.read_csv("data/food_calories.csv")

    food_df = load_food_data()

    # =========================
    # STYLES
    # =========================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

    # =========================
    # SIDEBAR
    # =========================
    st.sidebar.title("📌 Dashboard")
    menu = st.sidebar.radio("Navigation:", ["🏠 Home", "🍎 Calorie Intake", "🏃 Calories Burned"])
    st.sidebar.button("🚪 Logout", on_click=lambda: st.session_state.update({"logged_in": False}))

    # =========================
    # HOME
    # =========================
    if menu == "🏠 Home":
        st.title("🏋️ Fitness Calorie Tracker & Prediction System")
        st.markdown("---")
        st.write("""
        Track your daily activity and diet with this system:
        • Calorie Intake  
        • Calories Burned
        """)
        col1, col2 = st.columns(2)
        col1.metric("Target Burn", "500 kcal/day")
        col2.metric("Target Intake", "2200 kcal/day")

    # =========================
    # CALORIE INTAKE
    # =========================
    elif menu == "🍎 Calorie Intake":
        st.header("🍎 Food Intake Analyzer")
        food_name = st.text_input("Food Name")
        quantity = st.number_input("Quantity (grams)", min_value=1, value=100)

        if st.button("Predict Calories"):
            result = food_df[food_df["Food"].str.lower() == food_name.lower()]
            if not result.empty:
                calories_per_100g = result.iloc[0]["Calories"]
                total = (calories_per_100g / 100) * quantity
                st.success(f"🔥 Estimated Calories: {total:.2f} kcal")
            else:
                st.error("Food not found ❌")

    # =========================
    # CALORIES BURNED
    # =========================
    elif menu == "🏃 Calories Burned":
        st.header("🏃 Walking Calorie Estimator")
        weight = st.number_input("Weight (kg)", min_value=1, value=70)
        distance = st.number_input("Distance (km)", min_value=0.1, step=0.1, value=1.0)

        if st.button("Calculate"):
            calories = weight * distance * 0.9
            st.success(f"✅ Calories Burned: {calories:.2f} kcal")
