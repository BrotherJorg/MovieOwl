from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QDialog,
    QLineEdit,
    QLabel,
    QFormLayout,
    QComboBox,
    QMessageBox,
    QAbstractItemView,
    QHeaderView,
    QInputDialog,
)
from PyQt6.QtCore import Qt, pyqtSignal

from .model import Movie
from features.review_notes.view import ReviewNotesView


class WatchStatusView(QDialog):

    def __init__(self, service, movie, parent=None):
        super().__init__(parent)

        self.service = service
        self.movie = movie

        self.setWindowTitle("Watch Status")

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel(f"Movie: {movie.title}"))

        self.statusCombo = QComboBox()
        self.statusCombo.addItems([
            "Unwatched",
            "Watched",
        ])

        currentStatus = (
            movie.status
            if movie.status in ("Unwatched", "Watched")
            else "Unwatched"
        )
        self.statusCombo.setCurrentText(currentStatus)

        layout.addWidget(self.statusCombo)

        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.saveStatus)
        layout.addWidget(saveButton)

    def saveStatus(self):
        status = self.statusCombo.currentText()

        success = self.service.updateStatus(
            self.movie.id,
            status,
        )

        if success is False:
            QMessageBox.warning(
                self,
                "Invalid Status",
                "The watch status could not be updated.",
            )
            return

        self.accept()


class AddToCollectionView(QDialog):

    def __init__(self, collectionService, movie, parent=None):
        super().__init__(parent)

        self.collectionService = collectionService
        self.movie = movie

        self.setWindowTitle("Add to Collection")
        self.setMinimumWidth(360)

        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel(f"Add <b>{movie.title}</b> to a collection:")
        )

        self.collectionCombo = QComboBox()
        layout.addWidget(self.collectionCombo)

        self.createButton = QPushButton("+ Create Collection")
        self.createButton.clicked.connect(self.createCollection)
        layout.addWidget(self.createButton)

        buttonLayout = QHBoxLayout()

        addButton = QPushButton("Add")
        cancelButton = QPushButton("Cancel")

        addButton.clicked.connect(self.addMovie)
        cancelButton.clicked.connect(self.reject)

        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(cancelButton)

        layout.addLayout(buttonLayout)

        self.loadCollections()

    def loadCollections(self, preferredCollectionId=None):
        self.collectionCombo.clear()

        collections = self.collectionService.getAllCollections()

        for collectionId, collectionName in collections:
            self.collectionCombo.addItem(
                collectionName,
                collectionId,
            )

        if preferredCollectionId is not None:
            index = self.collectionCombo.findData(preferredCollectionId)
            if index >= 0:
                self.collectionCombo.setCurrentIndex(index)
                return

        # Favorites is the default when it exists.
        favoritesIndex = self.collectionCombo.findText(
            "Favorites",
            Qt.MatchFlag.MatchFixedString,
        )

        if favoritesIndex >= 0:
            self.collectionCombo.setCurrentIndex(favoritesIndex)

    def createCollection(self):
        name, ok = QInputDialog.getText(
            self,
            "Create Collection",
            "Collection name:",
        )

        if not ok:
            return

        name = name.strip()

        if not name:
            QMessageBox.warning(
                self,
                "Invalid Collection",
                "Collection name cannot be empty.",
            )
            return

        existing = self.collectionService.getCollectionByName(name)

        if existing is not None:
            QMessageBox.information(
                self,
                "Collection Exists",
                f"The collection '{existing[1]}' already exists.",
            )
            self.loadCollections(existing[0])
            return

        if not self.collectionService.createCollection(name):
            QMessageBox.warning(
                self,
                "Could Not Create Collection",
                "The collection could not be created. Check its name and try again.",
            )
            return

        created = self.collectionService.getCollectionByName(name)

        if created is None:
            QMessageBox.warning(
                self,
                "Collection Error",
                "The collection was not found after creation.",
            )
            self.loadCollections()
            return

        self.loadCollections(created[0])

    def addMovie(self):
        collectionId = self.collectionCombo.currentData()
        collectionName = self.collectionCombo.currentText()

        if collectionId is None:
            QMessageBox.warning(
                self,
                "No Collection",
                "Create or select a collection first.",
            )
            return

        added = self.collectionService.addMovieToCollection(
            self.movie.id,
            collectionId,
        )

        if added:
            QMessageBox.information(
                self,
                "Movie Added",
                f"'{self.movie.title}' was added to '{collectionName}'.",
            )
            self.accept()
        else:
            QMessageBox.information(
                self,
                "Already in Collection",
                f"'{self.movie.title}' is already in '{collectionName}'.",
            )


class ManageMoviesView(QWidget):

    movieChanged = pyqtSignal()

    def __init__(self, service, reviewNotesService, collectionService):
        super().__init__()

        self.service = service
        self.reviewNotesService = reviewNotesService
        self.collectionService = collectionService

        self.setWindowTitle("MovieOWL")
        self.resize(1280, 720)

        self.setup_ui()
        self.loadGenres()
        self.loadMovies()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        titleLabel = QLabel("Manage Movies")
        titleLabel.setObjectName("manageMoviesTitle")
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(titleLabel)

        search_layout = QHBoxLayout()
        main_layout.addLayout(search_layout)

        self.searchInput = QLineEdit()
        self.searchInput.setPlaceholderText("Search movies...")
        search_layout.addWidget(self.searchInput)

        searchButton = QPushButton("Search")
        search_layout.addWidget(searchButton)

        searchButton.clicked.connect(self.searchMovies)
        self.searchInput.returnPressed.connect(self.searchMovies)
        self.searchInput.textChanged.connect(self.searchMovies)

        self.genreCombo = QComboBox()
        self.genreCombo.addItem("All Genres")
        self.genreCombo.currentIndexChanged.connect(self.searchMovies)
        search_layout.addWidget(self.genreCombo)

        self.statusCombo = QComboBox()
        self.statusCombo.addItems([
            "All status",
            "Unwatched",
            "Watched",
        ])
        self.statusCombo.currentIndexChanged.connect(self.searchMovies)
        search_layout.addWidget(self.statusCombo)

        clearFilterButton = QPushButton("Clear Filters")
        clearFilterButton.clicked.connect(self.clearFilters)
        search_layout.addWidget(clearFilterButton)

        action_layout = QHBoxLayout()

        addButton = QPushButton("Add Movie")
        addButton.clicked.connect(self.addMovie)

        viewButton = QPushButton("View Details")
        viewButton.clicked.connect(self.viewDetails)

        editButton = QPushButton("Edit Movie")
        editButton.clicked.connect(self.editMovie)

        deleteButton = QPushButton("Delete Movie")
        deleteButton.clicked.connect(self.deleteMovie)

        statusButton = QPushButton("Watch Status")
        statusButton.clicked.connect(self.changeWatchStatus)

        self.reviewNotesButton = QPushButton("Reviews & Notes")
        self.reviewNotesButton.clicked.connect(self.openReviewNotes)

        self.collectionButton = QPushButton("Add to Collection")
        self.collectionButton.clicked.connect(self.addToCollection)

        action_layout.addWidget(addButton)
        action_layout.addWidget(viewButton)
        action_layout.addWidget(editButton)
        action_layout.addWidget(deleteButton)
        action_layout.addWidget(statusButton)
        action_layout.addWidget(self.reviewNotesButton)
        action_layout.addWidget(self.collectionButton)

        self.movieTable = QTableWidget()
        self.movieTable.setColumnCount(5)
        self.movieTable.setHorizontalHeaderLabels([
            "Title",
            "Genre",
            "Year",
            "Rating",
            "Status",
        ])

        self.movieTable.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        header = self.movieTable.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )

        self.movieTable.setColumnWidth(0, 320)
        self.movieTable.setColumnWidth(1, 220)
        self.movieTable.setColumnWidth(2, 120)
        self.movieTable.setColumnWidth(3, 140)
        self.movieTable.setColumnWidth(4, 220)

        self.movieTable.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.movieTable.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.movieTable.setSortingEnabled(True)
        self.movieTable.horizontalHeader().setStretchLastSection(True)

        main_layout.addWidget(self.movieTable)
        main_layout.addLayout(action_layout)

    def loadMovies(self):
        movies = self.service.getMovie()
        self.movieTable.setSortingEnabled(False)
        self.movieTable.setRowCount(len(movies))

        for row, movie in enumerate(movies):
            titleItem = QTableWidgetItem(movie.title)
            titleItem.setData(Qt.ItemDataRole.UserRole, movie.id)

            self.movieTable.setItem(row, 0, titleItem)
            self.movieTable.setItem(row, 1, QTableWidgetItem(str(movie.genre)))
            self.movieTable.setItem(row, 2, QTableWidgetItem(str(movie.year)))
            self.movieTable.setItem(row, 3, QTableWidgetItem(str(movie.rating)))
            self.movieTable.setItem(row, 4, QTableWidgetItem(movie.status))

        self.movieTable.setSortingEnabled(True)

    def addMovie(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Movie")

        formLayout = QFormLayout()
        dialog.setLayout(formLayout)

        self.titleInput = QLineEdit()
        self.yearInput = QLineEdit()
        self.genreInput = QLineEdit()
        self.ratingInput = QLineEdit()

        formLayout.addRow("Title:", self.titleInput)
        formLayout.addRow("Genre:", self.genreInput)
        formLayout.addRow("Year:", self.yearInput)
        formLayout.addRow("Rating:", self.ratingInput)

        addButton = QPushButton("Add")
        cancelButton = QPushButton("Cancel")
        formLayout.addRow(addButton, cancelButton)

        addButton.clicked.connect(lambda: self.saveMovie(dialog))
        cancelButton.clicked.connect(dialog.reject)

        dialog.exec()

    def saveMovie(self, dialog):
        title = self.titleInput.text().strip()
        genre = self.genreInput.text().strip()
        yearText = self.yearInput.text().strip()
        ratingText = self.ratingInput.text().strip()

        if not title:
            QMessageBox.warning(self, "Invalid Input", "Title cannot be empty.")
            return

        if not genre:
            QMessageBox.warning(self, "Invalid Input", "Genre cannot be empty.")
            return

        try:
            year = int(yearText)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Year must be a whole number.")
            return

        try:
            rating = float(ratingText)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Rating must be a number.")
            return

        if year < 1888 or year > 2100:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid movie year.")
            return

        if rating < 0 or rating > 10:
            QMessageBox.warning(self, "Invalid Input", "Rating must be between 0 and 10.")
            return

        movie = Movie(title, genre, year, rating)
        success = self.service.addMovie(movie)

        if not success:
            QMessageBox.warning(
                self,
                "Duplicate Movie",
                "A movie with this title already exists.",
            )
            return

        self.loadGenres()
        self.loadMovies()
        self.movieChanged.emit()
        dialog.accept()

    def getSelectedMovie(self):
        row = self.movieTable.currentRow()

        if row == -1:
            QMessageBox.warning(
                self,
                "No Movie Selected",
                "Select a movie first.",
            )
            return None

        movieId = self.movieTable.item(
            row, 0
        ).data(Qt.ItemDataRole.UserRole)

        for movie in self.service.getMovie():
            if movie.id == movieId:
                return movie

        QMessageBox.warning(
            self,
            "Movie Not Found",
            "The selected movie could not be found.",
        )
        return None

    def viewDetails(self):
        movie = self.getSelectedMovie()

        if movie is None:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Movie Details")

        layout = QFormLayout()
        dialog.setLayout(layout)

        layout.addRow("Title:", QLabel(movie.title))
        layout.addRow("Genre:", QLabel(movie.genre))
        layout.addRow("Year:", QLabel(str(movie.year)))
        layout.addRow("Rating:", QLabel(str(movie.rating)))
        layout.addRow("Status:", QLabel(movie.status))

        closeButton = QPushButton("Close")
        closeButton.clicked.connect(dialog.accept)
        layout.addRow(closeButton)

        dialog.exec()

    def editMovie(self):
        movie = self.getSelectedMovie()

        if movie is None:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Movie")

        formLayout = QFormLayout()
        dialog.setLayout(formLayout)

        self.titleInput = QLineEdit(movie.title)
        self.yearInput = QLineEdit(str(movie.year))
        self.genreInput = QLineEdit(movie.genre)
        self.ratingInput = QLineEdit(str(movie.rating))

        formLayout.addRow("Title:", self.titleInput)
        formLayout.addRow("Genre:", self.genreInput)
        formLayout.addRow("Year:", self.yearInput)
        formLayout.addRow("Rating:", self.ratingInput)

        saveButton = QPushButton("Save")
        cancelButton = QPushButton("Cancel")
        formLayout.addRow(saveButton, cancelButton)

        saveButton.clicked.connect(lambda: self.saveEdit(dialog, movie))
        cancelButton.clicked.connect(dialog.reject)

        dialog.exec()

    def saveEdit(self, dialog, movie):
        title = self.titleInput.text().strip()
        genre = self.genreInput.text().strip()
        yearText = self.yearInput.text().strip()
        ratingText = self.ratingInput.text().strip()

        if not title:
            QMessageBox.warning(self, "Invalid Input", "Title cannot be empty.")
            return

        if not genre:
            QMessageBox.warning(self, "Invalid Input", "Genre cannot be empty.")
            return

        try:
            year = int(yearText)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Year must be a whole number.")
            return

        try:
            rating = float(ratingText)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Rating must be a number.")
            return

        if year < 1888 or year > 2100:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid movie year.")
            return

        if rating < 0 or rating > 10:
            QMessageBox.warning(self, "Invalid Input", "Rating must be between 0 and 10.")
            return

        movie.title = title
        movie.genre = genre
        movie.year = year
        movie.rating = rating

        self.service.updateMovie(movie)

        self.loadGenres()
        self.searchMovies()
        self.movieChanged.emit()
        dialog.accept()

    def deleteMovie(self):
        movie = self.getSelectedMovie()

        if movie is None:
            return

        confirmation = QMessageBox.question(
            self,
            "Delete Movie",
            f'Delete "{movie.title}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if confirmation != QMessageBox.StandardButton.Yes:
            return

        self.service.deleteMovie(movie.id)

        self.loadGenres()
        self.loadMovies()
        self.movieChanged.emit()

    def searchMovies(self):
        searchText = self.searchInput.text()
        genre = self.genreCombo.currentText()
        status = self.statusCombo.currentText()

        movies = self.service.searchMovies(searchText, genre, status)

        self.movieTable.setSortingEnabled(False)
        self.movieTable.setRowCount(len(movies))

        for row, movie in enumerate(movies):
            titleItem = QTableWidgetItem(movie.title)
            titleItem.setData(Qt.ItemDataRole.UserRole, movie.id)

            self.movieTable.setItem(row, 0, titleItem)
            self.movieTable.setItem(row, 1, QTableWidgetItem(str(movie.genre)))
            self.movieTable.setItem(row, 2, QTableWidgetItem(str(movie.year)))
            self.movieTable.setItem(row, 3, QTableWidgetItem(str(movie.rating)))
            self.movieTable.setItem(row, 4, QTableWidgetItem(movie.status))

        self.movieTable.setSortingEnabled(True)

    def clearFilters(self):
        self.searchInput.clear()

        self.genreCombo.blockSignals(True)
        self.statusCombo.blockSignals(True)

        self.genreCombo.setCurrentIndex(0)
        self.statusCombo.setCurrentIndex(0)

        self.genreCombo.blockSignals(False)
        self.statusCombo.blockSignals(False)

        self.loadMovies()

    def loadGenres(self):
        genres = self.service.getGenres()

        self.genreCombo.blockSignals(True)
        self.genreCombo.clear()
        self.genreCombo.addItem("All Genres")
        self.genreCombo.addItems(genres)
        self.genreCombo.blockSignals(False)

    def changeWatchStatus(self):
        movie = self.getSelectedMovie()

        if movie is None:
            return

        dialog = WatchStatusView(self.service, movie, self)

        if dialog.exec():
            self.searchMovies()
            self.movieChanged.emit()

    def openReviewNotes(self):
        movie = self.getSelectedMovie()

        if movie is None:
            return

        dialog = ReviewNotesView(movie, self.reviewNotesService)

        if dialog.exec():
            self.searchMovies()
            self.movieChanged.emit()

    def addToCollection(self):
        movie = self.getSelectedMovie()

        if movie is None:
            return

        dialog = AddToCollectionView(
            self.collectionService,
            movie,
            self,
        )

        if dialog.exec():
            self.movieChanged.emit()
