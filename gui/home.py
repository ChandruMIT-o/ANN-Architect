# coding:utf-8
import sys
import re

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCompleter, QGridLayout, QScrollArea, QSizePolicy

from qfluentwidgets import (MessageBoxBase, SubtitleLabel, LineEdit, PushButton, setTheme, Theme, CaptionLabel, SearchLineEdit,
                            IconWidget, CardWidget, BodyLabel, PillPushButton, FluentIcon, InfoBadge, InfoLevel)
from qfluentwidgets import FluentIcon as FIF

class AppCard(CardWidget):

    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.openButton = PushButton('Clone', self)
        self.moreButton = PillPushButton(FluentIcon.HEART, "Fav", self)

        self.architypeInfoBadge = InfoBadge("Architype: CNN", self, InfoLevel.INFOAMTION)
        self.totalParametersInfoBadge = InfoBadge("Total Parameters: 1.2B", self, InfoLevel.INFOAMTION)


        self.vCardLayout = QVBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()
        self.hButtonLayout = QHBoxLayout()

        self.setFixedWidth(250)
        self.setFixedHeight(250)

        self.iconWidget.setFixedSize(48, 48)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.openButton.setFixedWidth(120)

        self.vCardLayout.setContentsMargins(20, 20, 20, 20)
        self.vCardLayout.setSpacing(10)
        self.vCardLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignLeft)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)
        self.vCardLayout.addLayout(self.vBoxLayout)
        self.vCardLayout.addWidget(self.architypeInfoBadge, 0, Qt.AlignLeft)
        self.vCardLayout.addWidget(self.totalParametersInfoBadge, 0, Qt.AlignLeft)

        self.vCardLayout.addStretch(1)

        self.hButtonLayout.addWidget(self.openButton)
        self.hButtonLayout.addWidget(self.moreButton)
        self.hButtonLayout.setAlignment(Qt.AlignCenter)

        self.vCardLayout.addLayout(self.hButtonLayout)

        self.moreButton.setFixedSize(80, 32)

class CustomMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('Project Name', self)
        self.urlLineEdit = LineEdit(self)

        self.urlLineEdit.setPlaceholderText('Identifier Naming Convention')
        self.urlLineEdit.setClearButtonEnabled(True)

        self.validationText = CaptionLabel('• Min 3 Characters • Identifier Naming', self)
        self.nameAlreadyPresentText = CaptionLabel('• Name Already in Use!', self) 
        self.nameAlreadyPresentText.setStyleSheet("QLabel{color: '#FFC300'}")
        self.nameAlreadyPresentText.setVisible(False)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.urlLineEdit)
        self.viewLayout.addWidget(self.validationText)
        self.viewLayout.addWidget(self.nameAlreadyPresentText)

        self.yesButton.setText('Create')
        self.cancelButton.setText('Cancel')

        self.widget.setMinimumWidth(350)
        self.yesButton.setDisabled(True)
        self.urlLineEdit.textChanged.connect(self._validateUrl)

        # self.hideYesButton()

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
            self.validationText.setStyleSheet("QLabel{color: '#06D001'}")
        else:
            self.validationText.setStyleSheet("QLabel{color: white}")
        self.nameAlreadyPresentText.setVisible(not self.isNameUnique(text))

class HomeScreen(QWidget):

    def __init__(self):
        super().__init__()
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
        self.searchButton = PushButton("Search",self)
        self.searchButton.setMaximumWidth(100)


        self.projectCardWidget = QWidget()
        self.projectCardWidget.setStyleSheet('QWidget{background: "#272727"; border: 0px;}')
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
        self.gridProjectsLayout.setHorizontalSpacing(20)
        self.gridProjectsLayout.setVerticalSpacing(20)

        for x in range(5):
            for y in range(5):

                self.gridProjectsLayout.addWidget(AppCard(
                    icon=":/qfluentwidgets/images/logo.png",
                    title="DEEP CNN Model",
                    content="Last Updated 3 days ago."
                ), x, y)

        self.resize(600, 600)
        
        self.hSearchLayout.addWidget(self.searchLineEdit)
        self.hSearchLayout.addWidget(self.searchButton)
        self.hSearchLayout.setAlignment(Qt.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.projectCardWidget.setLayout(self.gridProjectsLayout)
        self.scroll_area.setWidget(self.projectCardWidget)

        self.vBoxLayout.addWidget(self.createProjectButton, stretch=1, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addLayout(self.hSearchLayout, stretch=1)
        self.vBoxLayout.addWidget(self.scroll_area, stretch=5, alignment=Qt.AlignmentFlag.AlignTop)

        self.vBoxLayout.setContentsMargins(50, 50, 50, 50)

        self.createProjectButton.clicked.connect(self.showDialog)

        # ------------------------- GET GLOBAL PROJECT NAMES ----------------
        stands = [
            "Star Platinum", "Hierophant Green",
            "Made in Haven", "King Crimson",
            "Silver Chariot", "Crazy diamond",
            "Metallica", "Another One Bites The Dust",
            "Heaven's Door", "Killer Queen",
            "The Grateful Dead", "Stone Free",
            "The World", "Sticky Fingers",
            "Ozone Baby", "Love Love Deluxe",
            "Hermit Purple", "Gold Experience",
            "King Nothing", "Paper Moon King",
            "Scary Monster", "Mandom",
            "20th Century Boy", "Tusk Act 4",
            "Ball Breaker", "Sex Pistols",
            "D4C • Love Train", "Born This Way",
            "SOFT & WET", "Paisley Park",
            "Wonder of U", "Walking Heart",
            "Cream Starter", "November Rain",
            "Smooth Operators", "The Matte Kudasai"
        ]
        self.completer = QCompleter(stands, self.searchLineEdit)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setMaxVisibleItems(10)
        self.searchLineEdit.setCompleter(self.completer)
        # ------------------------- GET GLOBAL PROJECT NAMES ----------------

    def showDialog(self):
        w = CustomMessageBox(self)
        if w.exec():
            print(w.urlLineEdit.text())

if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = HomeScreen()
    w.show()
    app.exec_()