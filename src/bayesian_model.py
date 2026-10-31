
from pgmpy.models import DiscreteBayesianNetwork

from src.cpt import (
    create_root_cpds,
    create_stress_risk_cpd,
    create_exam_readiness_cpd,
)


def create_bayesian_network():
    """
    Build the Bayesian network for the personalized study planner.

    The network contains eight variables:
    - Concept1Difficulty
    - Concept2Difficulty
    - Concept3Difficulty
    - Mastery
    - Stress
    - DaysUntilExam
    - ExamReadiness
    - StressRisk
    """

    # Define the directed edges of the Bayesian network.
    edges = [
        ("Concept1Difficulty", "ExamReadiness"),
        ("Concept2Difficulty", "ExamReadiness"),
        ("Concept3Difficulty", "ExamReadiness"),
        ("Mastery", "ExamReadiness"),
        ("Stress", "ExamReadiness"),
        ("DaysUntilExam", "ExamReadiness"),
        ("Stress", "StressRisk"),
        ("DaysUntilExam", "StressRisk"),
    ]

    # Create the Bayesian network structure.
    model = DiscreteBayesianNetwork(edges)

    # Add the six root-variable CPTs.
    model.add_cpds(*create_root_cpds())

    # Add the conditional CPTs.
    model.add_cpds(
        create_exam_readiness_cpd(),
        create_stress_risk_cpd(),
    )

    return model


if __name__ == "__main__":
    model = create_bayesian_network()

    print("Bayesian Network Validation")
    print("---------------------------")

    print("Number of variables:", len(model.nodes()))
    print("Number of edges:", len(model.edges()))
    print("Number of CPTs:", len(model.get_cpds()))
    print("Model valid:", model.check_model())

    print("\nNetwork edges:")

    for parent, child in model.edges():
        print(f"{parent} -> {child}")
