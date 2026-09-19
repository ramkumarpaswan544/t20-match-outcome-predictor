# T20 International Match Outcome Predictor

A probabilistic win-probability engine and dynamic team rating model for T20 International cricket.

## Mathematical Formulation

This engine applies an **Elo-style framework equivalent to the Bradley-Terry logistic model** on a base-10, 400-point scale. 

The expected win probability of Team A against Team B is given by:

$$P(\text{Team A}) = \frac{1}{1 + 10^{-(\Delta + \text{Adv}) / 400}}$$

Where:
* $\Delta = R_A - R_B$ denotes the difference in baseline ratings.
* $\text{Adv} = +30$ rating points assigned when a team plays in their home country.
* For pure neutral venues, $\text{Adv} = 0$.

### Dynamic Zero-Sum Post-Match Recalibration

Team ratings update iteratively following each match based on observed outcome versus pre-match expectation:

$$R'_A = R_A + K \cdot (S_A - E_A)$$
$$R'_B = R_B + K \cdot (S_B - E_B)$$

Where:
* $S_A \in \{1.0, 0.5, 0.0\}$ denotes a win, tie/no-result, or loss for Team A.
* $E_A$ and $E_B$ are the pre-match expected win probabilities ($E_A + E_B = 1$).
* $K = 32$ is the tournament weight multiplier controlling update sensitivity.
* Because $(S_A - E_A) + (S_B - E_B) = 0$, the rating exchange is strictly zero-sum.

> **Data Disclaimer:** Baseline ratings and match outcomes in the demonstration script are synthetic calibration values designed to illustrate the model's dynamics. They do not represent official ICC rankings.

## Running the Model

Clone the repository and run the script with Python 3:

```bash
git clone [https://github.com/ramkumarpaswan544/t20-match-outcome-predictor.git](https://github.com/ramkumarpaswan544/t20-match-outcome-predictor.git)
cd t20-match-outcome-predictor
python t20_predictor.py
