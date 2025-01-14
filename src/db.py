import sqlite3
import re
from datetime import datetime
from enum import Enum

from src.elo import calculateElo


class DatabaseError(Exception):
    """Raised when database-related errors occur."""
    pass


class ResultType(Enum):
    WIN = 1
    DRAW = 1/2
    LOSS = 0


class ChessDatabase:
    def __init__(self, databasePath):
        self.connection = connection = sqlite3.connect(databasePath)
        self.cursor = connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def _sanitizeString(self, string: str):
        """Validate string to prevent SQL injection."""
        if not re.match(r"^[\w\u0400-\u04FF\s]+$", string):
            raise DatabaseError(f'Invalid string "{string}" for the database')

    def _getDateNow(self) -> str:
        """Get the current datetime as a string."""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def _tableExists(self, tableName: str):
        """Check if a table exists in the database."""
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}'")
        return self.cursor.fetchone()

    def _checkPlayerExists(self, player_name: str):
        """Raise an error if the player does not exist."""
        if not self._tableExists(player_name):
            raise DatabaseError(f"Player {player_name} does not exist.")

    def createGameRecordDB(self):
        """Create the 'games' table for recording matches."""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS games 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            DatePlayed DATETIME NOT NULL, 
            Player1 STRING NOT NULL, 
            Player2 STRING NOT NULL, 
            Result FLOAT NOT NULL)""")

    def addPlayer(self, playerName: str):
        """Add a new player to the database."""
        self._sanitizeString(playerName)

        playerExists = self._tableExists(playerName)

        if playerExists:
            raise DatabaseError(f"The player {playerName} already exists in the database")

        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {playerName} "
                            f"(id INTEGER PRIMARY KEY, "
                            f"DatePlayed DATETIME NOT NULL, "
                            f"Ranking FLOAT NOT NULL)")

        self.cursor.execute(f"INSERT INTO {playerName} "
                            f"(id, DatePlayed, Ranking) VALUES "
                            f"(?, ?, ?) ", (0, self._getDateNow(), 1000))

        self.connection.commit()

    def reportResult(self, player1: str, player2: str, result: Enum):
        """Record the result of a game and update player rankings."""
        for player in (player1, player2):
            self._sanitizeString(player1)
            self._checkPlayerExists(player)

        if not isinstance(result, ResultType):
            raise ValueError(f"Invalid result type: {result}")

        date_played = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.cursor.execute(f"INSERT INTO games "
                            f"(DatePlayed, Player1, Player2, Result) "
                            f"VALUES (?, ?, ?, ?)", (date_played, player1, player2, result.name))

        uniqueID = self.cursor.lastrowid

        player1Elo = self._getElo(player1)
        player2Elo = self._getElo(player2)

        player1NewElo, player2NewElo = calculateElo(player1Elo, player2Elo, result.value)

        self.cursor.execute(f"INSERT INTO {player1} "
                            f"(id, DatePlayed, Ranking) VALUES "
                            f"(?, ?, ?)", (uniqueID, date_played, player1NewElo))
        self.cursor.execute(f"INSERT INTO {player2} "
                            f"(id, DatePlayed, Ranking) VALUES "
                            f"(?, ?, ?)", (uniqueID, date_played, player2NewElo))
        self.connection.commit()

    def _getElo(self, playerName: str):
        """Get the latest Elo rating of a player."""
        self._checkPlayerExists(playerName)
        self.cursor.execute(f"SELECT Ranking FROM {playerName} WHERE id=(SELECT MAX(id) FROM {playerName})")

        return self.cursor.fetchone()[0]

    def close(self):
        """Close the database connection."""
        self.connection.close()


if __name__ == "__main__":
    with ChessDatabase("../db/chessRankings.db") as db:
        db.createGameRecordDB()
        try:
            db.addPlayer("Player1")
        except DatabaseError as e:
            print(e)
        try:
            db.addPlayer("Player2")
        except DatabaseError as e:
            print(e)
        db.reportResult("Player1", "Player2", ResultType.DRAW)

        db.cursor.execute("SELECT * FROM Player1")
        rows = db.cursor.fetchall()
        for row in rows[len(rows) - 10: len(rows)]:
            print(row)

        print()

        db.cursor.execute("SELECT * FROM Player2")
        rows = db.cursor.fetchall()
        for row in rows[len(rows) - 10: len(rows)]:
            print(row)

        print()

        db.cursor.execute("SELECT * FROM games")
        rows = db.cursor.fetchall()
        for row in rows[len(rows) - 10: len(rows)]:
            print(row)