def probability(rating1: float, rating2: float) -> float:
    """
    Calculate the probability that a player will win a given a match given the rankings of both players
    :param rating1: Player 1's rating
    :param rating2: Player 2's rating
    :return: The probability that player 1 will win
    """
    return round(1.0 / (1.0 + 10 ** ((rating2 - rating1) / 400)), 4)


def calculateElo(rating1: float, rating2: float, outcome: float, K: float = 100) -> (float, float):
    """
    Calculate the new elo ratings for two players based on the outcome of the match
    :param rating1: Player 1's current rating
    :param rating2: Player 2's current rating
    :param K: The sensitivity of the ranking system
    :param outcome: The outcome of the match between the two players (1 for player 1 win, 0 for player 2 win, 1/2 for
    draw
    :return: Player 1's new rating, player 2's new ranking
    """
    P1 = probability(rating1, rating2)
    P2 = probability(rating2, rating1)

    new_rating_1 = rating1 + K * (outcome - P1)
    new_rating_2 = rating2 + K * ((1 - outcome) - P2)

    return new_rating_1, new_rating_2
