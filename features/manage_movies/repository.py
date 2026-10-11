from .model import Movie
from db.database import Database


class MovieRepository:

    VALID_STATUSES = ("Unwatched", "Watched")

    def __init__(self):
        self.database = Database()

    def add(self, movie):
        cursor = self.database.connection.cursor()

        cursor.execute("""
            SELECT id
            FROM Movies
            WHERE title = ?
        """, (movie.title,))

        if cursor.fetchone():
            return False

        cursor.execute("""
            INSERT INTO Movies (title, genre, year, rating)
            VALUES (?, ?, ?, ?)
        """, (
            movie.title,
            movie.genre,
            movie.year,
            movie.rating
        ))

        self.database.connection.commit()
        return True

    def getAll(self):
        cursor = self.database.connection.cursor()

        cursor.execute("""
            SELECT id, title, genre, year, rating, status
            FROM Movies
        """)

        movies = []

        for row in cursor.fetchall():
            movie = Movie(
                row[1],
                row[2],
                row[3],
                row[4],
                row[0],
                row[5]
            )
            movies.append(movie)

        return movies

    def updateMovie(self, movie):
        cursor = self.database.connection.cursor()

        cursor.execute("""
            UPDATE Movies
            SET title = ?, genre = ?, year = ?, rating = ?
            WHERE id = ?
        """, (
            movie.title,
            movie.genre,
            movie.year,
            movie.rating,
            movie.id
        ))

        self.database.connection.commit()

    def deleteMovie(self, movie_id):
        cursor = self.database.connection.cursor()

        cursor.execute("""
            DELETE FROM Movies
            WHERE id = ?
        """, (movie_id,))

        self.database.connection.commit()

    def searchMovies(self, searchText, genre, status):
        conditions = []
        values = []

        if searchText:
            conditions.append("title LIKE ?")
            values.append(f"%{searchText}%")

        if genre != "All Genres":
            conditions.append("genre = ?")
            values.append(genre)

        if status != "All status":
            conditions.append("status = ?")
            values.append(status)

        query = """
            SELECT id, title, genre, year, rating, status
            FROM Movies
        """

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY title"

        cursor = self.database.connection.cursor()
        cursor.execute(query, values)

        movies = []

        for row in cursor.fetchall():
            movie = Movie(
                row[1],
                row[2],
                row[3],
                row[4],
                row[0],
                row[5]
            )
            movies.append(movie)

        return movies

    def getGenres(self):
        cursor = self.database.connection.cursor()

        cursor.execute("""
            SELECT DISTINCT genre
            FROM Movies
            ORDER BY genre
        """)

        return [row[0] for row in cursor.fetchall()]

    def updateStatus(self, movie_id, status):
        if status not in self.VALID_STATUSES:
            return False

        cursor = self.database.connection.cursor()

        cursor.execute("""
            UPDATE Movies
            SET status = ?
            WHERE id = ?
        """, (status, movie_id))

        self.database.connection.commit()
        return cursor.rowcount > 0
