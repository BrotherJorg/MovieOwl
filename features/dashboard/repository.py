
from db.database import Database


class DashboardRepository:

    def __init__(self):
        self.database = Database()

    def getStats(self):
        cursor = self.database.connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM movies
            WHERE status = 'Watched'
        """)
        watched = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM movies
            WHERE status = 'Unwatched'
        """)
        unwatched = cursor.fetchone()[0]

        return {
            "watched": watched,
            "unwatched": unwatched
        }
