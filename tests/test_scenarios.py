
import pytest

from src.scenarios import SCENARIOS, get_scenario
from src.decision import recommend_study_action


def test_three_scenarios_exist():
    assert len(SCENARIOS) == 3


def test_scenario_contains_six_variables():
    for name in SCENARIOS:
        scenario = get_scenario(name)
        assert len(scenario) == 6


def test_invalid_scenario():
    with pytest.raises(ValueError):
        get_scenario("Unknown Student")


def test_scenario_returns_copy():
    scenario = get_scenario("Struggling Student")
    scenario["Mastery"] = "High"

    original = get_scenario("Struggling Student")

    assert original["Mastery"] == "Low"


def test_struggling_student_recommendation():
    evidence = get_scenario("Struggling Student")

    result = recommend_study_action(evidence)

    assert (
        result["recommendation"]["action"]
        == "Intensive Study"
    )


def test_well_prepared_student_recommendation():
    evidence = get_scenario("Well-Prepared Student")

    result = recommend_study_action(evidence)

    assert (
        result["recommendation"]["action"]
        == "Light Review"
    )


def test_prepared_student_has_higher_readiness():
    struggling = recommend_study_action(
        get_scenario("Struggling Student")
    )

    prepared = recommend_study_action(
        get_scenario("Well-Prepared Student")
    )

    assert (
        prepared["prediction"]["exam_readiness_high"]
        >
        struggling["prediction"]["exam_readiness_high"]
    )


def test_all_scenarios_generate_recommendations():
    for name in SCENARIOS:
        result = recommend_study_action(
            get_scenario(name)
        )

        assert len(result["all_actions"]) == 3

        assert result["recommendation"]["action"] in [
            "Intensive Study",
            "Light Review",
            "Rest Day",
        ]
