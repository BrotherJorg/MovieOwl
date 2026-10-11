from .repository import CollectionRepository


class CollectionService:

    def __init__(self, repository):
        self.repository = repository

    def createCollection(self, name):
        if not name or not name.strip():
            return False

        return self.repository.createCollection(name.strip())

    def getAllCollections(self):
        return self.repository.getAllCollections()

    def getCollectionByName(self, name):
        if not name:
            return None

        targetName = name.strip().casefold()

        for collection in self.getAllCollections():
            if collection[1].casefold() == targetName:
                return collection

        return None

    def deleteCollection(self, collection_id):
        return self.repository.deleteCollection(collection_id)

    def addMovieToCollection(self, movie_id, collection_id):
        return self.repository.addMovieToCollection(
            movie_id,
            collection_id
        )

    def removeMovieFromCollection(self, movie_id, collection_id):
        return self.repository.removeMovieFromCollection(
            movie_id,
            collection_id
        )

    def getMoviesInCollection(self, collection_id):
        return self.repository.getMoviesInCollection(collection_id)

    def getAllMovies(self):
        return self.repository.getAllMovies()
