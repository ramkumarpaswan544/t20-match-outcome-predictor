# T20 International Match Outcome Predictor

A probabilistic win-probability engine and dynamic team rating model for T20 International cricket.

## Mathematical Formulation

This engine applies an Elo-style framework equivalent to the Bradley-Terry logistic model on a base-10, 400-point scale.

The expected win probability of Team A against Team B is given by:

$$P(\text{Team A}) = \frac{1}{1 + 10^{-(\Delta + \mathrm{Adv})/400}}$$

Where:

- $\Delta = R_A - R_B$ denotes the difference in baseline ratings.
- $\mathrm{Adv} = H_A - H_B$ is the net home advantage, where $H = 30$ for a team playing in its home country and $0$ otherwise.
- At neutral venues (or if both teams are at home), $\mathrm{Adv} = 0$.

## Dynamic Zero-Sum Post-Match Recalibration

Team ratings update iteratively following each match, based on the observed outcome versus the pre-match expectation:

$$R_A' = R_A + K \cdot (S_A - E_A)$$

$$R_B' = R_B + K \cdot (S_B - E_B)$$

Where:

- $S_A \in \{1.0, 0.5, 0.0\}$ denotes a win, tie/no-result, or loss for Team A, and $S_B = 1 - S_A$.
- $E_A$ and $E_B$ are the pre-match expected win probabilities ($E_A + E_B = 1$).
- $K = 32$ is the tournament weight multiplier controlling update sensitivity.
- The expected score uses the home-adjusted ratings, but the change is applied to the base ratings.
- Because $(S_A - E_A) + (S_B - E_B) = 0$, the rating exchange is strictly zero-sum.

> **Data Disclaimer:** Baseline ratings and match outcomes in the demonstration script are synthetic calibration values designed to illustrate the model's dynamics. They do not represent official ICC rankings.

## Running the Model

Clone the repository and run the script with Python 3:

```bash
git clone https://github.com/ramkumarpaswan544/t20-match-outcome-predictor.git
cd t20-match-outcome-predictor
python t20_predictor.py
```

The script uses only the Python standard library, so there is nothing else to install.

## Sample Output

Running `python t20_predictor.py` prints:

```text
=== T20 MATCH PREDICTIONS & DYNAMIC RATING UPDATES ===

Fixture: Australia vs India [Home (Australia)]
  Pre-match Win Odds: Australia 44.3% | India 55.7%
  Result: Australia won
  Updated Strength Index: Australia -> 1697.8 (+17.8) | India -> 1732.2 (-17.8)

Fixture: New Zealand vs England [Home (New Zealand)]
  Pre-match Win Odds: New Zealand 55.7% | England 44.3%
  Result: New Zealand won
  Updated Strength Index: New Zealand -> 1664.2 (+14.2) | England -> 1625.8 (-14.2)

Fixture: South Africa vs India [Neutral (Australia)]
  Pre-match Win Odds: South Africa 33.1% | India 66.9%
  Result: India won
  Updated Strength Index: South Africa -> 1599.4 (-10.6) | India -> 1742.8 (+10.6)

=== UPDATED TOURNAMENT STANDINGS ===
1. India          1742.8
2. Australia      1697.8
3. New Zealand    1664.2
4. England        1625.8
5. South Africa   1599.4
```

## Limitations

- Starting ratings are synthetic placeholders, not estimated from data.
- The home advantage (+30) and K-factor (32) are set by hand, not tuned.
- The model has not been backtested, so its predictive accuracy is unknown.
- `update_ratings` supports ties (S = 0.5), but the demo fixtures only contain decisive results.
- Possible next steps: backtest on historical T20I results (log loss or Brier score) and tune K and the home advantage on that data.
