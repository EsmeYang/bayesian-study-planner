
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

from src.decision import recommend_study_action
from src.scenarios import SCENARIOS, get_scenario
from src.calendar_integration import (
    create_study_event,
    add_event_to_calendar,
)


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="BayesStudy",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 BayesStudy")

st.subheader("Personalized Bayesian Study Planner")

st.caption(
    "A Bayesian decision-support system for personalized "
    "study recommendations and calendar scheduling."
)


# --------------------------------------------------
# Student profile
# --------------------------------------------------

st.sidebar.header("Student Profile")

scenario_name = st.sidebar.selectbox(
    "Student Scenario",
    ["Custom Student"] + list(SCENARIOS.keys()),
)

if scenario_name == "Custom Student":
    defaults = {
        "Concept1Difficulty": "Easy",
        "Concept2Difficulty": "Easy",
        "Concept3Difficulty": "Easy",
        "Mastery": "Low",
        "Stress": "Low",
        "DaysUntilExam": "Far",
    }
else:
    defaults = get_scenario(scenario_name)


def student_input(label, variable, options):
    return st.sidebar.selectbox(
        label,
        options,
        index=options.index(defaults[variable]),
        key=f"{scenario_name}_{variable}",
    )


concept1 = student_input(
    "Concept 1 Difficulty",
    "Concept1Difficulty",
    ["Easy", "Hard"],
)

concept2 = student_input(
    "Concept 2 Difficulty",
    "Concept2Difficulty",
    ["Easy", "Hard"],
)

concept3 = student_input(
    "Concept 3 Difficulty",
    "Concept3Difficulty",
    ["Easy", "Hard"],
)

mastery = student_input(
    "Current Mastery",
    "Mastery",
    ["Low", "High"],
)

stress = student_input(
    "Current Stress",
    "Stress",
    ["Low", "High"],
)

days_until_exam = student_input(
    "Days Until Exam",
    "DaysUntilExam",
    ["Near", "Far"],
)


evidence = {
    "Concept1Difficulty": concept1,
    "Concept2Difficulty": concept2,
    "Concept3Difficulty": concept3,
    "Mastery": mastery,
    "Stress": stress,
    "DaysUntilExam": days_until_exam,
}


# --------------------------------------------------
# Generate recommendation
# --------------------------------------------------

if st.sidebar.button(
    "Generate Recommendation",
    type="primary",
    use_container_width=True,
):
    st.session_state["result"] = recommend_study_action(
        evidence
    )

    st.session_state["last_evidence"] = evidence.copy()

    st.session_state.pop("created_event", None)


if "result" not in st.session_state:
    st.info(
        "Select your student profile and click "
        "Generate Recommendation to get started."
    )
    st.stop()


if st.session_state["last_evidence"] != evidence:
    st.warning(
        "Your student profile has changed. "
        "Generate a new recommendation to continue."
    )
    st.stop()


result = st.session_state["result"]

prediction = result["prediction"]
recommendation = result["recommendation"]
all_actions = result["all_actions"]


# --------------------------------------------------
# Bayesian predictions
# --------------------------------------------------

st.header("1. Bayesian Predictions")

col1, col2 = st.columns(2)

with col1:
    readiness = prediction["exam_readiness_high"]

    st.metric(
        "Exam Readiness (High)",
        f"{readiness:.1%}",
    )

    st.progress(readiness)

with col2:
    stress_risk = prediction["stress_risk_high"]

    st.metric(
        "Stress Risk (High)",
        f"{stress_risk:.1%}",
    )

    st.progress(stress_risk)


# --------------------------------------------------
# Expected utility comparison
# --------------------------------------------------

st.divider()

st.header("2. Expected Utility Comparison")

action_data = pd.DataFrame(all_actions)

chart_data = action_data[
    ["action", "expected_utility"]
].set_index("action")

st.bar_chart(chart_data)

display_data = action_data.rename(
    columns={
        "action": "Action",
        "hours": "Study Hours",
        "expected_readiness": "Projected Readiness",
        "expected_stress": "Projected Stress Risk",
        "expected_utility": "Expected Utility",
    }
)

st.dataframe(
    display_data.style.format({
        "Projected Readiness": "{:.1%}",
        "Projected Stress Risk": "{:.1%}",
        "Expected Utility": "{:.2f}",
    }),
    hide_index=True,
    use_container_width=True,
)


# --------------------------------------------------
# Recommended action
# --------------------------------------------------

st.divider()

st.header("3. Recommended Study Action")

action = recommendation["action"]
hours = recommendation["hours"]
utility = recommendation["expected_utility"]

st.success(f"Recommended Action: {action}")

col1, col2 = st.columns(2)

col1.metric("Study Duration", f"{hours} hours")

col2.metric("Expected Utility", f"{utility:.2f}")

if action == "Intensive Study":
    st.write(
        "A longer study session is recommended because "
        "its estimated benefits outweigh the modeled costs."
    )

elif action == "Light Review":
    st.write(
        "A shorter review session offers the best modeled "
        "balance between preparation and study cost."
    )

else:
    st.write(
        "Rest is recommended because additional study "
        "offers less estimated utility under this profile."
    )


# --------------------------------------------------
# Google Calendar integration
# --------------------------------------------------

st.divider()

st.header("4. Schedule Your Study Session")

if hours == 0:
    st.info(
        "Rest Day is recommended. "
        "No study session needs to be scheduled."
    )

else:
    pacific = ZoneInfo("America/Vancouver")
    now = datetime.now(pacific)
    default_start = now + timedelta(days=1)

    selected_date = st.date_input(
        "Study Date",
        value=default_start.date(),
        min_value=now.date(),
    )

    selected_time = st.time_input(
        "Start Time",
        value=default_start.time().replace(
            second=0,
            microsecond=0,
        ),
    )

    start_time = datetime.combine(
        selected_date,
        selected_time,
        tzinfo=pacific,
    )

    event = create_study_event(
        action,
        start_time,
    )

    st.subheader("Calendar Event Preview")

    st.write("**Title:**", event["summary"])

    st.write(
        "**Start:**",
        event["start"]["dateTime"],
    )

    st.write(
        "**End:**",
        event["end"]["dateTime"],
    )

    event_key = (
        action,
        start_time.isoformat(),
    )

    already_created = (
        st.session_state.get("created_event") == event_key
    )

    if already_created:
        st.success("This session has already been scheduled.")

    elif start_time <= now:
        st.warning("Please select a future start time.")

    else:
        confirmed = st.checkbox(
            "I confirm that I want to add this event "
            "to my Google Calendar."
        )

        if st.button(
            "Add to Google Calendar",
            disabled=not confirmed,
            type="primary",
        ):
            try:
                with st.spinner(
                    "Connecting to Google Calendar..."
                ):
                    created = add_event_to_calendar(event)

                st.session_state["created_event"] = event_key

                st.success(
                    "Google Calendar event created successfully!"
                )

                if created.get("htmlLink"):
                    st.link_button(
                        "Open Google Calendar Event",
                        created["htmlLink"],
                    )

            except Exception as error:
                st.error(
                    f"Unable to create calendar event: {error}"
                )


# --------------------------------------------------
# Model limitations
# --------------------------------------------------

st.divider()

with st.expander("About the Bayesian Model"):
    st.write(
        "BayesStudy uses a discrete Bayesian Network "
        "with eight variables and Variable Elimination "
        "for probabilistic inference."
    )

    st.write(
        "Expected utility combines projected exam "
        "readiness, stress risk, and study duration."
    )

    st.latex(
        r"EU(a)=100P(R=High|e,a)"
        r"-30P(S=High|e,a)-2h(a)"
    )

    st.write(
        "The conditional probabilities, action effects, "
        "and utility weights are manually defined prototype "
        "assumptions rather than estimates learned from "
        "real student data."
    )

    st.write(
        "Calendar scheduling requires explicit user "
        "confirmation. The system does not automatically "
        "check for scheduling conflicts."
    )

st.caption(
    "BayesStudy | COSC 329 Individual Project"
)
