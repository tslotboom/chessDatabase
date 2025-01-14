import unittest
from src.elo import *


class TestElo(unittest.TestCase):

    def testProbability(self):
        # Test with equal ratings
        self.assertAlmostEqual(probability(1400, 1400), 0.5, places=4)

        # Test with Player 1 having a higher rating
        self.assertAlmostEqual(probability(1600, 1400), 0.7597, places=4)

        # Test with Player 2 having a higher rating
        self.assertAlmostEqual(probability(1400, 1600), 0.2403, places=4)

        # Test with a large rating difference
        self.assertAlmostEqual(probability(2000, 1000), 0.9968, places=4)

    def testCalculateElo(self):
        # Test with equal ratings and Player 1 winning
        rating1, rating2 = calculateElo(1000, 1000, 1)
        self.assertAlmostEqual(rating1, 1020, places=4)
        self.assertAlmostEqual(rating2, 980, places=4)

        # Test with equal ratings and Player 2 winning
        rating1, rating2 = calculateElo(1000, 1000, 0)
        self.assertAlmostEqual(rating1, 980, places=4)
        self.assertAlmostEqual(rating2, 1020, places=4)

        # Test with equal ratings and a draw
        rating1, rating2 = calculateElo(1000, 1000, 1/2)
        self.assertAlmostEqual(rating1, 1000, places=4)
        self.assertAlmostEqual(rating2, 1000, places=4)

        # Test with Player 1 having a higher rating and winning
        rating1, rating2 = calculateElo(1200, 800, 1)
        self.assertAlmostEqual(rating1, 1203.636, places=2)
        self.assertAlmostEqual(rating2, 796.364, places=2)

        # Test with Player 1 having a higher rating and losing
        rating1, rating2 = calculateElo(1200, 800, 0)
        self.assertAlmostEqual(rating1, 1163.636, places=2)
        self.assertAlmostEqual(rating2, 836.364, places=2)

        # Test with Player 2 having a higher rating and Player 1 winning
        rating1, rating2 = calculateElo(800, 1200, 1)
        self.assertAlmostEqual(rating1, 836.364, places=2)
        self.assertAlmostEqual(rating2, 1163.636, places=2)

        # Test with Player 2 having a higher rating and Player 1 losing
        rating1, rating2 = calculateElo(800, 1200, 0)
        self.assertAlmostEqual(rating1, 796.364, places=2)
        self.assertAlmostEqual(rating2, 1203.636, places=2)

        # Test with a draw and different ratings
        rating1, rating2 = calculateElo(800, 1200, 0.5)
        self.assertAlmostEqual(rating1, 816.364, places=2)
        self.assertAlmostEqual(rating2, 1183.636, places=2)


if __name__ == '__main__':
    unittest.main()
