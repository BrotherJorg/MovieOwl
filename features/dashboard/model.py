class DashboardStats:
    def __init__(
        self,
        totalMovies,
        watched,
        unwatched,
        averageRating,
        genreCounts
    ):

        self.totalMovies = totalMovies
        self.watched = watched
        self.unwatched = unwatched
        self.averageRating = averageRating
        self.genreCounts = genreCounts