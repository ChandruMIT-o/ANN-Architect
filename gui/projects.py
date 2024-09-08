from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCompleter, QGridLayout, QScrollArea, QSizePolicy, QAction, QSpacerItem
from PyQt5.QtCore import Qt
from qfluentwidgets import (MessageBoxBase, SubtitleLabel, DisplayLabel, PushButton, setTheme, Theme, CaptionLabel, SearchLineEdit,
                            IconWidget, CardWidget, BodyLabel, PillPushButton, FluentIcon, InfoBadge, InfoLevel, ToolButton, TransparentToolButton,
                            TransparentDropDownToolButton, RoundMenu, PrimaryToolButton)
from qfluentwidgets import FluentIcon as FIF
import sys

if __name__ == '__main__':
    from _right_section import RightSection
    from _code_gen_dialog import GeneratedCodeMessageBox
    from _summary_gen_dialog import GeneratedSummaryMessageBox
    from _model_designer import ModelDesigner
else:
    from gui._right_section import RightSection
    from gui._code_gen_dialog import GeneratedCodeMessageBox
    from gui._summary_gen_dialog import GeneratedSummaryMessageBox
    from gui._model_designer import ModelDesigner

class ProjectsScreen(QWidget):
    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setStyleSheet('ProjectsScreen{background:"#272727"}')

        self.hBoxLayout = QHBoxLayout(self)

        self.modelBuildingSectionLayout = QVBoxLayout()
        self.modelBuildingSectionLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.rightSectionLayout = QVBoxLayout()
        self.rightSectionLayout.setAlignment(Qt.AlignTop)

        self.titleLabel = SubtitleLabel("Deep CNN", self)
        self.titleLabel.setObjectName("titleLabelPS")
        self.titleLabel.setStyleSheet("""#titleLabelPS{
                font: 900 26px 'Segoe UI';
                background: transparent;
                border-radius: 8px;
                color: white;
                }
                """)
        
        self.modelBuildingSectionLayout.addWidget(self.titleLabel)

        self.modelDesigner = ModelDesigner()
        self.modelBuildingSectionLayout.addWidget(self.modelDesigner, alignment=Qt.AlignmentFlag.AlignTop)

        self.bottomButtonSectionLayout = QHBoxLayout()
        self.bottomButtonSectionLayout.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.codeGenerationButton = PushButton("Code", self, FIF.CODE)
        self.codeGenerationButton.clicked.connect(self.showCodeDialog)
        self.summaryGenerationButton = PushButton("Summary", self, FIF.BOOK_SHELF)
        self.summaryGenerationButton.clicked.connect(self.showSummaryDialog)
        self.saveProjectButton = PushButton("Save", self, FIF.SAVE)
        self.codeGenerationButton.setMaximumWidth(300)
        self.summaryGenerationButton.setMaximumWidth(300)

        self.rightSection = RightSection()

        self.bottomButtonSectionLayout.addWidget(self.codeGenerationButton)
        self.bottomButtonSectionLayout.addWidget(self.summaryGenerationButton)
        vspacer = QSpacerItem(100000, 100000, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.bottomButtonSectionLayout.addItem(vspacer)
        self.bottomButtonSectionLayout.addWidget(self.saveProjectButton, alignment=Qt.AlignmentFlag.AlignRight)

        spacer = QSpacerItem(40, 100000, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.modelBuildingSectionLayout.addItem(spacer)

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