
from src.inference import predict_student


ACTIONS = {
    "Intensive Study": {
        "hours": 5,
        "readiness_gain": 0.25,
        "stress_change": 0.15,
    },
    "Light Review": {
        "hours": 1,
        "readiness_gain": 0.10,
        "stress_change": 0.02,
    },
    "Rest Day": {
        "hours": 0,
        "readiness_gain": 0.00,
        "stress_change": -0.20,
    },
}


def clamp(value):
    return max(0.0, min(1.0, value))


def calculate_expected_utility(
    readiness_probability,
    stress_probability,
    action,
):
    """Estimate the utility of a study action."""

    if action not in ACTIONS:
        raise ValueError(f"Unknown action: {action}")

    settings = ACTIONS[action]

    adjusted_readiness = clamp(
        readiness_probability + settings["readiness_gain"]
    )

    adjusted_stress = clamp(
        stress_probability + settings["stress_change"]
    )

    utility = (
        100 * adjusted_readiness
        - 30 * adjusted_stress
        - 2 * settings["hours"]
    )

    return {
        "action": action,
        "hours": settings["hours"],
        "expected_readiness": adjusted_readiness,
        "expected_stress": adjusted_stress,
        "expected_utility": round(utility, 2),
    }


def recommend_study_action(evidence):
    """Compare all actions and recommend the highest-utility option."""

    prediction = predict_student(evidence)

    results = [
        calculate_expected_utility(
            prediction["exam_readiness_high"],
            prediction["stress_risk_high"],
            action,
        )
        for action in ACTIONS
    ]

    best = max(results, key=lambda item: item["expected_utility"])

    return {
        "prediction": prediction,
        "recommendation": best,
        "all_actions": results,
    }


if __name__ == "__main__":
    student = {
        "Concept1Difficulty": "Hard",
        "Concept2Difficulty": "Easy",
        "Concept3Difficulty": "Hard",
        "Mastery": "Low",
        "Stress": "High",
        "DaysUntilExam": "Near",
    }

    result = recommend_study_action(student)

    print("BayesStudy — Study Recommendation")
    print("--------------------------------")

    for action in result["all_actions"]:
        print(
            f"{action['action']}: "
            f"EU = {action['expected_utility']:.2f}"
        )

    print(
        "\nRecommended action:",
        result["recommendation"]["action"],
    )
