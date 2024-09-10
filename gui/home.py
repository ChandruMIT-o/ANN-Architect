# coding:utf-8
import sys
import re
import random
import datetime

from PyQt5.QtCore import Qt, QUrl, QStringListModel
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCompleter, QGridLayout, QScrollArea, QSizePolicy

from qfluentwidgets import (MessageBoxBase, SubtitleLabel, LineEdit, PushButton, setTheme, Theme, CaptionLabel, SearchLineEdit, ComboBox,
                            IconWidget, CardWidget, BodyLabel, PillPushButton, FluentIcon, InfoBadge, InfoLevel, TransparentToolButton)
from qfluentwidgets import FluentIcon as FIF

if __name__ == '__main__':
    from _summary_gen_dialog import GeneratedSummaryMessageBox
else:
    from gui._summary_gen_dialog import GeneratedSummaryMessageBox

class ProjectAppCard(CardWidget):

    def __init__(self, icon, title, lastUpdated, owner, archiType, totalParameters, is_fav,  parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.titleLabel.setObjectName("ProjectAppCardTitle")
        self.titleLabel.setStyleSheet("""#ProjectAppCardTitle{
                                        background: transparent; 
                                        color: white;
                                    }""")
        self.contentLabel = CaptionLabel(lastUpdated, self)
        self.contentLabel.setObjectName("ProjectAppCardContent")
        self.contentLabel.setStyleSheet("""#ProjectAppCardContent{
                                        background: transparent; 
                                        color: white;
                                    }""")
        self.openButton = PushButton('Clone', self)
        self.moreButton = PillPushButton(FluentIcon.HEART, "Fav", self)
        self.moreButton.setChecked(is_fav)
        self.moreButton.clicked.connect(self.updateFavs)

        self.infoSummaryButton = TransparentToolButton(FIF.INFO, self)
        self.infoSummaryButton.setFixedSize(32, 32)
        self.infoSummaryButton.clicked.connect(self.displaySummaryDialog)

        self.architypeInfoBadge = InfoBadge.info(archiType)
        self.totalParametersInfoBadge = InfoBadge.attension(totalParameters)
        self.ownerInfoBadge = InfoBadge.warning(owner)

        self.vCardLayout = QVBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()
        self.hButtonLayout = QHBoxLayout()
        self.hTitleLayout = QHBoxLayout()

        self.setFixedWidth(250)
        self.setFixedHeight(250)

        self.iconWidget.setFixedSize(32, 32)
        self.openButton.setFixedWidth(120)

        self.vCardLayout.setContentsMargins(20, 20, 20, 20)
        self.vCardLayout.setSpacing(10)

        self.hTitleLayout.addWidget(self.iconWidget, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.hTitleLayout.addWidget(self.infoSummaryButton, 0, alignment=Qt.AlignmentFlag.AlignRight)

        self.vCardLayout.addLayout(self.hTitleLayout)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignLeft)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)
        self.vCardLayout.addLayout(self.vBoxLayout)
        self.vCardLayout.addWidget(self.ownerInfoBadge, 0, Qt.AlignLeft)
        self.vCardLayout.addWidget(self.architypeInfoBadge, 0, Qt.AlignLeft)
        self.vCardLayout.addWidget(self.totalParametersInfoBadge, 0, Qt.AlignLeft)
        self.vCardLayout.addStretch(1)

        self.hButtonLayout.addWidget(self.openButton)
        self.hButtonLayout.addWidget(self.moreButton)
        self.hButtonLayout.setAlignment(Qt.AlignCenter)

        self.vCardLayout.addLayout(self.hButtonLayout)

        self.moreButton.setFixedSize(80, 32)

    def displaySummaryDialog(self):
        w = GeneratedSummaryMessageBox(self)
        if w.exec():
            pass

    def updateFavs(self):

        val = self.moreButton.isChecked()

        # TODO: This function updates the favourites table based on true or false in the variable val
        pass

class CustomMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('Project Name', self)
        self.archiTypeLabel = CaptionLabel('Architecture', self)
        self.urlLineEdit = LineEdit(self)
        self.archiTypeCombobox = ComboBox(self)
        self.hBoxLayout = QHBoxLayout(self)

        self.archiTypeCombobox.setPlaceholderText("CNN")

        items = ['CNN', 'Deep CNN', 'RNN', 'ANN']
        self.archiTypeCombobox.addItems(items)
        self.archiTypeCombobox.setCurrentIndex(-1)

        self.urlLineEdit.setPlaceholderText('Identifier Naming Convention')
        self.urlLineEdit.setClearButtonEnabled(True)

        self.validationText = CaptionLabel('• Min 3 Characters • Identifier Naming', self)
        self.validationText.setObjectName('validationTextProjectName')
        self.nameAlreadyPresentText = CaptionLabel('• Name Already in Use!', self) 
        self.nameAlreadyPresentText.setObjectName('nameAlreadyPresentTextProjectName')
        self.nameAlreadyPresentText.setStyleSheet("#nameAlreadyPresentTextProjectName{color: '#FFC300'}")
        self.nameAlreadyPresentText.setVisible(False)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.urlLineEdit)
        self.viewLayout.addWidget(self.validationText)
        self.viewLayout.addWidget(self.nameAlreadyPresentText)
        self.viewLayout.addWidget(self.archiTypeLabel)
        self.viewLayout.addWidget(self.archiTypeCombobox)

        self.yesButton.setText('Create')
        self.yesButton.clicked.connect(self.updateProjectsTable)
        self.cancelButton.setText('Cancel')

        self.widget.setMinimumWidth(350)
        self.yesButton.setDisabled(True)
        self.urlLineEdit.textChanged.connect(self._validateUrl)

        # self.hideYesButton()

    def updateProjectsTable(self):

        # TODO: This function updates the projects table based on the inputted data
        project_name = self.urlLineEdit.text()
        architype = self.archiTypeCombobox.text()
        today = datetime.datetime.now() # Change this to date format
        # TODO: Find other parameters as well
        pass

    def isNameValid(self, project_name):

        if not project_name: return False
        if len(project_name) < 3: return False
        return self.is_valid_identifier(project_name) and self.isNameUnique(project_name)
    
    def isNameUnique(self, project_name):
        # -------------------------------- GET PROJECT NAMES FROM SQLITE -----------------------------
        project_names = ['rameez', 'rameez1', 'rameez']
        # -------------------------------- GET PROJECT NAMES FROM SQLITE -----------------------------
        return project_name not in project_names

    def is_valid_identifier(self, identifier: str) -> bool:
        pattern = r'^[A-Za-z_][A-Za-z0-9_]*$'
        return bool(re.match(pattern, identifier))

    def _validateUrl(self, text):
        self.yesButton.setEnabled(self.isNameValid(text))
        if self.isNameValid(text):
            self.validationText.setStyleSheet("#validationTextProjectName{color: '#06D001'}")
        else:
            self.validationText.setStyleSheet("#validationTextProjectName{color: white}")
        self.nameAlreadyPresentText.setVisible(not self.isNameUnique(text))

class HomeScreen(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        setTheme(Theme.DARK)
        self.setStyleSheet('HomeScreen{background:"#272727"}')

        self.vBoxLayout = QVBoxLayout(self)

        self.createProjectButton = PushButton(FIF.ADD_TO,'Create New Project', self)
        self.createProjectButton.setMinimumHeight(50)
        self.createProjectButton.setMinimumWidth(300)
        self.createProjectButton.setMaximumWidth(500)

        self.hSearchLayout = QHBoxLayout()

        self.searchLineEdit = SearchLineEdit(self)
        self.searchLineEdit.setMaximumWidth(400)
        self.searchLineEdit.textChanged.connect(self.init_search_complete)
        self.searchButton = PushButton("Search",self)
        self.searchButton.setMaximumWidth(100)
        self.searchButton.clicked.connect(self.repopulate_layout)

        self.projectCardWidget = QWidget()
        self.projectCardWidget.setObjectName("projectCardWidget")
        self.projectCardWidget.setStyleSheet('#projectCardWidget{background: "#272727"; border: 0px;}')
        self.scroll_area = QScrollArea()
        self.scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.scroll_area.setStyleSheet('''
                                        QScrollBar:vertical {
        background: transparent;  /* Background color of the scrollbar */
        width: 8px;
    }
    QScrollBar::handle:vertical {
        background: #36454F;  /* Color of the slider (handle) */
        border-radius: 4px;  /* Radius for rounded corners of the handle */
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background: none;  /* Remove arrows from the scrollbar */
        height: 0px;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;  /* Remove the scroll background */
    }
    QScrollBar:horizontal {
        background: transparent;  /* Background color of the scrollbar */
        height: 8px;
    }
    QScrollBar::handle:horizontal {
        background: #36454F;  /* Color of the slider (handle) */
        border-radius: 4px;  /* Radius for rounded corners of the handle */
    }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        background: none;  /* Remove arrows from the scrollbar */
        width: 0px;
    }
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
        background: none;  /* Remove the scroll background */
    }
    QWidget {
        border: 0px;  /* Remove borders from QWidget */
    }        
                                        ''')
        self.scroll_area.setWidgetResizable(True)  # Makes sure the grid layout resizes properly
        
        self.gridProjectsLayout = QGridLayout()
        self.gridProjectsLayout.setAlignment(Qt.AlignCenter)
        self.gridProjectsLayout.setSpacing(30)

        self.resize(600, 600)
        
        self.hSearchLayout.addWidget(self.searchLineEdit)
        self.hSearchLayout.addWidget(self.searchButton)
        self.hSearchLayout.setAlignment(Qt.AlignHCenter)

        self.projectCardWidget.setLayout(self.gridProjectsLayout)
        self.scroll_area.setWidget(self.projectCardWidget)

        self.vBoxLayout.addWidget(self.createProjectButton, alignment=Qt.AlignHCenter)
        self.vBoxLayout.addLayout(self.hSearchLayout)
        self.vBoxLayout.addWidget(self.scroll_area)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setSpacing(30)

        self.vBoxLayout.setContentsMargins(20, 50, 20, 20)

        self.createProjectButton.clicked.connect(self.showDialog)

        self.completer = QCompleter([], self.searchLineEdit)

        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setMaxVisibleItems(10)
        self.searchLineEdit.setCompleter(self.completer)

        self.init_top_k(True)

    def showDialog(self):
        w = CustomMessageBox(self)
        if w.exec():
            print(w.urlLineEdit.text())

    def init_search_complete(self):
        
        searchContent = self.searchLineEdit.text()

        if searchContent:

            # TODO: Use the above search content to fetch relevant titles for search suggestions
            # ? Store them in the below lists somehow

            project_names = [
                    "Celestial Convergence",
                    "Quantum Leap",
                    "Nebula Nexus",
                    "Stellar Surge",
                    "Cosmic Crucible",
                    "Galactic Gateway",
                    "Stardust Symphony",
                    "Celestial Choir",
                    "Nebula Nebula",
                    "Stellar Storm"
                ]
        else:
            project_names = []

        self.completer.setModel(QStringListModel(project_names))

    def init_top_k(self, switch):

        if switch:

            # TODO: Implement logic to fetch and display top k global projects
            # ? Store them in the below lists somehow
            self.titleSamples = ["Deep CNN Model", "BERT Language Model", "GAN Image Generator", "Transformer-Based Translator", "Autoencoder Anomaly Detector"]
            self.ownerSamples = ["Rameez Akther", "Alice Smith", "Bob Johnson", "Charlie Brown", "David Lee"]
            self.lastUpdatedSamples = [datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30)) for _ in range(5)]
            self.totalParametersSamples = [random.randint(1, 100) for _ in range(5)]
            self.archiTypeSamples = ["CNN", "RNN", "Transformer", "GAN", "Autoencoder"]

            # ! Fav separately should be fetched

            self.favs = [True, False, False, True, False]

        else:

            searchContent = self.searchLineEdit.text()

            # TODO: Use the above search content to fetch relevant records
            # ? Store them in the below lists somehow

            self.titleSamples = [
                "Advanced Speech Recognition System",  # Longer title
                "Building a Chatbot (Interactive)",  # Title with explanation in parentheses
                f"Project: Image Colorizer (v{random.randint(1, 10)})",  # Title with version number
                *["Simple {} Model".format(random.choice(["Regression", "Classification"])) for _ in range(2)]  # Dynamically generated titles
            ]
            self.ownerSamples = [
                "王晓明 (Wáng Xiǎomíng)",  # Chinese name
                "キム・민수 (Kim Min-soo)",  # Korean name
                "Aïcha Diallo",  # African name
                random.choice(["Pedro Hernandez", "Isabella Rossi"]),  # Random European name
                random.choice(["Sarah Jones", "David Williams"])  # Random American name
            ]
            self.lastUpdatedSamples = [datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30)) for _ in range(5)]
            self.totalParametersSamples = [random.randint(1000, 100000) for _ in range(5)]
            self.archiTypeSamples = random.sample(["CNN", "RNN", "Transformer", "GAN", "Autoencoder"], 4) + random.sample(self.archiTypeSamples, 1)  # Guarantees at least 1 duplicate
            
            # ! Fav separately should be fetched
            
            self.favs = [True, False, False, True, False]

        ind = 0

        for x,y in self._generate_matrix_indices(len(self.titleSamples), 5):
            self.gridProjectsLayout.addWidget(ProjectAppCard(
                icon="gui\images\logo.png",
                title=self.titleSamples[ind],
                owner=self.ownerSamples[ind],
                lastUpdated=self.lastUpdatedSamples[ind].strftime("%B %d, %Y"),  # Format date as needed
                totalParameters=f"{self.totalParametersSamples[ind]} B parameters",
                archiType=self.archiTypeSamples[ind],
                is_fav=self.favs[ind],
                parent=self
            ), x, y)

            ind += 1

    def repopulate_layout(self):

        searchContent = self.searchLineEdit.text()
        while self.gridProjectsLayout.count() > 0:
            item = self.gridProjectsLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if searchContent:
            self.init_top_k(False)
        else:
            self.init_top_k(True)

    def _generate_matrix_indices(self, rows, cols):
        """Generates a list of tuples representing the indices of a matrix.
        """
        import math

        temp = rows
        rows = int(math.ceil(rows / cols))

        indices = []
        for row in range(rows):
            for col in range(cols):
                indices.append((row, col))
        return indices[:temp]

if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    # with open("gui\styles\dark\main.qss", "r") as qss_file:
    #     app.setStyleSheet(qss_file.read())

    w = HomeScreen()
    w.show()
    app.exec_()