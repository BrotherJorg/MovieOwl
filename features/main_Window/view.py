from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget
)

from PyQt6.QtGui import QIcon

from PyQt6.QtCore import (
    QSize,
    Qt,
    QPropertyAnimation,
    QParallelAnimationGroup
)

from pathlib import Path


class MainWindow(QMainWindow):

    EXPANDED_WIDTH = 180
    COLLAPSED_WIDTH = 56

    def __init__(
        self,
        manageMoviesView,
        dashboardView,
        moviePickerView,
        collectionsView
    ):
        super().__init__()

        self.manageMoviesView = manageMoviesView
        self.dashboardView = dashboardView
        self.moviePickerView = moviePickerView
        self.collectionsView = collectionsView

        self.setWindowTitle("MovieOWL")
        self.resize(1000, 700)

        self.setup_ui()

    def setup_ui(self):

        self.sidebarAnimation = None

        centralWidget = QWidget()

        mainLayout = QHBoxLayout(centralWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        icon_dir = Path("assets/icons")

        # Sidebar
        self.sidebarWidget = QWidget()
        self.sidebarWidget.setObjectName("sidebarWidget")

        self.sidebarWidget.setMinimumWidth(self.EXPANDED_WIDTH)
        self.sidebarWidget.setMaximumWidth(self.EXPANDED_WIDTH)

        sidebar = QVBoxLayout()
        sidebar.setSpacing(10)
        sidebar.setContentsMargins(10, 10, 10, 10)

        self.sidebarWidget.setLayout(sidebar)

        self.manageButton = QPushButton("Manage Movies")
        self.dashboardButton = QPushButton("Dashboard")
        self.moviePickerButton = QPushButton("Movie Picker")
        self.collectionsButton = QPushButton("Collections")

        self.dashboardButton.setIcon(
            QIcon(str(icon_dir / "dashboard.svg"))
        )
        self.manageButton.setIcon(
            QIcon(str(icon_dir / "movie.svg"))
        )
        self.moviePickerButton.setIcon(
            QIcon(str(icon_dir / "moviepicker.svg"))
        )
        self.collectionsButton.setIcon(
            QIcon(str(icon_dir / "collections.svg"))
        )

        for button in [
            self.dashboardButton,
            self.manageButton,
            self.moviePickerButton,
            self.collectionsButton
        ]:
            button.setIconSize(QSize(20, 20))

        sidebar.addWidget(self.dashboardButton)
        sidebar.addWidget(self.manageButton)
        sidebar.addWidget(self.moviePickerButton)
        sidebar.addWidget(self.collectionsButton)
        sidebar.addStretch()

        self.collapseButton = QPushButton("Collapse")
        self.collapseButton.setIcon(
            QIcon(str(icon_dir / "sidebar.svg"))
        )
        self.collapseButton.setIconSize(QSize(20, 20))
        self.collapseButton.setLayoutDirection(
            Qt.LayoutDirection.LeftToRight
        )

        self.collapseButton.clicked.connect(self.toggleSidebar)
        sidebar.addWidget(self.collapseButton)

        # Main stack
        self.stack = QStackedWidget()

        self.stack.addWidget(self.manageMoviesView)
        self.stack.addWidget(self.dashboardView)
        self.stack.addWidget(self.moviePickerView)
        self.stack.addWidget(self.collectionsView)

        mainLayout.addWidget(self.sidebarWidget)
        mainLayout.addWidget(self.stack, 1)

        self.setCentralWidget(centralWidget)

        # Navigation
        self.manageButton.clicked.connect(
            lambda: self.stack.setCurrentWidget(
                self.manageMoviesView
            )
        )

        self.dashboardButton.clicked.connect(
            lambda: self.stack.setCurrentWidget(
                self.dashboardView
            )
        )

        self.moviePickerButton.clicked.connect(
            lambda: self.stack.setCurrentWidget(
                self.moviePickerView
            )
        )

        self.collectionsButton.clicked.connect(
            lambda: self.stack.setCurrentWidget(
                self.collectionsView
            )
        )

        # Live synchronization
        self.manageMoviesView.movieChanged.connect(
            self.dashboardView.refresh
        )

        self.stack.setCurrentWidget(self.dashboardView)

    def toggleSidebar(self):

        if self.sidebarWidget.width() == self.EXPANDED_WIDTH:

            startWidth = self.EXPANDED_WIDTH
            endWidth = self.COLLAPSED_WIDTH

            self.manageButton.setText("")
            self.dashboardButton.setText("")
            self.moviePickerButton.setText("")
            self.collectionsButton.setText("")
            self.collapseButton.setText("")

        else:

            startWidth = self.COLLAPSED_WIDTH
            endWidth = self.EXPANDED_WIDTH

            self.manageButton.setText("Manage Movies")
            self.dashboardButton.setText("Dashboard")
            self.moviePickerButton.setText("Movie Picker")
            self.collectionsButton.setText("Collections")
            self.collapseButton.setText("Collapse")

        self.sidebarWidget.setMinimumWidth(startWidth)
        self.sidebarWidget.setMaximumWidth(startWidth)

        self.sidebarAnimation = QParallelAnimationGroup(self)

        minimumAnimation = QPropertyAnimation(
            self.sidebarWidget,
            b"minimumWidth"
        )

        maximumAnimation = QPropertyAnimation(
            self.sidebarWidget,
            b"maximumWidth"
        )

        for animation in [
            minimumAnimation,
            maximumAnimation
        ]:
            animation.setDuration(220)
            animation.setStartValue(startWidth)
            animation.setEndValue(endWidth)
            self.sidebarAnimation.addAnimation(animation)

        self.sidebarAnimation.start()
