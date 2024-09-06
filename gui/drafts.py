from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCompleter, QGridLayout, QScrollArea, QSizePolicy, QAction
from PyQt5.QtCore import Qt
from qfluentwidgets import (MessageBoxBase, SubtitleLabel, LineEdit, PushButton, setTheme, Theme, CaptionLabel, SearchLineEdit,
                            IconWidget, CardWidget, BodyLabel, PillPushButton, FluentIcon, InfoBadge, InfoLevel, ToolButton, TransparentToolButton,
                            TransparentDropDownToolButton, RoundMenu, PrimaryToolButton, TitleLabel)
from qfluentwidgets import FluentIcon as FIF
import sys

class VerticalCard(CardWidget):

    def __init__(self, icon, title, content, parent=None, saved = False):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.openButton = PushButton('Edit', self)

        self.architypeInfoBadge = InfoBadge("Architype: CNN", self, InfoLevel.INFOAMTION)
        self.totalParametersInfoBadge = InfoBadge("Total Parameters: 1.2B", self, InfoLevel.INFOAMTION)

        if saved:
            self.moreButton = PillPushButton(FluentIcon.PEOPLE, 'Publish')

            self.menu = RoundMenu(parent=self)
            self.menu.addAction(QAction(FIF.COPY.icon(), 'Duplicate'))
            self.menu.addAction(QAction(FIF.DELETE.icon(), 'Delete'))

            self.transparentDropDownToolButton = TransparentDropDownToolButton(FIF.MORE, self)
            self.transparentDropDownToolButton.setMenu(self.menu)
        else:
            self.moreButton = PrimaryToolButton(FluentIcon.SAVE)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(48, 48)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.openButton.setFixedWidth(120)

        self.hBoxLayout.setContentsMargins(20, 11, 20, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignVCenter)
        
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.hBoxLayout.addWidget(self.architypeInfoBadge, 0, Qt.AlignVCenter)
        self.hBoxLayout.addWidget(self.totalParametersInfoBadge, 0, Qt.AlignVCenter)

        self.hBoxLayout.addStretch(1)
        if saved:
            self.hBoxLayout.addWidget(self.openButton, 0, Qt.AlignRight)
            self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignRight)
            self.hBoxLayout.addWidget(self.transparentDropDownToolButton, 0, Qt.AlignRight)

            self.moreButton.setFixedSize(100, 32)
        else:
            self.hBoxLayout.addWidget(self.openButton, 0, Qt.AlignRight)
            self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignRight)

            self.moreButton.setFixedSize(32, 32)

class DraftScreen(QWidget):
    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setStyleSheet('DraftScreen{background:"#272727"}')

        self.vBoxLayout = QVBoxLayout(self)
        self.title1 = TitleLabel("Saved")
        self.title2 = TitleLabel("Draft")
        self.vBoxLayout.addWidget(self.title1)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        for x in range(2):

            self.vBoxLayout.addWidget(VerticalCard(
                icon=":/qfluentwidgets/images/logo.png",
                title="DEEP CNN Model",
                content="Last Updated 3 days ago.",
                saved = True
            ))

        self.vBoxLayout.addWidget(self.title2)

        for x in range(2):

            self.vBoxLayout.addWidget(VerticalCard(
                icon=":/qfluentwidgets/images/logo.png",
                title="DEEP CNN Model",
                content="Last Updated 3 days ago.",
                saved = False
            ))

        self.scrollArea = QScrollArea()
        self.scrollArea.setStyleSheet('''
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

        self.scrollAreaWidget = QWidget()
        self.scrollAreaWidget.setStyleSheet('QWidget{background:"#272727"}')
        self.scrollAreaWidget.setLayout(self.vBoxLayout)

        self.scrollArea.setWidget(self.scrollAreaWidget)
        self.scrollArea.setWidgetResizable(True)  

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.scrollArea)

if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = DraftScreen()
    w.show()
    app.exec_()