
from pgmpy.factors.discrete import TabularCPD


def create_root_cpds():
    """Create handcrafted CPTs for the six root variables."""

    cpds = [
        TabularCPD(
            variable="Concept1Difficulty",
            variable_card=2,
            values=[[0.60], [0.40]],
            state_names={
                "Concept1Difficulty": ["Easy", "Hard"]
            },
        ),
        TabularCPD(
            variable="Concept2Difficulty",
            variable_card=2,
            values=[[0.50], [0.50]],
            state_names={
                "Concept2Difficulty": ["Easy", "Hard"]
            },
        ),
        TabularCPD(
            variable="Concept3Difficulty",
            variable_card=2,
            values=[[0.40], [0.60]],
            state_names={
                "Concept3Difficulty": ["Easy", "Hard"]
            },
        ),
        TabularCPD(
            variable="Mastery",
            variable_card=2,
            values=[[0.50], [0.50]],
            state_names={"Mastery": ["Low", "High"]},
        ),
        TabularCPD(
            variable="Stress",
            variable_card=2,
            values=[[0.60], [0.40]],
            state_names={"Stress": ["Low", "High"]},
        ),
        TabularCPD(
            variable="DaysUntilExam",
            variable_card=2,
            values=[[0.40], [0.60]],
            state_names={"DaysUntilExam": ["Near", "Far"]},
        ),
    ]

    return cpds




from itertools import product



def create_stress_risk_cpd():
    """
    Define P(StressRisk | Stress, DaysUntilExam).

    StressRisk depends on:
    - Current stress level
    - Number of days remaining before the exam
    """

    cpd = TabularCPD(
        variable="StressRisk",
        variable_card=2,
        values=[
            [0.65, 0.90, 0.10, 0.45],  # Low risk
            [0.35, 0.10, 0.90, 0.55],  # High risk
        ],
        evidence=["Stress", "DaysUntilExam"],
        evidence_card=[2, 2],
        state_names={
            "StressRisk": ["Low", "High"],
            "Stress": ["Low", "High"],
            "DaysUntilExam": ["Near", "Far"],
        },
    )

    return cpd



def create_exam_readiness_cpd():
    """
    Create a handcrafted CPT for ExamReadiness.

    The probability of high exam readiness depends on:
    - Three concept difficulties
    - Student mastery
    - Current stress
    - Days remaining until the exam
    """

    evidence = [
        "Concept1Difficulty",
        "Concept2Difficulty",
        "Concept3Difficulty",
        "Mastery",
        "Stress",
        "DaysUntilExam",
    ]

    state_names = {
        "Concept1Difficulty": ["Easy", "Hard"],
        "Concept2Difficulty": ["Easy", "Hard"],
        "Concept3Difficulty": ["Easy", "Hard"],
        "Mastery": ["Low", "High"],
        "Stress": ["Low", "High"],
        "DaysUntilExam": ["Near", "Far"],
        "ExamReadiness": ["Low", "High"],
    }

    low_probabilities = []
    high_probabilities = []

    for c1, c2, c3, mastery, stress, days in product(
        *[state_names[var] for var in evidence]
    ):
        # Handcrafted baseline probability
        p_high = 0.65

        # Hard concepts reduce readiness
        for difficulty in [c1, c2, c3]:
            if difficulty == "Hard":
                p_high -= 0.10

        # High mastery improves readiness
        if mastery == "High":
            p_high += 0.25

        # High stress reduces readiness
        if stress == "High":
            p_high -= 0.15

        # An approaching exam reduces readiness
        if days == "Near":
            p_high -= 0.15

        # Keep probabilities within valid bounds
        p_high = max(0.05, min(0.95, p_high))

        p_high = round(p_high, 4)
        p_low = round(1.0 - p_high, 4)

        low_probabilities.append(p_low)
        high_probabilities.append(p_high)

    return TabularCPD(
        variable="ExamReadiness",
        variable_card=2,
        values=[
            low_probabilities,
            high_probabilities,
        ],
        evidence=evidence,
        evidence_card=[2] * len(evidence),
        state_names=state_names,
    )
