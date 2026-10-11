from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
)
from PyQt6.QtCore import Qt


class DashboardView(QWidget):

    def __init__(self, service, recommendationService=None):
        super().__init__()

        self.service = service
        self.recommendationService = recommendationService

        self.setWindowTitle("Dashboard")
        self.resize(900, 600)
        self.setObjectName("dashboardView")

        self.setup_ui()
        self.loadDashboard()

    def setup_ui(self):
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.setSpacing(16)
        self.setLayout(mainLayout)

        title = QLabel("Dashboard")
        title.setObjectName("dashboardTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(title)

        statsLayout = QHBoxLayout()
        statsLayout.setSpacing(12)

        watchedCard = QFrame()
        watchedCard.setObjectName("dashboardCard")
        watchedLayout = QVBoxLayout(watchedCard)

        watchedTitle = QLabel("Watched Movies")
        watchedTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.watchedValue = QLabel("0")
        self.watchedValue.setObjectName("dashboardValue")
        self.watchedValue.setAlignment(Qt.AlignmentFlag.AlignCenter)

        watchedLayout.addWidget(watchedTitle)
        watchedLayout.addWidget(self.watchedValue)

        unwatchedCard = QFrame()
        unwatchedCard.setObjectName("dashboardCard")
        unwatchedLayout = QVBoxLayout(unwatchedCard)

        unwatchedTitle = QLabel("Unwatched Movies")
        unwatchedTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.unwatchedValue = QLabel("0")
        self.unwatchedValue.setObjectName("dashboardValue")
        self.unwatchedValue.setAlignment(Qt.AlignmentFlag.AlignCenter)

        unwatchedLayout.addWidget(unwatchedTitle)
        unwatchedLayout.addWidget(self.unwatchedValue)

        statsLayout.addWidget(watchedCard)
        statsLayout.addWidget(unwatchedCard)
        mainLayout.addLayout(statsLayout)

        recommendationsFrame = QFrame()
        recommendationsFrame.setObjectName("dashboardSection")

        recommendationsLayout = QVBoxLayout(recommendationsFrame)

        recommendationsTitle = QLabel("Recommended Movies")
        recommendationsTitle.setObjectName("dashboardSectionTitle")
        recommendationsTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.recommendationsLabel = QLabel()
        self.recommendationsLabel.setAlignment(
            Qt.AlignmentFlag.AlignCenter |
            Qt.AlignmentFlag.AlignTop
        )
        self.recommendationsLabel.setWordWrap(True)

        recommendationsLayout.addWidget(recommendationsTitle)
        recommendationsLayout.addWidget(self.recommendationsLabel)

        mainLayout.addWidget(recommendationsFrame, 1)

    def loadDashboard(self):
        stats = self.service.getStats()

        self.watchedValue.setText(str(stats["watched"]))
        self.unwatchedValue.setText(str(stats["unwatched"]))

        self.loadRecommendations()

    def loadRecommendations(self):
        if self.recommendationService is None:
            self.recommendationsLabel.setText(
                "Recommendations are not connected yet."
            )
            return

        recommendations = (
            self.recommendationService.getRecommendations()
        )

        if not recommendations:
            self.recommendationsLabel.setText(
                "Add movies to see recommendations."
            )
            return

        lines = []

        for index, recommendation in enumerate(
            recommendations, start=1
        ):
            movie = recommendation.movie
            reason = recommendation.reason

            lines.append(
                f"{index}. {movie[1]} ({movie[3]})\n"
                f"   Genre: {movie[2]} | Rating: {movie[4]}\n"
                f"   {reason}"
            )

        self.recommendationsLabel.setText("\n\n".join(lines))

    def refresh(self):
        self.loadDashboard()
