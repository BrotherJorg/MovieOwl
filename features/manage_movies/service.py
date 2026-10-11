class MovieService:

    def __init__(self, repository):
        self.repository = repository

    def addMovie(self, movie):
        return self.repository.add(movie)

    def getMovie(self):
        return self.repository.getAll()

    def updateMovie(self, movie):
        self.repository.updateMovie(movie)

    def deleteMovie(self, movie_id):
        self.repository.deleteMovie(movie_id)

    def searchMovies(self, searchText, genre, status):
        return self.repository.searchMovies(
            searchText,
            genre,
            status
        )

    def getGenres(self):
        return self.repository.getGenres()

    def updateStatus(self, movie_id, status):
        validStatuses = [
            "Unwatched",
            "Watched"
        ]

        if status not in validStatuses:
            return False

        self.repository.updateStatus(movie_id, status)
        return True
