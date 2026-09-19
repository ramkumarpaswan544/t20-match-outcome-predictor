"""
T20 International Match Outcome & Win Probability Engine.

Implements an Elo-style rating system mathematically equivalent to the
Bradley-Terry logistic model on a base-10, 400-point scale.

Disclaimer:
The ratings and tournament results defined here are synthetic calibration
placeholders for demonstration purposes, not official ICC published figures.
"""

import math

# Global Model Hyperparameters
HOME_ADVANTAGE = 30  # Rating boost awarded to the host nation
K_FACTOR = 32        # Tournament sensitivity / update multiplier


def calculate_win_probability(rating_a, rating_b, is_home_a=False, is_home_b=False):
    """
    Calculates the expected win probability of Team A against Team B.
    Applies HOME_ADVANTAGE if a team is playing in their home country.
    """
    adv_a = HOME_ADVANTAGE if is_home_a else 0
    adv_b = HOME_ADVANTAGE if is_home_b else 0

    delta = (rating_a + adv_a) - (rating_b + adv_b)
    prob_a = 1.0 / (1.0 + math.pow(10.0, -delta / 400.0))
    prob_b = 1.0 - prob_a
    return prob_a, prob_b


def update_ratings(rating_a, rating_b, actual_score_a, is_home_a=False, is_home_b=False):
    """
    Recalculates team ratings post-match using a zero-sum update rule.
    actual_score_a: 1.0 for Team A win, 0.5 for Tie/No Result, 0.0 for Team B win.
    """
    expected_a, expected_b = calculate_win_probability(rating_a, rating_b, is_home_a, is_home_b)

    new_rating_a = rating_a + K_FACTOR * (actual_score_a - expected_a)
    new_rating_b = rating_b + K_FACTOR * ((1.0 - actual_score_a) - expected_b)

    return round(new_rating_a, 1), round(new_rating_b, 1)


def simulate_tournament():
    # Initial Baseline Strength Ratings (Synthetic demonstration placeholders, Base 1500)
    ratings = {
        "India": 1750.0,
        "Australia": 1680.0,
        "New Zealand": 1650.0,
        "England": 1640.0,
        "South Africa": 1610.0
    }

    # Scheduled Fixtures: (Team A, Team B, Venue Country, Recorded Outcome)
    # Outcome can be: team name (winner), or 'Tie' / 'No Result'
    fixtures = [
        ("Australia", "India", "Australia", "Australia"),
        ("New Zealand", "England", "New Zealand", "New Zealand"),
        ("South Africa", "India", "Australia", "India"),
        ("England", "South Africa", "England", "Tie")
    ]

    print("=== T20 MATCH PREDICTIONS & DYNAMIC RATING UPDATES ===\n")

    for team_a, team_b, venue, outcome in fixtures:
        is_home_a = (team_a == venue)
        is_home_b = (team_b == venue)

        r_a = ratings[team_a]
        r_b = ratings[team_b]

        prob_a, prob_b = calculate_win_probability(r_a, r_b, is_home_a, is_home_b)

        venue_desc = f"Home ({venue})" if (is_home_a or is_home_b) else f"Neutral ({venue})"
        print(f"Fixture: {team_a} vs {team_b} [{venue_desc}]")
        print(f"  Pre-match Win Odds: {team_a} {prob_a * 100:.1f}% | {team_b} {prob_b * 100:.1f}%")
        print(f"  Recorded Outcome: {outcome}")

        # Handle Win, Tie / No Result, and Loss; reject unrecognised outcomes
        if outcome == team_a:
            score_a = 1.0
        elif outcome == team_b:
            score_a = 0.0
        elif outcome in ("Tie", "No Result"):
            score_a = 0.5
        else:
            raise ValueError(f"Unknown outcome '{outcome}' for {team_a} vs {team_b}")

        new_r_a, new_r_b = update_ratings(r_a, r_b, score_a, is_home_a=is_home_a, is_home_b=is_home_b)

        ratings[team_a] = new_r_a
        ratings[team_b] = new_r_b

        print(f"  Updated Strength: {team_a} -> {new_r_a} ({new_r_a - r_a:+.1f}) | "
              f"{team_b} -> {new_r_b} ({new_r_b - r_b:+.1f})\n")

    print("=== FINAL TOURNAMENT STANDINGS ===")
    ranked = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
    for rank, (team, rating) in enumerate(ranked, start=1):
        print(f"{rank}. {team:<14} {rating}")


if __name__ == "__main__":
    simulate_tournament()
