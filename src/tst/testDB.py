import unittest
import sqlite3
from datetime import datetime
from enum import Enum
from src.db import ChessDatabase, DatabaseError, ResultType


class TestChessDatabase(unittest.TestCase):

	def setUp(self):
		"""Set up an in-memory database for testing."""
		self.db = ChessDatabase("fakepath")
		self.db.connection = sqlite3.connect(':memory:')
		self.db.cursor = self.db.connection.cursor()
		self.db.createGameRecordDB()

	def tearDown(self):
		self.db.close()
		
	def testTableExists(self):
		self.db.addPlayer("Player1")
		self.assertTrue(self.db._tableExists("Player1"), "Player1 table should exist")
		self.assertFalse(self.db._tableExists("OOGABOOGA"), "OOGABOOGA table should not exist")

	def testCheckPlayerExists(self):
		self.db.addPlayer("Player1")
		with self.assertRaises(DatabaseError):
			self.db._checkPlayerExists("ARGABLARG")
		self.db._checkPlayerExists("Player1")

	def testAddPlayer(self):
		self.db.addPlayer("Player1")
		self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Player1'")
		table = self.db.cursor.fetchone()
		self.assertIsNotNone(table, "Player1 table should exist.")

		elo = self.db._getElo("Player1")
		self.assertAlmostEqual(elo, 1000)

		with self.assertRaises(DatabaseError):
			self.db.addPlayer("OR 1=1")

		with self.assertRaises(DatabaseError):
			self.db.addPlayer("Player@123")

		with self.assertRaises(DatabaseError):
			self.db.addPlayer("Player1")

	def testReportResults(self):
		self.db.addPlayer("Player1")
		self.db.addPlayer("Player2")

		initialElo1 = self.db._getElo("Player1")
		initialElo2 = self.db._getElo("Player2")

		self.db.reportResult("Player1", "Player2", ResultType.DRAW)

		newElo1 = self.db._getElo("Player1")
		newElo2 = self.db._getElo("Player2")

		self.assertAlmostEqual(newElo1, initialElo1, 4, "Player1 Elo should still be equal to its initial value.")
		self.assertAlmostEqual(newElo2, initialElo2, 4, "Player2 Elo should still be equal to its initial value.")

		self.db.reportResult("Player1", "Player2", ResultType.WIN)

		newElo1 = self.db._getElo("Player1")
		newElo2 = self.db._getElo("Player2")

		self.assertNotEqual(newElo1, initialElo1, "Player1 Elo should be updated.")
		self.assertNotEqual(newElo2, initialElo2, "Player2 Elo should be updated.")

		self.db.reportResult("Player1", "Player2", ResultType.LOSS)

		newNewElo1 = self.db._getElo("Player1")
		newNewElo2 = self.db._getElo("Player2")

		self.assertNotEqual(newElo1, newNewElo1, "Player1 Elo should be updated again.")
		self.assertNotEqual(newElo2, newNewElo2, "Player2 Elo should be updated again.")

		with self.assertRaises(DatabaseError):
			self.db.reportResult("Player1", "UNGA BUNGA", ResultType.WIN)

		with self.assertRaises(ValueError):
			self.db.reportResult("Player1", "Player2", "INVALID")

	def testGetElo(self):
		self.db.addPlayer("Player1")
		self.db.addPlayer("Player2")

		self.assertAlmostEqual(self.db._getElo("Player1"), 1000, 4, "New players start the game with an elo of 1000")
		self.assertAlmostEqual(self.db._getElo("Player2"), 1000, 4, "New players start the game with an elo of 1000")


