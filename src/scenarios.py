
SCENARIOS = {
    "Struggling Student": {
        "Concept1Difficulty": "Hard",
        "Concept2Difficulty": "Easy",
        "Concept3Difficulty": "Hard",
        "Mastery": "Low",
        "Stress": "High",
        "DaysUntilExam": "Near",
    },

    "Average Student": {
        "Concept1Difficulty": "Easy",
        "Concept2Difficulty": "Hard",
        "Concept3Difficulty": "Easy",
        "Mastery": "Low",
        "Stress": "Low",
        "DaysUntilExam": "Far",
    },

    "Well-Prepared Student": {
        "Concept1Difficulty": "Easy",
        "Concept2Difficulty": "Easy",
        "Concept3Difficulty": "Easy",
        "Mastery": "High",
        "Stress": "Low",
        "DaysUntilExam": "Far",
    },
}


def get_scenario(name):
    """Return a copy of a predefined student scenario."""

    if name not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {name}")

    return SCENARIOS[name].copy()
