
# Bayesian Network Design

## 1. Overview

BayesStudy is a personalized study planning system that uses a Bayesian network to estimate a student's exam readiness and stress risk.

The model contains 8 binary variables and 8 directed edges.

## 2. Variables

| Variable | States | Description |
|---|---|---|
| Concept1Difficulty | Easy, Hard | Difficulty of concept 1 |
| Concept2Difficulty | Easy, Hard | Difficulty of concept 2 |
| Concept3Difficulty | Easy, Hard | Difficulty of concept 3 |
| Mastery | Low, High | Student's overall mastery |
| Stress | Low, High | Student's current stress |
| DaysUntilExam | Near, Far | Whether the exam is approaching |
| ExamReadiness | Low, High | Predicted exam readiness |
| StressRisk | Low, High | Predicted stress risk |

## 3. Network Structure

The Bayesian network has the following directed edges:

- Concept1Difficulty -> ExamReadiness
- Concept2Difficulty -> ExamReadiness
- Concept3Difficulty -> ExamReadiness
- Mastery -> ExamReadiness
- Stress -> ExamReadiness
- DaysUntilExam -> ExamReadiness
- Stress -> StressRisk
- DaysUntilExam -> StressRisk

The model is a directed acyclic graph (DAG).

## 4. Root CPTs

The six root variables have the following prior probabilities:

| Variable | First state | Probability | Second state | Probability |
|---|---|---|---|---|
| Concept1Difficulty | Easy | 0.60 | Hard | 0.40 |
| Concept2Difficulty | Easy | 0.50 | Hard | 0.50 |
| Concept3Difficulty | Easy | 0.40 | Hard | 0.60 |
| Mastery | Low | 0.50 | High | 0.50 |
| Stress | Low | 0.60 | High | 0.40 |
| DaysUntilExam | Near | 0.40 | Far | 0.60 |

These probabilities are handcrafted assumptions for the prototype rather than estimates from a real student dataset.

## 5. ExamReadiness CPT

ExamReadiness depends on six parent variables:

- Concept1Difficulty
- Concept2Difficulty
- Concept3Difficulty
- Mastery
- Stress
- DaysUntilExam

There are 2^6 = 64 possible parent-state combinations.

The probability of high exam readiness is calculated using a handcrafted scoring rule:

1. Start with P(High) = 0.65.
2. Subtract 0.10 for each difficult concept.
3. Add 0.25 if Mastery is High.
4. Subtract 0.15 if Stress is High.
5. Subtract 0.15 if DaysUntilExam is Near.
6. Clip the final probability to the interval [0.05, 0.95].

For every parent-state combination:

P(ExamReadiness = Low) = 1 - P(ExamReadiness = High)

This rule generates the 64-column CPT.

## 6. StressRisk CPT

StressRisk depends on Stress and DaysUntilExam.

| Stress | DaysUntilExam | P(Low Risk) | P(High Risk) |
|---|---|---|---|
| Low | Near | 0.65 | 0.35 |
| Low | Far | 0.90 | 0.10 |
| High | Near | 0.10 | 0.90 |
| High | Far | 0.45 | 0.55 |

These values are handcrafted assumptions. Higher current stress and an approaching exam increase the modeled probability of high stress risk.

## 7. Model Validation

The network is implemented using pgmpy.

Validation checks confirm:

- 8 variables
- 8 directed edges
- 8 CPTs
- All CPT probability columns sum to 1
- ExamReadiness has the expected 6 parents
- StressRisk has the expected 2 parents
- model.check_model() returns True

Seven automated tests are implemented in tests/test_bayesian_model.py.

## 8. Planned Extensions

Week 9:
Use Variable Elimination to calculate posterior probabilities of ExamReadiness and StressRisk from observed student information.

Week 10:
Implement expected utility calculations for three actions:
- Intensive study: 5-hour study block
- Light review: 1-hour review
- Rest day

The decision model will balance predicted exam success, stress, and study effort.

Week 11:
Integrate Google Calendar API for scheduling.

Week 12:
Build a Streamlit interface and evaluate different student scenarios.

Weeks 13-14:
Complete testing, presentation, documentation, and submission.
