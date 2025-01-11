import sqlite3

def createDatabase():
    pass

# def reportResult(p1, p2, result, ):




if __name__ == "__main__":
    connection = sqlite3.connect("../db/chessRankings.db")
    cursor = connection.cursor()


    cursor.execute("SELECT * FROM player1")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.execute("SELECT * FROM player2")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.execute("SELECT * FROM games")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
