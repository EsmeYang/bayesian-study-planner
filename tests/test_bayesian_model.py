
import numpy as np

from src.bayesian_model import create_bayesian_network


def test_model_is_valid():
    model = create_bayesian_network()
    assert model.check_model()


def test_number_of_variables():
    model = create_bayesian_network()
    assert len(model.nodes()) == 8


def test_number_of_edges():
    model = create_bayesian_network()
    assert len(model.edges()) == 8


def test_number_of_cpds():
    model = create_bayesian_network()
    assert len(model.get_cpds()) == 8


def test_all_cpds_sum_to_one():
    model = create_bayesian_network()

    for cpd in model.get_cpds():
        probabilities = cpd.get_values()
        column_sums = probabilities.sum(axis=0)

        assert np.allclose(column_sums, 1.0)


def test_exam_readiness_has_six_parents():
    model = create_bayesian_network()

    expected_parents = {
        "Concept1Difficulty",
        "Concept2Difficulty",
        "Concept3Difficulty",
        "Mastery",
        "Stress",
        "DaysUntilExam",
    }

    assert set(model.get_parents("ExamReadiness")) == expected_parents


def test_stress_risk_has_two_parents():
    model = create_bayesian_network()

    expected_parents = {"Stress", "DaysUntilExam"}

    assert set(model.get_parents("StressRisk")) == expected_parents
