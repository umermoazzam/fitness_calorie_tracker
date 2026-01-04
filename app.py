import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import date
from model.weight_model import predict_weight


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
def save_daily_log(intake=0, burned=0, weight=None, steps=0, distance=0.0, water_intake=0.0, sleep_hours=0.0, notes=""):
    today = date.today().isoformat()
    try:
        df = pd.read_csv("data/daily_log.csv")
    except:
        df = pd.DataFrame(columns=["date", "weight", "intake", "burned", "steps", "distance", "water_intake", "sleep_hours", "notes"])

    if today in df["date"].values:
        if weight is not None:
            df.loc[df["date"] == today, "weight"] = weight
        df.loc[df["date"] == today, "intake"] += intake
        df.loc[df["date"] == today, "burned"] += burned
        df.loc[df["date"] == today, "steps"] += steps
        df.loc[df["date"] == today, "distance"] += distance
        df.loc[df["date"] == today, "water_intake"] += water_intake
        df.loc[df["date"] == today, "sleep_hours"] += sleep_hours
        if notes:
            df.loc[df["date"] == today, "notes"] = notes
    else:
        df = pd.concat([
            df,
            pd.DataFrame([[today, weight, intake, burned, steps, distance, water_intake, sleep_hours, notes]], 
                         columns=df.columns)
        ])

    df.to_csv("data/daily_log.csv", index=False)


# =========================
# LOGIN / SIGNUP
# =========================

if not st.session_state.logged_in:
    # 🏋️ PROJECT TITLE
    st.markdown(
        """
        <h1 style="text-align:center; color:#ff4b4b;">
        🏋️ Fitness Calorie Tracker & Weight Prediction System
        </h1>
        <h4 style="text-align:center; color:gray;">
        Machine Learning Project
        </h4>
        <hr>
        """,
        unsafe_allow_html=True
    )


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
        ["🏠 Home", "🍎 Calorie Intake", "🏃 Calories Burned", "⚖️ Weight Goal", "📊 Progress"]
    )
    st.sidebar.button("🚪 Logout", on_click=lambda: st.session_state.clear())
    
    # =========================
    # DEVELOPER INFO
    # =========================
    st.sidebar.markdown(
    """
    ---
    **Developed by:**  
    22-NTU-CS-1227 (Umer Moazzam)  
    22-NTU-CS-1229 (Wasif Ali)  
    22-NTU-CS-1191 (Bilal Afzal)
    """
)

    # =========================
    # HOME
    # =========================
    if menu == "🏠 Home":
        st.title("🏋️ Fitness Calorie Tracker")

        try:
            df = pd.read_csv("data/daily_log.csv")
        except:
            df = pd.DataFrame(columns=["date", "weight", "intake", "burned", "steps", "distance", "water_intake", "sleep_hours", "notes"])

        today = date.today().isoformat()
        today_data = df[df["date"] == today]

        intake = today_data["intake"].sum() if not today_data.empty else 0
        burned = today_data["burned"].sum() if not today_data.empty else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("🔥 Calories Burned Today", f"{burned:.0f} kcal", delta=f"{burned-500:.0f} kcal")
        col2.metric("🍽️ Calories Intake Today", f"{intake:.0f} kcal", delta=f"{intake-2200:.0f} kcal")
        col3.metric("⚖️ Current Weight", f"{today_data['weight'].values[0]:.1f} kg" if not today_data.empty and today_data['weight'].values[0] else "N/A")


    # =========================
    # CALORIE INTAKE
    # =========================
    elif menu == "🍎 Calorie Intake":
        st.header(" Food Intake Analyzer")

        food_input = st.text_input("Enter Food Names (comma separated)")
        quantities_input = st.text_input("Enter Quantities (grams, comma separated, same order)")

        target_calories = st.number_input("Target Calories (optional)", min_value=0.0, value=0.0)

        if st.button("Calculate Intake"):
            if not food_input.strip():
                st.error("Please enter at least one food ❌")
            else:
                food_list = [f.strip() for f in food_input.split(",")]
                if quantities_input.strip():
                    quantity_list = [float(q.strip()) for q in quantities_input.split(",")]
                    if len(quantity_list) != len(food_list):
                        st.error("Number of quantities must match number of foods ❌")
                        st.stop()
                else:
                    quantity_list = [100] * len(food_list)  # default 100g if no quantity

                total_calories = 0
                st.subheader("🍴 Food Calories")
                for food, qty in zip(food_list, quantity_list):
                    result = food_df[food_df["Food"].str.lower() == food.lower()]
                    if not result.empty:
                        calories_per_100g = result.iloc[0]["Calories"]
                        calories = (calories_per_100g / 100) * qty
                        total_calories += calories
                        st.write(f"{food} ({qty} g): {calories:.2f} kcal")
                        save_daily_log(intake=calories)
                    else:
                        st.warning(f"{food} not found in database ❌")

                st.success(f"🔥 Total Calories: {total_calories:.2f} kcal")

                if target_calories > 0:
                    st.subheader("📌 Quantities for Target Calories")
                    for food in food_list:
                        result = food_df[food_df["Food"].str.lower() == food.lower()]
                        if not result.empty:
                            calories_per_100g = result.iloc[0]["Calories"]
                            suggested_quantity = (target_calories / calories_per_100g) * 100
                            st.info(f"{food}: approx {suggested_quantity:.2f} g needed to reach {target_calories} kcal")


    # =========================
    # CALORIES BURNED
    # =========================
    elif menu == "🏃 Calories Burned":
        st.header("🏃 Walking Calorie Estimator")

        weight = st.number_input("Weight (kg)", min_value=1, value=70)
        distance = st.number_input("Distance (km, optional)", min_value=0.0, step=0.1, value=0.0)
        target_calories = st.number_input("Target Calories to Burn (optional)", min_value=0.0, value=0.0)

        if st.button("Calculate"):
            # Calculate calories from distance
            if distance > 0:
                calories = weight * distance * 0.9
                st.success(f"✅ Calories Burned for {distance} km: {calories:.2f} kcal")
                save_daily_log(burned=calories)

            # Calculate distance required for target calories
            if target_calories > 0:
                if weight > 0:
                    required_distance = target_calories / (weight * 0.9)
                    st.info(f"🏃 Distance required to burn {target_calories:.2f} kcal: {required_distance:.2f} km")
                else:
                    st.error("Weight must be greater than 0 to calculate required distance.")

            # If both provided, show both results
            if distance > 0 and target_calories > 0:
                st.write("✅ Both calculations completed!")


  
    # =========================
    # WEIGHT GOAL
    # =========================
    elif menu == "⚖️ Weight Goal":
        st.header("⚖️ Weight Gain / Loss Planner")

        current_weight = st.number_input("Current Weight (kg)", min_value=1, value=70)
        target_weight = st.number_input("Target Weight (kg)", min_value=1, value=72)
        days = st.number_input("Time Period (days)", min_value=1, value=30)

        if st.button("Calculate Plan"):
            # Save current weight to daily log
            save_daily_log(weight=current_weight)
            
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



  