
import sys

from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import QApplication

from features.main_Window.view import MainWindow

from features.manage_movies.repository import MovieRepository
from features.manage_movies.service import MovieService
from features.manage_movies.view import ManageMoviesView

from features.review_notes.repository import ReviewNotesRepository
from features.review_notes.service import ReviewNotesService

from features.dashboard.repository import DashboardRepository
from features.dashboard.service import DashboardService
from features.dashboard.view import DashboardView

from features.movie_picker.repository import MoviePickerRepository
from features.movie_picker.service import MoviePickerService
from features.movie_picker.view import MoviePickerView

from features.recommendations.repository import RecommendationRepository
from features.recommendations.service import RecommendationService

from features.collections.repository import CollectionRepository
from features.collections.service import CollectionService
from features.collections.view import CollectionsView


# Movie management
movieRepository = MovieRepository()
movieService = MovieService(movieRepository)

# Review notes
reviewNotesRepository = ReviewNotesRepository()
reviewNotesService = ReviewNotesService(reviewNotesRepository)

# Dashboard
dashboardRepository = DashboardRepository()
dashboardService = DashboardService(dashboardRepository)

# Movie picker
moviePickerRepository = MoviePickerRepository()
moviePickerService = MoviePickerService(moviePickerRepository)

# Recommendations
recommendationRepository = RecommendationRepository()
recommendationService = RecommendationService(recommendationRepository)

# Collections
collectionRepository = CollectionRepository()
collectionService = CollectionService(collectionRepository)


# Application
app = QApplication(sys.argv)

fontId = QFontDatabase.addApplicationFont(
    "assets/fonts/static/manrope-latin-400-normal.ttf"
)

if fontId != -1:
    fontFamily = QFontDatabase.applicationFontFamilies(fontId)[0]
    app.setFont(QFont(fontFamily, 10))

with open("styles/main.qss", "r", encoding="utf-8") as file:
    app.setStyleSheet(file.read())


# Views
manageMoviesView = ManageMoviesView(
    movieService,
    reviewNotesService,
    collectionService
)

dashboardView = DashboardView(
    dashboardService,
    recommendationService
)

moviePickerView = MoviePickerView(moviePickerService)
collectionsView = CollectionsView(collectionService)


# Synchronize views when movies change
manageMoviesView.movieChanged.connect(dashboardView.refresh)
manageMoviesView.movieChanged.connect(collectionsView.refresh)


# Main window
window = MainWindow(
    manageMoviesView,
    dashboardView,
    moviePickerView,
    collectionsView
)

window.show()

sys.exit(app.exec())
