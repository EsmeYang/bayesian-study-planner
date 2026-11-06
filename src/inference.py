
from pgmpy.inference import VariableElimination

from src.bayesian_model import create_bayesian_network


def predict_student(evidence):
    """
    Predict exam readiness and stress risk
    using Variable Elimination.
    """

    model = create_bayesian_network()
    inference = VariableElimination(model)

    readiness = inference.query(
        variables=["ExamReadiness"],
        evidence=evidence,
        show_progress=False,
    )

    stress_risk = inference.query(
        variables=["StressRisk"],
        evidence=evidence,
        show_progress=False,
    )

    return {
        "exam_readiness_high": float(
            readiness.get_value(ExamReadiness="High")
        ),
        "stress_risk_high": float(
            stress_risk.get_value(StressRisk="High")
        ),
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

    result = predict_student(student)

    print("Student Prediction")
    print("------------------")
    print(f"Exam readiness (High): {result['exam_readiness_high']:.2%}")
    print(f"Stress risk (High): {result['stress_risk_high']:.2%}")
