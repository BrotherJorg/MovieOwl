from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QInputDialog,
    QMessageBox,
    QListWidget,
    QListWidgetItem
)
from PyQt6.QtCore import Qt


class CollectionsView(QWidget):

    def __init__(self, service):
        super().__init__()

        self.service = service
        self.currentCollectionId = None
        self.currentCollectionName = None

        self.setObjectName("collectionsView")

        self.setup_ui()
        self.loadCollections()

    def setup_ui(self):
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(30, 30, 30, 30)
        mainLayout.setSpacing(12)
        self.setLayout(mainLayout)

        titleLabel = QLabel("Collections")
        titleLabel.setObjectName("collectionsTitle")
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(titleLabel)

        collectionButtonLayout = QHBoxLayout()

        createButton = QPushButton("+ New Collection")
        createButton.setObjectName("collectionsCreateButton")

        deleteButton = QPushButton("Delete Collection")
        deleteButton.setObjectName("collectionsDeleteButton")

        collectionButtonLayout.addWidget(createButton)
        collectionButtonLayout.addWidget(deleteButton)
        collectionButtonLayout.addStretch()
        mainLayout.addLayout(collectionButtonLayout)

        self.collectionList = QListWidget()
        self.collectionList.setObjectName("collectionList")
        mainLayout.addWidget(self.collectionList)

        self.collectionTitle = QLabel("Select a collection")
        self.collectionTitle.setObjectName("collectionTitle")
        self.collectionTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(self.collectionTitle)

        movieButtonLayout = QHBoxLayout()

        self.addMovieButton = QPushButton("Add Movie")
        self.removeMovieButton = QPushButton("Remove Movie")

        movieButtonLayout.addWidget(self.addMovieButton)
        movieButtonLayout.addWidget(self.removeMovieButton)
        mainLayout.addLayout(movieButtonLayout)

        self.movieList = QListWidget()
        self.movieList.setObjectName("collectionMovieList")
        mainLayout.addWidget(self.movieList)

        createButton.clicked.connect(self.createCollection)
        deleteButton.clicked.connect(self.deleteCollection)
        self.collectionList.itemClicked.connect(self.openCollection)
        self.addMovieButton.clicked.connect(self.addMovie)
        self.removeMovieButton.clicked.connect(self.removeMovie)

    def refresh(self):
        """Refresh collections and the currently selected collection."""
        previousCollectionId = self.currentCollectionId

        self.loadCollections()

        if previousCollectionId is not None:
            for index in range(self.collectionList.count()):
                item = self.collectionList.item(index)

                if item.data(Qt.ItemDataRole.UserRole) == previousCollectionId:
                    self.collectionList.setCurrentItem(item)
                    self.openCollection(item)
                    return

        self.currentCollectionId = None
        self.currentCollectionName = None
        self.collectionTitle.setText("Select a collection")
        self.movieList.clear()

    def loadCollections(self):
        previousCollectionId = self.currentCollectionId
        self.collectionList.clear()

        collections = self.service.getAllCollections()

        for collection in collections:
            collectionId, collectionName = collection[0], collection[1]

            item = QListWidgetItem(collectionName)
            item.setData(Qt.ItemDataRole.UserRole, collectionId)
            self.collectionList.addItem(item)

        if not collections:
            self.currentCollectionId = None
            self.currentCollectionName = None
            self.collectionTitle.setText("No collections created")
            self.movieList.clear()
            return

        if previousCollectionId is not None:
            for index in range(self.collectionList.count()):
                item = self.collectionList.item(index)

                if item.data(Qt.ItemDataRole.UserRole) == previousCollectionId:
                    self.collectionList.setCurrentItem(item)
                    self.currentCollectionId = previousCollectionId
                    self.currentCollectionName = item.text()
                    self.loadMovies()
                    return

    def createCollection(self):
        name, ok = QInputDialog.getText(
            self,
            "New Collection",
            "Collection name:"
        )

        if not ok:
            return

        if not self.service.createCollection(name):
            QMessageBox.warning(
                self,
                "Invalid Collection",
                "Collection name must be non-empty and unique."
            )
            return

        self.loadCollections()

    def deleteCollection(self):
        item = self.collectionList.currentItem()

        if item is None:
            QMessageBox.warning(
                self,
                "No Collection Selected",
                "Select a collection first."
            )
            return

        collectionId = item.data(Qt.ItemDataRole.UserRole)
        collectionName = item.text()

        answer = QMessageBox.question(
            self,
            "Delete Collection",
            f"Delete '{collectionName}'?"
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        self.service.deleteCollection(collectionId)

        self.currentCollectionId = None
        self.currentCollectionName = None
        self.collectionTitle.setText("Select a collection")
        self.movieList.clear()
        self.loadCollections()

    def openCollection(self, item):
        collectionId = item.data(Qt.ItemDataRole.UserRole)
        collectionName = item.text()

        self.currentCollectionId = collectionId
        self.currentCollectionName = collectionName
        self.collectionTitle.setText(f"Movies in {collectionName}")

        self.loadMovies()

    def loadMovies(self):
        self.movieList.clear()

        if self.currentCollectionId is None:
            return

        movies = self.service.getMoviesInCollection(
            self.currentCollectionId
        )

        for movie in movies:
            movieId, title, genre, year, rating, status = movie[:6]

            text = (
                f"{title}  |  {genre}  |  {year}  |  "
                f"Rating: {rating}  |  {status}"
            )

            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, movieId)
            self.movieList.addItem(item)

    def addMovie(self):
        if self.currentCollectionId is None:
            QMessageBox.warning(
                self,
                "No Collection Selected",
                "Select a collection first."
            )
            return

        allMovies = self.service.getAllMovies()

        if not allMovies:
            QMessageBox.information(
                self,
                "No Movies",
                "There are no movies to add."
            )
            return

        currentMovies = self.service.getMoviesInCollection(
            self.currentCollectionId
        )
        currentMovieIds = {movie[0] for movie in currentMovies}

        availableMovies = [
            movie for movie in allMovies
            if movie[0] not in currentMovieIds
        ]

        if not availableMovies:
            QMessageBox.information(
                self,
                "Collection Full",
                "All movies are already in this collection."
            )
            return

        movieNames = [movie[1] for movie in availableMovies]

        movieName, ok = QInputDialog.getItem(
            self,
            "Add Movie",
            "Select a movie:",
            movieNames,
            0,
            False
        )

        if not ok:
            return

        selectedMovie = next(
            (movie for movie in availableMovies if movie[1] == movieName),
            None
        )

        if selectedMovie is None:
            return

        self.service.addMovieToCollection(
            selectedMovie[0],
            self.currentCollectionId
        )

        self.loadMovies()

    def removeMovie(self):
        if self.currentCollectionId is None:
            QMessageBox.warning(
                self,
                "No Collection Selected",
                "Select a collection first."
            )
            return

        item = self.movieList.currentItem()

        if item is None:
            QMessageBox.warning(
                self,
                "No Movie Selected",
                "Select a movie first."
            )
            return

        movieId = item.data(Qt.ItemDataRole.UserRole)

        self.service.removeMovieFromCollection(
            movieId,
            self.currentCollectionId
        )

        self.loadMovies()
