
# BayesStudy — Personalized Bayesian Study Planner

A personalized study planning system that uses Bayesian networks to estimate exam readiness and stress risk, with the goal of recommending study schedules that balance academic performance and student well-being.

## Project Status

**In Development — Week 8: Bayesian Network Foundation Completed**

The project is being developed incrementally as part of a university course project.

### Current Features

- Bayesian network implemented using pgmpy
- 8 binary variables and 8 directed edges
- Handcrafted Conditional Probability Tables (CPTs)
- Exam readiness and stress risk modeling
- Model structure and CPT validation
- 7 automated tests using pytest

### Planned Features

- Bayesian inference using Variable Elimination
- Expected utility-based study recommendations
- Three study actions: intensive study, light review, and rest
- Google Calendar integration
- Interactive Streamlit interface
- Evaluation using simulated student scenarios

## Bayesian Network

The network contains eight variables:

| Variable | States | Description |
|---|---|---|
| Concept1Difficulty | Easy / Hard | Difficulty of the first concept |
| Concept2Difficulty | Easy / Hard | Difficulty of the second concept |
| Concept3Difficulty | Easy / Hard | Difficulty of the third concept |
| Mastery | Low / High | Student's overall mastery |
| Stress | Low / High | Student's current stress level |
| DaysUntilExam | Near / Far | Proximity of the upcoming exam |
| ExamReadiness | Low / High | Predicted exam readiness |
| StressRisk | Low / High | Predicted stress risk |

The model uses handcrafted CPTs to represent dependencies between these variables.

See [Network Design](docs/network_design.md) for the complete network structure and probability definitions.

## Tech Stack

- Python 3.12
- pgmpy
- NumPy
- pandas
- pytest

Planned integrations:
- Google Calendar API
- Streamlit

## Project Structure

```text
bayesian-study-planner/
├── docs/
│   └── network_design.md
├── src/
│   ├── __init__.py
│   ├── cpt.py
│   └── bayesian_model.py
├── tests/
│   └── test_bayesian_model.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/EsmeYang/bayesian-study-planner.git
cd bayesian-study-planner
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Running the Bayesian Network

To build and validate the model:

```bash
python -m src.bayesian_model
```

Expected validation results:

```text
Number of variables: 8
Number of edges: 8
Number of CPTs: 8
Model valid: True
```

## Running Tests

Run all automated tests:

```bash
python -m pytest -v
```

Current test results:

**7 tests passed.**

Tests cover model validity, variable and edge counts, CPT normalization, and parent relationships.

## Development Roadmap

| Week | Focus | Status |
|---|---|---|
| 8 | Bayesian network structure and CPTs | Completed |
| 9 | Bayesian inference | Planned |
| 10 | Expected utility and decision making | Planned |
| 11 | Google Calendar integration | Planned |
| 12 | Streamlit UI and scenario simulations | Planned |
| 13 | Testing and presentation | Planned |
| 14 | Documentation and final submission | Planned |

## Limitations

The current CPT probabilities are handcrafted for a prototype and have not been estimated or validated using real student data.

The current implementation validates the probabilistic model but does not yet provide study recommendations or calendar scheduling.

## Author

EsmeYang
