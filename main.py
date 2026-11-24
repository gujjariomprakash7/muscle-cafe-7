import streamlit as st
from datetime import time, date

import pandas as pd
import plotly.express as px

from database import (
    create_table,
    save_profile,
    get_latest_profile,
    save_body_measurement,
    get_body_measurements,
    save_workout_log,
    get_workout_logs,
    register_account,
    authenticate_user,
)
from logic.workout import (
    generate_workout,
    get_focus_options,
    get_focus_education,
    MUSCLE_GROUPS,
    EQUIPMENT_OPTIONS,
)
from logic.plan import generate_weekly_plan, WEEKDAYS
from nutrition import DIET_OPTIONS, build_nutrition_plan


# -------------------------------------------------
# PAGE SETUP
# -------------------------------------------------
st.set_page_config(
    page_title="Muscle Cafe",
    page_icon="💪",
    layout="wide",
)

# Create the SQLite table if it does not already exist.
create_table()


# -------------------------------------------------
# VISUAL DESIGN SYSTEM + CHART HELPERS
# -------------------------------------------------
CHART_COLORS = [
    "#B7F34A", "#22D3EE", "#A78BFA", "#FB7185", "#F59E0B",
    "#34D399", "#60A5FA", "#F472B6", "#C084FC", "#F97316",
]

PLOTLY_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "scrollZoom": True,
    "responsive": True,
}

def style_figure(fig, height=360):
    """Apply a consistent dark, high-contrast style to interactive Plotly charts."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, Segoe UI, sans-serif", "color": "#E8EDF2", "size": 12},
        title={"font": {"size": 17, "color": "#F8FAFC"}, "x": 0.02, "xanchor": "left"},
        margin={"l": 18, "r": 18, "t": 58, "b": 24},
        height=height,
        hoverlabel={"bgcolor": "#17232D", "font": {"color": "#FFFFFF"}},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
        hovermode="x unified",
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="rgba(148,163,184,0.18)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(148,163,184,0.15)", zeroline=False)
    return fig

def filter_chart_period(frame, date_column, period):
    """Filter a chart dataframe without changing the saved source records."""
    if frame.empty or period == "All time":
        return frame.copy()
    result = frame.copy()
    result[date_column] = pd.to_datetime(result[date_column])
    days = 30 if period == "Last 30 days" else 90
    cutoff = pd.Timestamp(date.today() - pd.Timedelta(days=days - 1))
    return result[result[date_column] >= cutoff]

st.markdown(
    """
    <style>
      .stApp {
        background: radial-gradient(circle at 8% 0%, rgba(34,211,238,.08), transparent 27%),
                    radial-gradient(circle at 92% 4%, rgba(183,243,74,.07), transparent 25%),
                    #111B24;
      }
      .block-container { padding-top: 1.65rem; padding-bottom: 3rem; max-width: 1480px; }
      h1 { font-weight: 800 !important; letter-spacing: -.035em; }
      h2, h3 { font-weight: 700 !important; letter-spacing: -.02em; }
      [data-testid="stSidebar"] { background: linear-gradient(180deg, #17232D 0%, #111B24 100%); border-right: 1px solid rgba(148,163,184,.13); }
      [data-testid="stMetric"] { background: linear-gradient(145deg, rgba(32,45,55,.96), rgba(25,38,48,.96)); border: 1px solid rgba(183,243,74,.18); padding: 15px 17px; border-radius: 16px; box-shadow: 0 8px 24px rgba(0,0,0,.12); }
      [data-testid="stMetricLabel"] { color: #AFC0CB !important; }
      [data-testid="stMetricValue"] { color: #F8FAFC !important; font-weight: 750; }
      div[data-testid="stVerticalBlockBorderWrapper"] { border-color: rgba(148,163,184,.2); border-radius: 16px; }
      .stButton > button, .stFormSubmitButton > button { border: 0; border-radius: 11px; background: linear-gradient(100deg, #B7F34A, #7DDC70); color: #14202A; font-weight: 750; transition: transform .15s ease, filter .15s ease; }
      .stButton > button:hover, .stFormSubmitButton > button:hover { filter: brightness(1.06); transform: translateY(-1px); color: #101820; border: 0; }
      .stDownloadButton > button { border-radius: 11px; border: 1px solid rgba(34,211,238,.55); color: #DFFBFF; background: rgba(34,211,238,.08); font-weight: 650; }
      [data-testid="stExpander"] { border: 1px solid rgba(148,163,184,.18); border-radius: 14px; }
      [data-testid="stDataFrame"] { border: 1px solid rgba(148,163,184,.16); border-radius: 12px; overflow: hidden; }
      div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, textarea { border-radius: 10px !important; }
      .mc-eyebrow { color: #B7F34A; font-size: .76rem; font-weight: 800; letter-spacing: .16em; text-transform: uppercase; margin-bottom: .25rem; }
      .mc-subtitle { color: #B5C2CC; font-size: .98rem; margin-top: -.45rem; margin-bottom: 1rem; }
    </style>
    <div class="mc-eyebrow">Muscle Cafe · Build Strength. Fuel Life.</div>
    """,
    unsafe_allow_html=True,
)


# -------------------------------------------------
# ACCOUNT SIGN-IN / REGISTRATION
# -------------------------------------------------
if "account_id" not in st.session_state:
    st.markdown("# ☕ Welcome to Muscle Cafe")
    st.markdown("Create an account or sign in to access your personal fitness space.")
    login_tab, register_tab = st.tabs(["Sign in", "Create account"])

    with login_tab:
        with st.form("account_login_form"):
            login_email = st.text_input("Email address", key="login_email").strip()
            login_password = st.text_input("Password", type="password", key="login_password")
            login_submitted = st.form_submit_button("Sign in", type="primary", use_container_width=True)

        if login_submitted:
            account = authenticate_user(login_email, login_password)
            if account:
                st.session_state["account_id"] = account["id"]
                st.session_state["account_email"] = account["email"]
                st.rerun()
            else:
                st.error("Email or password is incorrect. Please try again.")

    with register_tab:
        st.caption("Use an email address you can access. Passwords must be at least 8 characters.")
        with st.form("account_register_form"):
            register_email = st.text_input("Email address", key="register_email").strip()
            register_password = st.text_input("Create password", type="password", key="register_password")
            confirm_password = st.text_input("Confirm password", type="password", key="confirm_password")
            register_submitted = st.form_submit_button("Create my account", type="primary", use_container_width=True)

        if register_submitted:
            if register_password != confirm_password:
                st.error("The passwords do not match.")
            else:
                new_account_id, register_error = register_account(register_email, register_password)
                if new_account_id is not None:
                    st.session_state["account_id"] = new_account_id
                    st.session_state["account_email"] = register_email.lower().strip()
                    st.success("Account created. Welcome to Muscle Cafe!")
                    st.rerun()
                else:
                    st.error(register_error or "Your account could not be created.")

    st.info("Your profile, measurements and workout history are separated by account on this app instance.")
    st.stop()

account_id = int(st.session_state["account_id"])

# -------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------
st.sidebar.title("☕ Muscle Cafe")
st.sidebar.caption("Build Strength. Fuel Life.")
st.sidebar.caption(f"Signed in: {st.session_state.get('account_email', '')}")
if st.sidebar.button("Log out", use_container_width=True):
    # Clear widget state as well as credentials before another person signs in.
    for state_key in list(st.session_state.keys()):
        del st.session_state[state_key]
    st.rerun()

page = st.sidebar.radio(
    "Navigate",
    ["Home", "My Profile", "Workout Planner", "Weekly Plan", "Nutrition Planner", "Progress Tracker"],
)


# -------------------------------------------------
# HOME PAGE — LIVE DASHBOARD
# -------------------------------------------------
if page == "Home":
    st.title("☕ Muscle Cafe Dashboard")
    st.caption("Build Strength. Fuel Life. Review your training and check-ins in one place.")

    profile = get_latest_profile(account_id)
    dashboard_body_records = get_body_measurements(account_id)
    dashboard_workout_records = get_workout_logs(account_id)

    if profile is None:
        st.info("Welcome to Muscle Cafe! Start by saving your fitness profile.")
        st.write(
            "Once you save a profile and start recording check-ins and workouts, "
            "this dashboard will show your real progress data here."
        )
    else:
        st.subheader(f"Welcome back, {profile[1]}!")
        profile_col1, profile_col2, profile_col3 = st.columns(3)
        profile_col1.metric("Main goal", profile[6])
        profile_col2.metric("Experience", profile[5])
        profile_col3.metric("Food preference", profile[7])

        # Calculate summary metrics only from saved records.
        body_df_home = pd.DataFrame(dashboard_body_records)
        workout_df_home = pd.DataFrame(dashboard_workout_records)

        latest_weight_text = "No check-in yet"
        weight_change_text = "Not enough data"
        checkin_count = len(dashboard_body_records)
        if not body_df_home.empty:
            body_df_home["entry_date"] = pd.to_datetime(body_df_home["entry_date"])
            body_df_home = body_df_home.sort_values(["entry_date", "id"])
            latest_weight = float(body_df_home.iloc[-1]["weight_kg"])
            latest_weight_text = f"{latest_weight:.1f} kg"
            if len(body_df_home) >= 2:
                first_weight = float(body_df_home.iloc[0]["weight_kg"])
                change = latest_weight - first_weight
                weight_change_text = f"{change:+.1f} kg since first check-in"

        workout_entries = len(dashboard_workout_records)
        training_days_count = 0
        recent_7_day_entries = 0
        if not workout_df_home.empty:
            workout_df_home["entry_date"] = pd.to_datetime(workout_df_home["entry_date"])
            training_days_count = int(workout_df_home["entry_date"].dt.date.nunique())
            seven_days_ago = pd.Timestamp(date.today() - pd.Timedelta(days=6))
            recent_7_day_entries = int((workout_df_home["entry_date"] >= seven_days_ago).sum())

        st.divider()
        metric1, metric2, metric3, metric4 = st.columns(4)
        metric1.metric("Latest body weight", latest_weight_text)
        metric2.metric("Body check-ins", checkin_count)
        metric3.metric("Workout entries", workout_entries)
        metric4.metric("Training days logged", training_days_count)
        st.caption(weight_change_text)

        st.markdown("### Your training analytics")
        control_col1, control_col2 = st.columns([1, 1])
        with control_col1:
            dashboard_period = st.selectbox(
                "Chart time range", ["All time", "Last 30 days", "Last 90 days"],
                key="dashboard_chart_period",
            )
        with control_col2:
            activity_metric = st.selectbox(
                "Compare training by", ["Working sets", "Exercise entries"],
                key="dashboard_activity_metric",
            )

        body_chart_data = filter_chart_period(body_df_home, "entry_date", dashboard_period)
        workout_chart_data = filter_chart_period(workout_df_home, "entry_date", dashboard_period)

        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.markdown("#### ⚖️ Body-weight trend")
            if not body_chart_data.empty:
                weight_chart_home = px.line(
                    body_chart_data, x="entry_date", y="weight_kg", markers=True,
                    color_discrete_sequence=["#B7F34A"],
                    labels={"entry_date": "Date", "weight_kg": "Weight (kg)"},
                    hover_data={"weight_kg": ":.1f"},
                )
                weight_chart_home.update_traces(line={"width": 3}, marker={"size": 9})
                weight_chart_home = style_figure(weight_chart_home, 350)
                st.plotly_chart(weight_chart_home, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                st.info("Your body-weight chart will appear after a check-in in the selected period.")

        with chart_col2:
            st.markdown("#### 🏋️ Training by muscle group")
            if not workout_chart_data.empty:
                if activity_metric == "Working sets":
                    group_summary = (
                        workout_chart_data.groupby("muscle_group", as_index=False)["sets"]
                        .sum().rename(columns={"sets": "Value"})
                    )
                    metric_label = "Recorded working sets"
                else:
                    group_summary = (
                        workout_chart_data.groupby("muscle_group", as_index=False)
                        .size().rename(columns={"size": "Value"})
                    )
                    metric_label = "Exercise entries"
                group_summary = group_summary.sort_values("Value", ascending=True)
                group_bar = px.bar(
                    group_summary, x="Value", y="muscle_group", orientation="h",
                    color="muscle_group", color_discrete_sequence=CHART_COLORS,
                    labels={"Value": metric_label, "muscle_group": "Muscle group"},
                    hover_data={"Value": True, "muscle_group": False},
                )
                group_bar.update_layout(showlegend=False, yaxis_title=None, xaxis_title=metric_label)
                group_bar = style_figure(group_bar, 350)
                st.plotly_chart(group_bar, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                st.info("Your training chart will appear after you log a workout.")

        pie_col, activity_col = st.columns(2)
        with pie_col:
            st.markdown("#### 🍩 Training distribution")
            if not workout_chart_data.empty:
                distribution = (
                    workout_chart_data.groupby("muscle_group", as_index=False)["sets"]
                    .sum().rename(columns={"sets": "Working sets"})
                )
                distribution = distribution[distribution["Working sets"] > 0]
                if not distribution.empty:
                    distribution_pie = px.pie(
                        distribution, names="muscle_group", values="Working sets", hole=0.58,
                        color_discrete_sequence=CHART_COLORS,
                        hover_data={"Working sets": True},
                    )
                    distribution_pie.update_traces(
                        textposition="inside", textinfo="percent",
                        hovertemplate="<b>%{label}</b><br>%{value} working sets<br>%{percent}<extra></extra>",
                        marker={"line": {"color": "#111B24", "width": 2}},
                    )
                    distribution_pie = style_figure(distribution_pie, 360)
                    distribution_pie.update_layout(showlegend=True, legend_title_text="Muscle group")
                    st.plotly_chart(distribution_pie, use_container_width=True, config=PLOTLY_CONFIG)
                else:
                    st.info("No working-set totals are available for the selected period.")
            else:
                st.info("Log workouts to see your training distribution.")

        with activity_col:
            st.markdown("#### 📅 Training activity by day")
            if not workout_chart_data.empty:
                daily_activity = (
                    workout_chart_data.assign(day=workout_chart_data["entry_date"].dt.strftime("%a"))
                    .groupby("day", as_index=False).size()
                    .rename(columns={"size": "Exercise entries"})
                )
                weekday_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                daily_activity["day"] = pd.Categorical(daily_activity["day"], categories=weekday_order, ordered=True)
                daily_activity = daily_activity.sort_values("day")
                daily_bar = px.bar(
                    daily_activity, x="day", y="Exercise entries",
                    color="Exercise entries", color_continuous_scale=["#203542", "#22D3EE", "#B7F34A"],
                    labels={"day": "Day", "Exercise entries": "Logged exercise entries"},
                )
                daily_bar.update_layout(coloraxis_showscale=False)
                daily_bar = style_figure(daily_bar, 360)
                st.plotly_chart(daily_bar, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                st.info("Your weekly activity chart will appear after logging workouts.")

        st.divider()
        recent_col1, recent_col2 = st.columns(2)
        with recent_col1:
            st.markdown("#### Recent workout activity")
            st.metric("Exercise entries in the last 7 days", recent_7_day_entries)
            if not workout_df_home.empty:
                recent_workouts = workout_df_home.sort_values(
                    ["entry_date", "id"], ascending=False
                ).copy()
                recent_workouts["entry_date"] = recent_workouts["entry_date"].dt.strftime("%Y-%m-%d")
                st.dataframe(
                    recent_workouts[["entry_date", "muscle_group", "exercise_name", "sets", "reps", "load_kg"]].head(5),
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("No workout entries recorded yet.")

        with recent_col2:
            st.markdown("#### Latest body check-in")
            if not body_df_home.empty:
                latest_body = body_df_home.iloc[-1]
                st.write(f"**Date:** {latest_body['entry_date'].date().isoformat()}")
                st.write(f"**Weight:** {float(latest_body['weight_kg']):.1f} kg")
                for column, label in (
                    ("waist_cm", "Waist"),
                    ("chest_cm", "Chest"),
                    ("arm_cm", "Upper arm"),
                    ("hip_cm", "Hip"),
                ):
                    value = latest_body.get(column)
                    if pd.notna(value):
                        st.write(f"**{label}:** {float(value):.1f} cm")
            else:
                st.info("No body measurements recorded yet.")

    st.divider()
    st.markdown("#### Your Muscle Cafe tools")
    tool_col1, tool_col2, tool_col3 = st.columns(3)
    tool_col1.write("**Workout Planner**\nTarget a muscle area and work around busy equipment.")
    tool_col2.write("**Weekly Plan**\nOrganise training days, weekly sets and recovery.")
    tool_col3.write("**Nutrition Planner**\nExplore meal ideas and estimated protein intake.")


# -------------------------------------------------
# MY PROFILE PAGE
# -------------------------------------------------
elif page == "My Profile":
    st.title("My Fitness Profile")
    st.write("Enter your details so Muscle Cafe can personalise your plan.")

    with st.form("profile_form"):
        name = st.text_input("Name")

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=21,
            step=1,
        )

        height = st.number_input(
            "Height (cm)",
            min_value=100.0,
            max_value=250.0,
            value=170.0,
            step=0.5,
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=30.0,
            max_value=300.0,
            value=65.0,
            step=0.5,
        )

        experience = st.selectbox(
            "Fitness experience",
            ["Beginner", "Intermediate", "Advanced"],
        )

        goal = st.selectbox(
            "Main fitness goal",
            ["Build Muscle", "Improve General Fitness", "Lose Fat"],
        )

        diet = st.selectbox(
            "Food preference",
            ["Vegetarian", "Eggetarian", "Non-Vegetarian", "Vegan"],
        )

        workout_minutes = st.selectbox(
            "Available workout time (minutes)",
            [20, 30, 45, 60, 90],
            index=2,
        )

        wake_time = st.time_input("Usual wake-up time", value=time(7, 0))
        sleep_time = st.time_input("Usual sleep time", value=time(23, 0))

        submitted = st.form_submit_button("Save Profile")

    if submitted:
        if not name.strip():
            st.error("Please enter your name before saving your profile.")
        else:
            profile_data = {
                "name": name.strip(),
                "age": int(age),
                "height": float(height),
                "weight": float(weight),
                "experience": experience,
                "goal": goal,
                "diet": diet,
                "workout_minutes": int(workout_minutes),
                "wake_time": wake_time.strftime("%H:%M"),
                "sleep_time": sleep_time.strftime("%H:%M"),
            }

            try:
                save_profile(profile_data, account_id)
                st.success("Your profile has been saved successfully!")
            except Exception as error:
                st.error(
                    "Your profile could not be saved. Check database.py, "
                    "especially the SQL INSERT placeholders."
                )
                st.exception(error)

    st.divider()
    st.subheader("Saved Profile")
    saved_profile = get_latest_profile(account_id)

    if saved_profile is None:
        st.info("No profile has been saved yet.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {saved_profile[1]}")
            st.write(f"**Age:** {saved_profile[2]}")
            st.write(f"**Height:** {saved_profile[3]} cm")
            st.write(f"**Weight:** {saved_profile[4]} kg")
            st.write(f"**Experience:** {saved_profile[5]}")
        with col2:
            st.write(f"**Goal:** {saved_profile[6]}")
            st.write(f"**Food preference:** {saved_profile[7]}")
            st.write(f"**Workout time:** {saved_profile[8]} minutes")
            st.write(f"**Wake-up time:** {saved_profile[9]}")
            st.write(f"**Sleep time:** {saved_profile[10]}")


# -------------------------------------------------
# WORKOUT PLANNER PAGE
# -------------------------------------------------
elif page == "Workout Planner":
    st.title("🏋️ Targeted Workout Planner")
    st.write(
        "Choose a muscle group and a specific muscle head or region to "
        "prioritise. Mark equipment that is busy or unavailable, and "
        "Muscle Cafe will suggest a session with alternatives and short "
        "exercise-learning notes."
    )

    profile = get_latest_profile(account_id)

    if profile is None:
        st.warning("Please open My Profile and save your profile first.")
    else:
        st.write(f"Welcome, **{profile[1]}**!")
        st.caption(
            f"Experience: {profile[5]}  |  "
            f"Goal: {profile[6]}  |  "
            f"Available time: {profile[8]} minutes"
        )

        muscle_group = st.selectbox(
            "Which muscle group do you want to train?",
            MUSCLE_GROUPS,
        )

        focus_options = ["All areas"] + get_focus_options(muscle_group)
        focus = st.selectbox(
            "Which area or muscle head do you want to prioritise?",
            focus_options,
        )

        focus_info = get_focus_education(muscle_group, focus)
        with st.expander("Learn about this muscle area", expanded=True):
            st.write(focus_info["summary"])
            st.caption(focus_info["limitation"])

        unavailable_equipment = st.multiselect(
            "Which equipment is busy or unavailable?",
            EQUIPMENT_OPTIONS,
            help=(
                "Select equipment you cannot use today. Exercises requiring "
                "that equipment will be excluded. Bodyweight options remain available."
            ),
        )

        st.caption(
            "Tip: You can select more than one unavailable equipment type. "
            "Bodyweight movements are kept as an option."
        )

        if st.button("Generate My Workout", type="primary"):
            try:
                workout_plan = generate_workout(
                    experience=profile[5],
                    goal=profile[6],
                    minutes=int(profile[8]),
                    muscle_group=muscle_group,
                    focus=focus,
                    unavailable_equipment=unavailable_equipment,
                )

                if not workout_plan:
                    st.warning(
                        "No suitable exercises were found for this selection. "
                        "Try choosing All areas or make more equipment available."
                    )
                else:
                    st.subheader(f"Your {muscle_group} Workout")
                    st.caption(
                        f"Priority: {focus}  |  "
                        f"Exercises selected: {len(workout_plan)}"
                    )

                    for number, exercise in enumerate(workout_plan, start=1):
                        with st.container(border=True):
                            st.markdown(f"### {number}. {exercise['name']}")

                            detail_col1, detail_col2, detail_col3 = st.columns(3)
                            detail_col1.write(
                                f"**Target area**\n\n{exercise['focus']}"
                            )
                            detail_col2.write(
                                f"**Movement type**\n\n{exercise['movement_type']}"
                            )
                            detail_col3.write(
                                f"**Equipment**\n\n{exercise['equipment']}"
                            )

                            st.write(
                                f"**Sets:** {exercise['sets']}  |  "
                                f"**Reps:** {exercise['reps']}"
                            )
                            st.write(
                                f"**Why this exercise fits:** {exercise['why_it_fits']}"
                            )
                            st.caption(
                                f"**Technique cue:** {exercise['coaching_cue']}"
                            )

                            if exercise["alternatives"]:
                                st.caption(
                                    "Other available alternatives for a similar movement: "
                                    + ", ".join(exercise["alternatives"])
                                )

                    workout_chart_df = pd.DataFrame(workout_plan)
                    st.markdown("#### 📊 Your session at a glance")
                    workout_chart_col1, workout_chart_col2 = st.columns(2)
                    with workout_chart_col1:
                        movement_mix = (
                            workout_chart_df.groupby("movement_type", as_index=False).size()
                            .rename(columns={"size": "Exercises"})
                        )
                        movement_pie = px.pie(
                            movement_mix, names="movement_type", values="Exercises", hole=0.58,
                            color_discrete_sequence=["#B7F34A", "#22D3EE", "#A78BFA"],
                            title="Movement mix",
                        )
                        movement_pie.update_traces(textposition="inside", textinfo="label+percent")
                        st.plotly_chart(style_figure(movement_pie, 300), use_container_width=True, config=PLOTLY_CONFIG)
                    with workout_chart_col2:
                        exercise_volume = workout_chart_df[["name", "sets"]].copy()
                        exercise_bar = px.bar(
                            exercise_volume, x="sets", y="name", orientation="h",
                            color="sets", color_continuous_scale=["#203542", "#22D3EE", "#B7F34A"],
                            title="Planned working sets by exercise",
                            labels={"sets": "Working sets", "name": "Exercise"},
                        )
                        exercise_bar.update_layout(coloraxis_showscale=False, yaxis={"categoryorder": "total ascending"})
                        st.plotly_chart(style_figure(exercise_bar, 300), use_container_width=True, config=PLOTLY_CONFIG)

                    st.info(
                        "Use alternatives as substitutions, not as extra exercises. "
                        "Most muscle heads work together, so labels such as long-head "
                        "or side-delt emphasis are learning guides, not promises of "
                        "complete isolation. Start with a controllable load and leave "
                        "about 2–3 good reps in reserve. Stop if you feel pain."
                    )
                    st.caption(
                        "Muscle Cafe is an educational workout-planning tool, not a "
                        "replacement for individual coaching or medical advice. "
                        "Ask a qualified trainer to check technique when learning "
                        "new or complex lifts."
                    )
                    st.success("Your workout is ready!")

            except Exception as error:
                st.error("Something went wrong while generating your workout.")
                st.exception(error)


# -------------------------------------------------
# WEEKLY TRAINING & RECOVERY PLAN PAGE
# -------------------------------------------------
elif page == "Weekly Plan":
    st.title("📅 Weekly Training & Recovery Planner")
    st.write(
        "Create a weekly split around the days you are available, choose one "
        "muscle group to prioritise, and review estimated direct working sets "
        "and rest days."
    )

    profile = get_latest_profile(account_id)

    if profile is None:
        st.warning("Please open My Profile and save your profile first.")
    else:
        st.caption(
            f"Experience: {profile[5]}  |  Goal: {profile[6]}  |  "
            f"Workout time per session: {profile[8]} minutes"
        )

        days_per_week = st.selectbox(
            "How many days can you train each week?",
            [2, 3, 4, 5, 6],
            index=1,
        )

        default_days_by_frequency = {
            2: ["Monday", "Thursday"],
            3: ["Monday", "Wednesday", "Friday"],
            4: ["Monday", "Tuesday", "Thursday", "Saturday"],
            5: ["Monday", "Tuesday", "Thursday", "Friday", "Saturday"],
            6: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        }

        training_days = st.multiselect(
            "Choose the days you are available to train",
            WEEKDAYS,
            default=default_days_by_frequency[days_per_week],
            max_selections=days_per_week,
        )

        priority_muscle = st.selectbox(
            "Which muscle group do you want to prioritise this week?",
            MUSCLE_GROUPS,
        )

        priority_focus = st.selectbox(
            "Which part of that muscle do you want to emphasise?",
            ["All areas"] + get_focus_options(priority_muscle),
        )

        focus_info = get_focus_education(priority_muscle, priority_focus)
        with st.expander("Learn about your priority muscle", expanded=False):
            st.write(focus_info["summary"])
            st.caption(focus_info["limitation"])

        if st.button("Build My Weekly Plan", type="primary"):
            if len(training_days) != days_per_week:
                st.error(
                    f"Please select exactly {days_per_week} training days "
                    "to match your chosen weekly frequency."
                )
            else:
                try:
                    plan = generate_weekly_plan(
                        training_days=training_days,
                        experience=profile[5],
                        priority_muscle=priority_muscle,
                    )

                    st.subheader("Your weekly split")
                    st.write(
                        f"Priority: **{priority_muscle}** — {priority_focus}"
                    )

                    for session in plan["sessions"]:
                        with st.container(border=True):
                            st.markdown(
                                f"### {session['day']} — {session['session']}"
                            )
                            for muscle, sets in session["sets_by_muscle"].items():
                                is_priority = muscle == priority_muscle
                                label = " ⭐ Priority" if is_priority else ""
                                st.write(
                                    f"**{muscle}{label}:** {sets} direct working sets"
                                )

                    st.subheader("Estimated weekly direct-set volume")
                    volume_rows = [
                        {"Muscle group": muscle, "Planned direct sets/week": sets}
                        for muscle, sets in sorted(plan["weekly_volume"].items())
                    ]
                    st.dataframe(
                        volume_rows,
                        use_container_width=True,
                        hide_index=True,
                    )
                    volume_chart_df = pd.DataFrame(volume_rows)
                    if not volume_chart_df.empty and volume_chart_df["Planned direct sets/week"].sum() > 0:
                        volume_chart_col1, volume_chart_col2 = st.columns(2)
                        with volume_chart_col1:
                            volume_bar = px.bar(
                                volume_chart_df.sort_values("Planned direct sets/week"),
                                x="Planned direct sets/week", y="Muscle group", orientation="h",
                                color="Muscle group", color_discrete_sequence=CHART_COLORS,
                                title="Weekly working sets by muscle",
                            )
                            volume_bar.update_layout(showlegend=False)
                            st.plotly_chart(style_figure(volume_bar, 350), use_container_width=True, config=PLOTLY_CONFIG)
                        with volume_chart_col2:
                            volume_pie = px.pie(
                                volume_chart_df, names="Muscle group", values="Planned direct sets/week",
                                hole=0.58, color_discrete_sequence=CHART_COLORS,
                                title="Share of planned weekly volume",
                            )
                            volume_pie.update_traces(textposition="inside", textinfo="percent")
                            st.plotly_chart(style_figure(volume_pie, 350), use_container_width=True, config=PLOTLY_CONFIG)

                    st.subheader("Recovery days")
                    if plan["rest_days"]:
                        st.write("**Non-training days:** " + ", ".join(plan["rest_days"]))
                    else:
                        st.write("No full rest days are left in this weekly schedule.")

                    if plan["recovery_warnings"]:
                        st.warning(
                            "These muscle groups appear on back-to-back selected days: "
                            + ", ".join(plan["recovery_warnings"])
                            + ". Consider moving a session or adding a rest day."
                        )
                    else:
                        st.success(
                            "The planned repeated muscle groups are not scheduled "
                            "on adjacent selected days. Adjust the plan if your "
                            "recovery, soreness or performance suggests you need more rest."
                        )

                    st.info(
                        "These are planning estimates for direct working sets, not "
                        "a log of completed training. Compound exercises also train "
                        "secondary muscles, but those indirect sets are not added to "
                        "the table. Start conservatively and adjust based on progress, "
                        "technique, sleep and recovery."
                    )
                    st.caption(
                        "Muscle Cafe provides general educational guidance for healthy "
                        "adults. It is not an individual medical or coaching prescription."
                    )

                except Exception as error:
                    st.error("The weekly plan could not be created.")
                    st.exception(error)


# -------------------------------------------------
# NUTRITION PLANNER PAGE
# -------------------------------------------------
elif page == "Nutrition Planner":
    st.title("🥗 Muscle Cafe - Nutrition Planner")
    st.write(
        "Get a practical food-first day plan using your saved weight, goal, "
        "food preference and usual waking hours. Food portions and protein "
        "values are estimates, not exact nutrition labels."
    )

    profile = get_latest_profile(account_id)

    if profile is None:
        st.warning("Please open My Profile and save your profile first.")
    else:
        st.caption(
            f"Saved goal: {profile[6]}  |  Saved weight: {profile[4]} kg  |  "
            f"Saved food preference: {profile[7]}"
        )

        saved_diet = profile[7] if profile[7] in DIET_OPTIONS else "Vegetarian"
        diet_choice = st.selectbox(
            "Food preference for this meal plan",
            DIET_OPTIONS,
            index=DIET_OPTIONS.index(saved_diet),
        )

        try:
            nutrition_plan = build_nutrition_plan(
                weight_kg=float(profile[4]),
                goal=profile[6],
                diet=diet_choice,
                wake_time=profile[9],
                sleep_time=profile[10],
            )

            st.subheader("Your estimated daily protein range")
            metric_col1, metric_col2 = st.columns(2)
            metric_col1.metric(
                "Suggested daily range",
                f"{nutrition_plan['protein_low_g']}–{nutrition_plan['protein_high_g']} g",
            )
            metric_col2.metric(
                "Example menu protein",
                f"{nutrition_plan['sample_protein_total_g']} g",
            )
            st.caption(
                "This broad range is an educational estimate for healthy adults "
                "who exercise. It is not a personalised medical prescription."
            )

            st.subheader("A practical sample day")
            st.write(
                "Meal times are suggestions based on your saved wake-up and sleep "
                "times. Move them around to suit classes, work, training and appetite."
            )

            for meal in nutrition_plan["meals"]:
                with st.container(border=True):
                    heading_col, protein_col = st.columns([3, 1])
                    heading_col.markdown(
                        f"### {meal['suggested_time']} — {meal['name']}"
                    )
                    protein_col.metric("Approx. protein", f"{meal['protein_g']} g")
                    st.write(meal["foods"])
                    st.caption(meal["why"])

            meal_chart_df = pd.DataFrame(nutrition_plan["meals"])
            if not meal_chart_df.empty:
                st.markdown("#### 🍽️ Protein across your sample meals")
                meal_chart_col1, meal_chart_col2 = st.columns(2)
                with meal_chart_col1:
                    meal_protein_bar = px.bar(
                        meal_chart_df, x="name", y="protein_g",
                        color="name", color_discrete_sequence=CHART_COLORS,
                        text="protein_g", title="Approximate protein per meal",
                        labels={"name": "Meal", "protein_g": "Protein (g)"},
                    )
                    meal_protein_bar.update_traces(texttemplate="%{text} g", textposition="outside")
                    meal_protein_bar.update_layout(showlegend=False)
                    st.plotly_chart(style_figure(meal_protein_bar, 330), use_container_width=True, config=PLOTLY_CONFIG)
                with meal_chart_col2:
                    meal_protein_pie = px.pie(
                        meal_chart_df, names="name", values="protein_g", hole=0.58,
                        color_discrete_sequence=CHART_COLORS, title="Protein contribution by meal",
                    )
                    meal_protein_pie.update_traces(textposition="inside", textinfo="label+percent")
                    st.plotly_chart(style_figure(meal_protein_pie, 330), use_container_width=True, config=PLOTLY_CONFIG)

            st.subheader("Optional protein add-on")
            booster_options = nutrition_plan["protein_boosters"]
            booster_labels = ["No extra add-on"] + [
                f"{item['name']} (+{item['protein_g']} g)"
                for item in booster_options
            ]
            selected_booster = st.selectbox(
                "Choose an extra option only if it suits your appetite and needs",
                booster_labels,
            )

            extra_protein = 0
            if selected_booster != "No extra add-on":
                selected_index = booster_labels.index(selected_booster) - 1
                extra_protein = booster_options[selected_index]["protein_g"]
                st.write(
                    f"Example menu plus this add-on: "
                    f"**{nutrition_plan['sample_protein_total_g'] + extra_protein} g protein**"
                )

            total_with_add_on = nutrition_plan["sample_protein_total_g"] + extra_protein
            if total_with_add_on < nutrition_plan["protein_low_g"]:
                st.info(
                    "This sample menu is below the lower end of the estimated range. "
                    "You can adjust portions or add another compatible protein food; "
                    "you do not need to force-feed or rely on supplements."
                )
            elif total_with_add_on > nutrition_plan["protein_high_g"]:
                st.info(
                    "This example is above the estimated range. That is not a target "
                    "to chase: portions can be adjusted to appetite and your overall diet."
                )
            else:
                st.success(
                    "This example menu falls within the estimated daily protein range."
                )

            st.subheader("A few practical nutrition habits")
            st.write(
                "- Include a protein source in each main meal.\n"
                "- Include vegetables or fruit and a carbohydrate source rather than focusing only on protein.\n"
                "- Drink fluids regularly and adjust for heat, activity and thirst.\n"
                "- Use food variety across the week; this is one sample day, not a rigid prescription."
            )

            st.info(
                "Muscle Cafe does not calculate a calorie target in this version. "
                "A responsible energy estimate needs more information about daily "
                "activity and other individual factors."
            )
            st.caption(
                "Protein estimates vary by brand, recipe, cooking method and portion. "
                "This planner is intended for generally healthy adults. If you have "
                "kidney disease, are pregnant, have a medical nutrition need, or have "
                "a history of disordered eating, get individual advice from a qualified "
                "doctor or registered dietitian before following protein targets."
            )

        except Exception as error:
            st.error("The nutrition plan could not be created.")
            st.exception(error)

# -------------------------------------------------
# PROGRESS TRACKER PAGE
# -------------------------------------------------
elif page == "Progress Tracker":
    st.title("📈 Progress Tracker")
    st.write(
        "Record body check-ins and workout performance so you can review "
        "your progress over time. Consistent, comparable entries are more "
        "useful than reacting to one day's changes."
    )

    profile = get_latest_profile(account_id)
    existing_measurements = get_body_measurements(account_id)
    existing_logs = get_workout_logs(account_id)

    default_weight = (
        float(existing_measurements[-1]["weight_kg"])
        if existing_measurements
        else (float(profile[4]) if profile is not None else 65.0)
    )

    st.subheader("1. Body check-in")
    st.caption(
        "A weekly check-in is a practical starting point. Try to measure at a "
        "similar time and under similar conditions. Leave optional measurements at 0 if not taken."
    )

    with st.form("body_checkin_form"):
        checkin_date = st.date_input("Check-in date", value=date.today(), key="checkin_date")
        checkin_weight = st.number_input(
            "Body weight (kg)", min_value=20.0, max_value=300.0,
            value=default_weight, step=0.1, key="checkin_weight"
        )
        measure_col1, measure_col2 = st.columns(2)
        with measure_col1:
            waist_cm = st.number_input(
                "Waist (cm) — optional; enter 0 if not measured",
                min_value=0.0, max_value=250.0, value=0.0, step=0.5,
                key="waist_cm"
            )
            chest_cm = st.number_input(
                "Chest (cm) — optional; enter 0 if not measured",
                min_value=0.0, max_value=250.0, value=0.0, step=0.5,
                key="chest_cm"
            )
        with measure_col2:
            arm_cm = st.number_input(
                "Upper arm (cm) — optional; enter 0 if not measured",
                min_value=0.0, max_value=250.0, value=0.0, step=0.5,
                key="arm_cm"
            )
            hip_cm = st.number_input(
                "Hip (cm) — optional; enter 0 if not measured",
                min_value=0.0, max_value=250.0, value=0.0, step=0.5,
                key="hip_cm"
            )
        body_notes = st.text_area(
            "Notes (optional)",
            placeholder="For example: morning measurement, before breakfast",
            key="body_notes",
        )
        body_submitted = st.form_submit_button("Save body check-in")

    if body_submitted:
        try:
            save_body_measurement(
                account_id=account_id,
                entry_date=checkin_date,
                weight_kg=checkin_weight,
                waist_cm=waist_cm if waist_cm > 0 else None,
                chest_cm=chest_cm if chest_cm > 0 else None,
                arm_cm=arm_cm if arm_cm > 0 else None,
                hip_cm=hip_cm if hip_cm > 0 else None,
                notes=body_notes,
            )
            st.success("Body check-in saved.")
        except Exception as error:
            st.error("The body check-in could not be saved.")
            st.exception(error)

    st.divider()
    st.subheader("2. Log a workout exercise")
    st.caption(
        "Enter one exercise per log entry. Use the load and reps from your "
        "best controlled working set for that exercise. Enter 0 kg for bodyweight movements."
    )

    with st.form("workout_log_form"):
        log_date = st.date_input("Workout date", value=date.today(), key="log_date")
        log_col1, log_col2 = st.columns(2)
        with log_col1:
            log_muscle = st.selectbox("Muscle group", MUSCLE_GROUPS, key="log_muscle")
            exercise_name = st.text_input(
                "Exercise name",
                placeholder="For example: Incline Dumbbell Press",
                key="logged_exercise_name",
            )
            log_sets = st.number_input(
                "Working sets", min_value=1, max_value=30, value=3, step=1,
                key="logged_sets"
            )
        with log_col2:
            log_reps = st.number_input(
                "Reps in your recorded working set", min_value=1, max_value=200,
                value=10, step=1, key="logged_reps"
            )
            log_load = st.number_input(
                "Load (kg); enter 0 for bodyweight/no external load",
                min_value=0.0, max_value=1000.0, value=0.0, step=0.5,
                key="logged_load"
            )
            log_notes = st.text_input(
                "Notes (optional)", placeholder="For example: felt controlled",
                key="logged_notes"
            )
        workout_submitted = st.form_submit_button("Save workout entry")

    if workout_submitted:
        if not exercise_name.strip():
            st.error("Please enter the exercise name.")
        else:
            try:
                save_workout_log(
                    account_id=account_id,
                    entry_date=log_date,
                    muscle_group=log_muscle,
                    exercise_name=exercise_name,
                    sets=log_sets,
                    reps=log_reps,
                    load_kg=log_load,
                    notes=log_notes,
                )
                st.success("Workout entry saved.")
            except Exception as error:
                st.error("The workout entry could not be saved.")
                st.exception(error)

    # Reload after form submissions so new entries appear immediately.
    body_records = get_body_measurements(account_id)
    workout_records = get_workout_logs(account_id)

    st.divider()
    st.subheader("3. Your body-weight trend")
    if body_records:
        body_df = pd.DataFrame(body_records)
        body_df["entry_date"] = pd.to_datetime(body_df["entry_date"])
        body_df = body_df.sort_values(["entry_date", "id"])

        first_weight = float(body_df.iloc[0]["weight_kg"])
        latest_weight = float(body_df.iloc[-1]["weight_kg"])
        weight_change = latest_weight - first_weight
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Latest weight", f"{latest_weight:.1f} kg")
        metric_col2.metric("First recorded weight", f"{first_weight:.1f} kg")
        metric_col3.metric(
            "Change since first check-in",
            f"{weight_change:+.1f} kg",
            help="A positive or negative change is not automatically good or bad; interpret it in the context of your goal and overall wellbeing.",
        )

        weight_chart = px.line(
            body_df, x="entry_date", y="weight_kg", markers=True,
            title="Body weight over time",
            color_discrete_sequence=["#B7F34A"],
            labels={"entry_date": "Date", "weight_kg": "Weight (kg)"},
        )
        weight_chart.update_traces(line={"width": 3}, marker={"size": 9})
        st.plotly_chart(style_figure(weight_chart, 390), use_container_width=True, config=PLOTLY_CONFIG)

        optional_columns = [
            column for column in ["waist_cm", "chest_cm", "arm_cm", "hip_cm"]
            if body_df[column].notna().any()
        ]
        if optional_columns:
            st.markdown("**Optional measurement history**")
            pretty_names = {
                "waist_cm": "Waist (cm)",
                "chest_cm": "Chest (cm)",
                "arm_cm": "Upper arm (cm)",
                "hip_cm": "Hip (cm)",
            }
            measurement_df = body_df[["entry_date"] + optional_columns].copy()
            measurement_df = measurement_df.rename(columns=pretty_names)
            st.dataframe(measurement_df, use_container_width=True, hide_index=True)

        available_measurements = [
            ("waist_cm", "Waist (cm)"), ("chest_cm", "Chest (cm)"),
            ("arm_cm", "Upper arm (cm)"), ("hip_cm", "Hip (cm)"),
        ]
        available_measurements = [(col, label) for col, label in available_measurements if body_df[col].notna().any()]
        if available_measurements:
            selected_measurement = st.selectbox(
                "Explore a measurement trend", [label for _, label in available_measurements],
                key="measurement_trend_choice",
            )
            measurement_column = dict((label, col) for col, label in available_measurements)[selected_measurement]
            measurement_history = body_df[body_df[measurement_column].notna()]
            measurement_chart = px.area(
                measurement_history, x="entry_date", y=measurement_column, markers=True,
                title=f"{selected_measurement} over time",
                color_discrete_sequence=["#22D3EE"],
            )
            measurement_chart.update_traces(line={"width": 3}, fillcolor="rgba(34,211,238,0.12)")
            st.plotly_chart(style_figure(measurement_chart, 330), use_container_width=True, config=PLOTLY_CONFIG)

        display_body = body_df.sort_values(["entry_date", "id"], ascending=False).copy()
        display_body["entry_date"] = display_body["entry_date"].dt.strftime("%Y-%m-%d")
        st.markdown("**Body check-in history**")
        st.dataframe(
            display_body[["entry_date", "weight_kg", "waist_cm", "chest_cm", "arm_cm", "hip_cm", "notes"]],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No body check-ins yet. Save your first entry above to start a trend.")

    st.divider()
    st.subheader("4. Workout performance history")
    if workout_records:
        workout_df = pd.DataFrame(workout_records)
        workout_df["entry_date"] = pd.to_datetime(workout_df["entry_date"])
        unique_exercises = sorted(workout_df["exercise_name"].dropna().unique().tolist())
        st.markdown("#### Training distribution")
        workout_chart_col1, workout_chart_col2 = st.columns(2)
        muscle_set_summary = (
            workout_df.groupby("muscle_group", as_index=False)["sets"].sum()
            .rename(columns={"sets": "Working sets"})
        )
        with workout_chart_col1:
            training_pie = px.pie(
                muscle_set_summary, names="muscle_group", values="Working sets",
                hole=0.58, color_discrete_sequence=CHART_COLORS,
                title="Logged working sets by muscle",
            )
            training_pie.update_traces(textposition="inside", textinfo="percent")
            st.plotly_chart(style_figure(training_pie, 340), use_container_width=True, config=PLOTLY_CONFIG)
        with workout_chart_col2:
            training_bar = px.bar(
                muscle_set_summary.sort_values("Working sets"),
                x="Working sets", y="muscle_group", orientation="h",
                color="muscle_group", color_discrete_sequence=CHART_COLORS,
                title="Compare working sets",
            )
            training_bar.update_layout(showlegend=False, yaxis_title=None)
            st.plotly_chart(style_figure(training_bar, 340), use_container_width=True, config=PLOTLY_CONFIG)

        selected_exercise = st.selectbox(
            "Choose an exercise to review",
            unique_exercises,
            key="progress_exercise_choice",
        )
        exercise_df = workout_df[workout_df["exercise_name"] == selected_exercise].copy()
        exercise_df = exercise_df.sort_values(["entry_date", "id"])

        if (exercise_df["load_kg"] > 0).any():
            chart_df = exercise_df[exercise_df["load_kg"] > 0]
            performance_chart = px.line(
                chart_df, x="entry_date", y="load_kg", markers=True,
                title=f"Recorded load: {selected_exercise}",
                color_discrete_sequence=["#A78BFA"],
                labels={"entry_date": "Date", "load_kg": "Load (kg)"},
            )
            performance_chart.update_traces(line={"width": 3}, marker={"size": 9})
            st.plotly_chart(style_figure(performance_chart, 370), use_container_width=True, config=PLOTLY_CONFIG)
        else:
            performance_chart = px.line(
                exercise_df, x="entry_date", y="reps", markers=True,
                title=f"Recorded reps: {selected_exercise}",
                color_discrete_sequence=["#F59E0B"],
                labels={"entry_date": "Date", "reps": "Reps"},
            )
            performance_chart.update_traces(line={"width": 3}, marker={"size": 9})
            st.plotly_chart(style_figure(performance_chart, 370), use_container_width=True, config=PLOTLY_CONFIG)

        total_entries = len(workout_df)
        training_days_logged = workout_df["entry_date"].dt.date.nunique()
        summary_col1, summary_col2 = st.columns(2)
        summary_col1.metric("Exercise entries logged", total_entries)
        summary_col2.metric("Training days recorded", training_days_logged)

        log_display = workout_df.sort_values(["entry_date", "id"], ascending=False).copy()
        log_display["entry_date"] = log_display["entry_date"].dt.strftime("%Y-%m-%d")
        st.markdown("**Recent workout entries**")
        st.dataframe(
            log_display[["entry_date", "muscle_group", "exercise_name", "sets", "reps", "load_kg", "notes"]].head(30),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No workout entries yet. Save your first exercise entry above to track performance.")

    st.divider()
    st.subheader("5. Export your Muscle Cafe data")
    st.write(
        "Download a copy of your saved records for your own review or to analyse in a spreadsheet. "
        "Only records already saved in this app are included."
    )
    export_col1, export_col2 = st.columns(2)
    with export_col1:
        if body_records:
            body_export_df = pd.DataFrame(body_records)
            st.download_button(
                label="Download body check-ins (CSV)",
                data=body_export_df.to_csv(index=False).encode("utf-8"),
                file_name="muscle_cafe_body_checkins.csv",
                mime="text/csv",
                key="download_body_checkins_csv",
            )
        else:
            st.caption("Save a body check-in to enable this export.")
    with export_col2:
        if workout_records:
            workout_export_df = pd.DataFrame(workout_records)
            st.download_button(
                label="Download workout history (CSV)",
                data=workout_export_df.to_csv(index=False).encode("utf-8"),
                file_name="muscle_cafe_workout_history.csv",
                mime="text/csv",
                key="download_workout_history_csv",
            )
        else:
            st.caption("Save a workout entry to enable this export.")

    st.caption(
        "Progress trends are descriptive, not a diagnosis or a measure of body composition. "
        "Body weight naturally fluctuates. Compare trends over several weeks rather than "
        "judging one measurement, and stop any exercise that causes pain."
    )

