
import pytest

from src.inference import predict_student


def test_prediction_probabilities():
    evidence = {
        "Mastery": "Low",
        "Stress": "High",
        "DaysUntilExam": "Near",
    }

    result = predict_student(evidence)

    assert 0 <= result["exam_readiness_high"] <= 1
    assert 0 <= result["stress_risk_high"] <= 1


def test_high_stress_increases_risk():
    base = {
        "DaysUntilExam": "Near",
    }

    low = predict_student({
        **base,
        "Stress": "Low",
    })

    high = predict_student({
        **base,
        "Stress": "High",
    })

    assert (
        high["stress_risk_high"]
        > low["stress_risk_high"]
    )


def test_high_mastery_improves_readiness():
    base = {
        "Stress": "Low",
        "DaysUntilExam": "Far",
    }

    low = predict_student({
        **base,
        "Mastery": "Low",
    })

    high = predict_student({
        **base,
        "Mastery": "High",
    })

    assert (
        high["exam_readiness_high"]
        > low["exam_readiness_high"]
    )


def test_fully_observed_student():
    evidence = {
        "Concept1Difficulty": "Hard",
        "Concept2Difficulty": "Easy",
        "Concept3Difficulty": "Hard",
        "Mastery": "Low",
        "Stress": "High",
        "DaysUntilExam": "Near",
    }

    result = predict_student(evidence)

    assert result["exam_readiness_high"] == pytest.approx(0.15)
    assert result["stress_risk_high"] == pytest.approx(0.90)


def test_partial_evidence():
    result = predict_student({
        "Mastery": "High",
    })

    assert 0 <= result["exam_readiness_high"] <= 1
    assert 0 <= result["stress_risk_high"] <= 1
