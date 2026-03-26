import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
from db_update import *
load_dotenv()


def mainbar():

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"), )
    taskstodo = view_todo()
    # CHAT

    st.set_page_config(page_icon="🗓️", layout="wide",
                    page_title="AI planner assistant")

    st.title("AI planner assistant",text_alignment = "center", anchor=False)

    if st.button("Generate day"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates todays plan based on tasks given."},
                {"role": "user", "content": f"Tasks: {taskstodo}\nCreate todays plan based on tasks I gave you."}
            ], 
            max_tokens=150
        )
        insights = response.choices[0].message.content.strip()
        st.write("### AI Insights:")
        st.write(insights)  



    st.title("Your profile")

    with st.form("your_profile"):

# Step 1: About you 
        st.subheader("About you")

        occupation = st.text_input(
            "Occupation / field of work",
            placeholder="e.g. software engineer, marketing manager, student...",
            help="Helps AI adapt tasks and terminology to your context",
        )

        work_model = st.selectbox(
            "Work model",
            ["Office", "Remote", "Hybrid", "Self-employed", "Student"],
        )

        st.divider()

#Step 2: Sleep rhythm
        st.subheader("Sleep rhythm")

        col1, col2 = st.columns(2)
        with col1:
            wake_time = st.time_input("Typical wake-up time", value=None)
        with col2:
            bedtime = st.time_input("Typical bedtime", value=None)

        sleep_hours = st.slider(
            "Average hours of sleep per night",
            min_value=4.0,
            max_value=10.0,
            value=7.0,
            step=0.5,
            format="%.1f h",
        )

        peak_productivity = st.selectbox(
            "When are you most productive?",
            [
                "Early morning (5–8)",
                "Morning (8–12)",
                "Early afternoon (12–16)",
                "Late afternoon (16–19)",
                "Evening (19+)",
            ],
            index=1,
        )

        alarm_use = st.selectbox(
            "Do you use an alarm?",
            ["Yes, one alarm", "Yes, multiple alarms", "No, I wake up naturally"],
        )

        st.divider()

#Step 3: Work schedule
        st.subheader("Work schedule")

        col1, col2 = st.columns(2)
        with col1:
            work_start = st.time_input("Start of work day", value=None)
        with col2:
            work_end = st.time_input("End of work day", value=None)

        break_style = st.selectbox(
            "How do you usually take breaks?",
            [
                "Rarely — I work non-stop",
                "Short breaks every hour",
                "Pomodoro technique",
                "One long break after work",
            ],
            index=1,
        )

        work_type = st.multiselect(
            "Type of work you do",
            [
                "Deep analysis",
                "Writing / creative",
                "Meetings / communication",
                "Coding",
                "Administration",
                "Physical work",
            ],
            help="Helps AI estimate the mental load of your tasks",
        )

        workdays = st.multiselect(
            "Which days do you work?",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            default=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        )

        st.divider()

#Step 4: Physical activity
        st.subheader("Physical activity")

        exercises = st.toggle("Do you exercise regularly?", value=True)

        if exercises:
            ex_types = st.multiselect(
                "Types of workout",
                ["Gym", "Running", "Yoga / pilates", "Cycling", "Swimming",
                "Team sport", "Martial arts", "Walking"],
            )

            col1, col2 = st.columns(2)
            with col1:
                ex_freq = st.number_input(
                    "How many times per week?", min_value=1, max_value=7, value=3
                )
            with col2:
                ex_duration = st.number_input(
                    "Average duration (min)", min_value=15, max_value=180, value=60, step=5
                )

            ex_time_pref = st.selectbox(
                "When do you prefer to work out?",
                ["Before work", "During lunch break", "After work", "Evening", "It varies"],
                index=1,
            )
        else:
            ex_types = []
            ex_freq = 0
            ex_duration = 0
            ex_time_pref = None

        st.divider()

#Step 5: Nutrition & habits
        st.subheader("Nutrition & habits")

        breakfast = st.selectbox(
            "Breakfast",
            [
                "Always have breakfast",
                "Sometimes",
                "Rarely / never",
                "Intermittent fasting (IF)",
            ],
        )

        meals_per_day = st.selectbox(
            "Meals per day",
            ["1–2", "3", "4–5", "I snack throughout the day"],
            index=1,
        )

        diet = st.multiselect(
            "Diet or restrictions",
            ["No restrictions", "Vegan", "Vegetarian", "Gluten-free", "Keto", "Halal / Kosher"],
            default=["No restrictions"],
        )

        caffeine = st.selectbox(
            "Caffeine intake",
            [
                "None",
                "One coffee in the morning",
                "2–3 coffees a day",
                "More than 3",
                "Tea only",
            ],
            index=2,
        )

        water_goal = st.slider(
            "Daily water goal (litres)",
            min_value=1.0,
            max_value=4.0,
            value=2.0,
            step=0.5,
            format="%.1f L",
        )

        st.divider()

#Step 6: Goals & values
        st.subheader("Goals & values")

        life_priorities = st.multiselect(
            "Life priorities (choose up to 3)",
            [
                "Career & growth",
                "Health & fitness",
                "Family",
                "Finances",
                "Creativity",
                "Learning & development",
                "Social life",
                "Mental health",
                "Spirituality",
            ],
            max_selections=3,
        )

        challenges = st.multiselect(
            "Biggest productivity challenges",
            [
                "Procrastination",
                "Too many tasks at once",
                "Distractions (phone, social media)",
                "Low energy",
                "Difficulty saying no",
                "Perfectionism",
                "Poor organization",
            ],
        )

        motivation_style = st.selectbox(
            "Motivation style that works for you",
            [
                "Gentle & encouraging",
                "Direct & concrete",
                "Tough love, no excuses",
                "Data-driven & analytical",
            ],
            index=1,
        )

        long_term_goal = st.text_area(
            "Long-term goal that drives you",
            placeholder="e.g. Launch my own project, lose 10kg, learn a new language...",
            help="What do you want to achieve in the next year?",
        )

        st.divider()

#Step 7: Routines & preferences
        st.subheader("Routines & preferences")

        morning_routine = st.multiselect(
            "Morning routine (typical)",
            [
                "Meditation",
                "Exercise",
                "Reading",
                "Journaling",
                "Planning the day",
                "Shower first thing",
                "Coffee & silence",
                "Straight to work",
            ],
            help="What do you do from wake-up to starting work?",
        )

        evening_routine = st.multiselect(
            "Evening routine",
            [
                "Day review",
                "Reading",
                "Walk",
                "Meditation",
                "Prep for tomorrow",
                "Series / movie",
                "No screens before bed",
            ],
        )

        plan_format = st.selectbox(
            "Preferred plan format",
            [
                "Hour by hour",
                "Blocks (morning / afternoon / evening)",
                "Priority list",
                "Combination",
            ],
        )

        plan_language = st.selectbox("Plan language", ["English", "Serbian"])

        extra_notes = st.text_area(
            "Anything else AI should know about you",
            placeholder="Optional: health conditions, specific circumstances, special preferences...",
        )

#Submit
        submitted = st.form_submit_button("Save profile", use_container_width=True)

    if submitted:
        profile = {
            "occupation": occupation,
            "work_model": work_model,
            "wake_time": str(wake_time),
            "bedtime": str(bedtime),
            "sleep_hours": sleep_hours,
            "peak_productivity": peak_productivity,
            "alarm_use": alarm_use,
            "work_start": str(work_start),
            "work_end": str(work_end),
            "break_style": break_style,
            "work_type": work_type,
            "workdays": workdays,
            "exercises": exercises,
            "ex_types": ex_types,
            "ex_freq": ex_freq,
            "ex_duration": ex_duration,
            "ex_time_pref": ex_time_pref,
            "breakfast": breakfast,
            "meals_per_day": meals_per_day,
            "diet": diet,
            "caffeine": caffeine,
            "water_goal": water_goal,
            "life_priorities": life_priorities,
            "challenges": challenges,
            "motivation_style": motivation_style,
            "long_term_goal": long_term_goal,
            "morning_routine": morning_routine,
            "evening_routine": evening_routine,
            "plan_format": plan_format,
            "plan_language": plan_language,
            "extra_notes": extra_notes,
        }

        st.success("Profile saved!")
        profile_update(profile)