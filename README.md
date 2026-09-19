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

- $S_A \in \lbrace 1.0, 0.5, 0.0 \rbrace$ denotes a win, tie/no-result, or loss for Team A, and $S_B = 1 - S_A$.
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
  Recorded Outcome: Australia
  Updated Strength: Australia -> 1697.8 (+17.8) | India -> 1732.2 (-17.8)

Fixture: New Zealand vs England [Home (New Zealand)]
  Pre-match Win Odds: New Zealand 55.7% | England 44.3%
  Recorded Outcome: New Zealand
  Updated Strength: New Zealand -> 1664.2 (+14.2) | England -> 1625.8 (-14.2)

Fixture: South Africa vs India [Neutral (Australia)]
  Pre-match Win Odds: South Africa 33.1% | India 66.9%
  Recorded Outcome: India
  Updated Strength: South Africa -> 1599.4 (-10.6) | India -> 1742.8 (+10.6)

Fixture: England vs South Africa [Home (England)]
  Pre-match Win Odds: England 58.0% | South Africa 42.0%
  Recorded Outcome: Tie
  Updated Strength: England -> 1623.2 (-2.6) | South Africa -> 1602.0 (+2.6)

=== FINAL TOURNAMENT STANDINGS ===
1. India          1742.8
2. Australia      1697.8
3. New Zealand    1664.2
4. England        1623.2
5. South Africa   1602.0
```

In the last fixture, a tie scores 0.5 for both teams. That is below what the favourite (England, 58%) was expected to score, so England loses a little rating and South Africa gains the same amount.

## Limitations

- Starting ratings are synthetic placeholders, not estimated from data.
- The home advantage (`HOME_ADVANTAGE = 30`) and K-factor (`K_FACTOR = 32`) are set by hand, not tuned.
- The model has not been backtested, so its predictive accuracy is unknown.
- Ties and no-results are scored as 0.5 for both teams. The model does not estimate the probability of a tie itself.
- Possible next steps: backtest on historical T20I results (log loss or Brier score) and tune K and the home advantage on that data.
