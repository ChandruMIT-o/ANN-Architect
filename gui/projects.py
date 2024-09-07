from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCompleter, QGridLayout, QScrollArea, QSizePolicy, QAction
from PyQt5.QtCore import Qt
from qfluentwidgets import (MessageBoxBase, SubtitleLabel, LineEdit, PushButton, setTheme, Theme, CaptionLabel, SearchLineEdit,
                            IconWidget, CardWidget, BodyLabel, PillPushButton, FluentIcon, InfoBadge, InfoLevel, ToolButton, TransparentToolButton,
                            TransparentDropDownToolButton, RoundMenu, PrimaryToolButton, TitleLabel)
from qfluentwidgets import FluentIcon as FIF
import sys
from components.right_section import RightSection
from components.code_gen_dialog import GeneratedCodeMessageBox
from components.summary_gen_dialog import GeneratedSummaryMessageBox

class ProjectsScreen(QWidget):
    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setStyleSheet('ProjectsScreen{background:"#272727"}')

        self.hBoxLayout = QHBoxLayout(self)

        self.modelBuildingSectionLayout = QVBoxLayout()
        self.rightSectionLayout = QVBoxLayout()
        self.modelBuildingSectionLayout.setAlignment(Qt.AlignBottom)
        self.rightSectionLayout.setAlignment(Qt.AlignTop)

        self.bottomButtonSectionLayout = QHBoxLayout()
        self.bottomButtonSectionLayout.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.codeGenerationButton = PushButton("Code", self, FIF.CODE)
        self.codeGenerationButton.clicked.connect(self.showCodeDialog)
        self.summaryGenerationButton = PushButton("Summary", self, FIF.BOOK_SHELF)
        self.summaryGenerationButton.clicked.connect(self.showSummaryDialog)
        self.codeGenerationButton.setMaximumWidth(300)
        self.summaryGenerationButton.setMaximumWidth(300)

        self.rightSection = RightSection()

        self.bottomButtonSectionLayout.addWidget(self.codeGenerationButton)
        self.bottomButtonSectionLayout.addWidget(self.summaryGenerationButton)

        self.modelBuildingSectionLayout.addLayout(self.bottomButtonSectionLayout)
        self.rightSectionLayout.addWidget(self.rightSection)

        self.hBoxLayout.addLayout(self.modelBuildingSectionLayout,2)
        self.hBoxLayout.addLayout(self.rightSectionLayout,1)
        self.resize(800, 800)
        self.setLayout(self.hBoxLayout)

    def showCodeDialog(self):
        w = GeneratedCodeMessageBox(self)
        if w.exec():
            pass

    def showSummaryDialog(self):
        w = GeneratedSummaryMessageBox(self)
        if w.exec():
            pass
if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = ProjectsScreen()
    w.show()
    app.exec_()