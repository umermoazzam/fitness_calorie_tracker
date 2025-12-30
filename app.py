import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import date

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
    try:
        df = pd.read_csv("data/user.csv")
        return df if not df.empty else pd.DataFrame(columns=["username", "password"])
    except:
        return pd.DataFrame(columns=["username", "password"])

def save_user(username, password):
    df = load_users()
    df = pd.concat([df, pd.DataFrame([[username, password]], columns=df.columns)])
    df.to_csv("data/user.csv", index=False)
    load_users.clear()

# =========================
# DAILY LOG
# =========================
def save_daily_log(intake=0, burned=0):
    today = date.today().isoformat()
    try:
        df = pd.read_csv("data/daily_log.csv")
    except:
        df = pd.DataFrame(columns=["date", "intake", "burned"])

    if today in df["date"].values:
        df.loc[df["date"] == today, "intake"] += intake
        df.loc[df["date"] == today, "burned"] += burned
    else:
        df = pd.concat([
            df,
            pd.DataFrame([[today, intake, burned]], columns=df.columns)
        ])

    df.to_csv("data/daily_log.csv", index=False)

# =========================
# LOGIN / SIGNUP
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
                st.session_state.username = username
                st.success("Login successful ✅")
                st.rerun()
            else:
                st.error("Invalid username or password ❌")

    else:
        if st.button("Signup"):
            if not username or not password:
                st.error("Please fill all fields ❌")
            elif username in users_df["username"].values:
                st.error("Username already exists ❌")
            else:
                save_user(username, password)
                st.success("Signup successful! Now login.")
                st.rerun()

# =========================
# MAIN APP
# =========================
else:
    # Header username (top-right)
    st.markdown(
        f"""
        <div style="display:flex; justify-content:flex-end; font-size:18px; font-weight:600;">
            👋 Hi, {st.session_state.username}
        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # LOAD FOOD DATA
    # =========================
    @st.cache_data
    def load_food_data():
        try:
            return pd.read_csv("data/food_calories.csv")
        except:
            return pd.DataFrame(columns=["Food", "Calories"])

    food_df = load_food_data()

    # =========================
    # SIDEBAR
    # =========================
    st.sidebar.title("📌 Dashboard")
    menu = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "🍎 Calorie Intake", "🏃 Calories Burned", "📊 Progress", "⚖️ Weight Goal"]
    )
    st.sidebar.button("🚪 Logout", on_click=lambda: st.session_state.clear())

    # =========================
    # HOME
    # =========================
    if menu == "🏠 Home":
        st.title("🏋️ Fitness Calorie Tracker")
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
            result = food_df[food_df["Food"].str.lower() == food_name.lower().strip()]
            if not result.empty:
                calories_100g = result.iloc[0]["Calories"]
                total = (calories_100g / 100) * quantity
                st.success(f"🔥 Estimated Calories: {total:.2f} kcal")
                save_daily_log(intake=total)
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
            save_daily_log(burned=calories)

    # =========================
    # PROGRESS
    # =========================
    elif menu == "📊 Progress":
        st.header("📊 Fitness Progress")

        try:
            df = pd.read_csv("data/daily_log.csv")
        except:
            st.warning("No data available yet.")
            st.stop()

        today = date.today().isoformat()
        today_data = df[df["date"] == today]

        intake = today_data["intake"].sum() if not today_data.empty else 0
        burned = today_data["burned"].sum() if not today_data.empty else 0

        col1, col2 = st.columns(2)
        col1.metric("🔥 Intake", f"{intake:.0f} kcal")
        col2.metric("🏃 Burned", f"{burned:.0f} kcal")

        fig, ax = plt.subplots()
        ax.pie(
            [intake, burned],
            labels=["Intake", "Burned"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title("Today Calories")
        st.pyplot(fig)

        df["date"] = pd.to_datetime(df["date"])
        weekly = df.tail(7)
        st.subheader("📅 Last 7 Days")
        st.bar_chart(weekly.set_index("date")[["intake", "burned"]])

    # =========================
    # WEIGHT GOAL
    # =========================
    elif menu == "⚖️ Weight Goal":
        st.header("⚖️ Weight Gain / Loss Planner")

        current_weight = st.number_input("Current Weight (kg)", min_value=1, value=70)
        target_weight = st.number_input("Target Weight (kg)", min_value=1, value=72)
        days = st.number_input("Time Period (days)", min_value=1, value=30)

        if st.button("Calculate Plan"):
            diff = target_weight - current_weight
            total_calories = diff * 7700
            daily_calories = total_calories / days

            if diff > 0:
                st.success(f"You need a **daily surplus of {daily_calories:.0f} kcal** to gain {diff:.1f} kg.")
                st.subheader("🍽️ Recommended High-Calorie Foods")
                st.table(food_df.sort_values("Calories", ascending=False).head(5))
                st.info("Tip: Eat frequently, add nuts, milk, bananas, peanut butter.")
            elif diff < 0:
                st.warning(f"You need a **daily deficit of {abs(daily_calories):.0f} kcal** to lose {abs(diff):.1f} kg.")
                st.subheader("🥗 Recommended Low-Calorie Foods")
                st.table(food_df.sort_values("Calories").head(5))
                st.info("Tip: Walk daily, avoid sugar, eat vegetables & lean protein.")
            else:
                st.info("You are already at your target weight ✅")
