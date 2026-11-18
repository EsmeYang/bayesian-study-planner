
import pytest

from src.decision import (
    ACTIONS,
    calculate_expected_utility,
    recommend_study_action,
)


def test_three_actions_exist():
    assert len(ACTIONS) == 3


def test_action_hours():
    assert ACTIONS["Intensive Study"]["hours"] == 5
    assert ACTIONS["Light Review"]["hours"] == 1
    assert ACTIONS["Rest Day"]["hours"] == 0


def test_expected_utility_calculation():
    result = calculate_expected_utility(
        0.4, 0.5, "Light Review"
    )
    assert result["expected_utility"] == pytest.approx(32.4)


def test_probabilities_stay_valid():
    result = calculate_expected_utility(
        0.95, 0.95, "Intensive Study"
    )
    assert 0 <= result["expected_readiness"] <= 1
    assert 0 <= result["expected_stress"] <= 1


def test_invalid_action():
    with pytest.raises(ValueError):
        calculate_expected_utility(0.5, 0.5, "Unknown")


def test_recommendation_is_best_action():
    result = recommend_study_action({
        "Mastery": "Low",
        "Stress": "High",
        "DaysUntilExam": "Near",
    })

    utilities = [
        action["expected_utility"]
        for action in result["all_actions"]
    ]

    assert (
        result["recommendation"]["expected_utility"]
        == max(utilities)
    )


def test_all_actions_returned():
    result = recommend_study_action({
        "Mastery": "High",
    })

    assert len(result["all_actions"]) == 3
