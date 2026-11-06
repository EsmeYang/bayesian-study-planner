# BayesStudy — Personalized Bayesian Study Planner

A personalized study planning system that uses Bayesian networks to estimate exam readiness and stress risk, with the goal of recommending study schedules that balance academic performance and student well-being.

## Project Status

**In Development — Week 9: Bayesian Inference Completed**

The project is being developed incrementally as part of a university course project.

### Current Features

- Bayesian network implemented using pgmpy
- 8 binary variables and 8 directed edges
- Handcrafted Conditional Probability Tables (CPTs)
- Exam readiness and stress risk modeling
- Model structure and CPT validation
- Bayesian inference using Variable Elimination
- Predictions based on complete or partial student evidence
- 12 automated tests using pytest

### Planned Features

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

## Bayesian Inference

The system uses pgmpy's Variable Elimination algorithm to calculate posterior probabilities based on observed student information.

It estimates:

- P(ExamReadiness = High | Evidence)
- P(StressRisk = High | Evidence)

The system supports both complete and partial evidence.

### Example Student

| Variable | Value |
|---|---|
| Concept1Difficulty | Hard |
| Concept2Difficulty | Easy |
| Concept3Difficulty | Hard |
| Mastery | Low |
| Stress | High |
| DaysUntilExam | Near |

Expected model predictions:

- **High Exam Readiness: 15.00%**
- **High Stress Risk: 90.00%**

These probabilities are generated from the handcrafted CPTs and are not empirically validated predictions of real student outcomes.

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
│   ├── bayesian_model.py
│   └── inference.py
├── tests/
│   ├── test_bayesian_model.py
│   └── test_inference.py
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

## Running Bayesian Inference

Run the example student prediction:

```bash
python -m src.inference
```

Expected output:

```text
Student Prediction
------------------
Exam readiness (High): 15.00%
Stress risk (High): 90.00%
```

The system uses Variable Elimination to calculate posterior probabilities based on the provided student evidence.

## Running Tests

Run all automated tests:

```bash
python -m pytest -v
```

Expected test results:

**12 tests passed.**

Tests cover:

- Bayesian network validity
- Variable and edge counts
- CPT normalization
- Parent relationships
- Probability bounds
- Inference with complete and partial evidence
- Effects of mastery and stress on predictions

## Development Roadmap

| Week | Focus | Status |
|---|---|---|
| 8 | Bayesian network structure and CPTs | Completed |
| 9 | Bayesian inference using Variable Elimination | Completed |
| 10 | Expected utility and decision making | Planned |
| 11 | Google Calendar integration | Planned |
| 12 | Streamlit UI and scenario simulations | Planned |
| 13 | Testing and presentation | Planned |
| 14 | Documentation and final submission | Planned |

## Limitations

The CPT probabilities are handcrafted for a prototype and have not been estimated or validated using real student data.

The current system provides probabilistic predictions but does not yet generate optimal study recommendations or automatically schedule calendar events.

Future development will introduce expected utility calculations to balance exam readiness, stress risk, and study effort.

## Author

EsmeYang

University of British Columbia Okanagan — Computer Science