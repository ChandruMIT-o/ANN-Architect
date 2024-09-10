from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCompleter, QGridLayout, QScrollArea, QSizePolicy, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from qfluentwidgets import (MessageBoxBase, SubtitleLabel, LineEdit, PushButton, setThemeColor, setTheme, Theme, CaptionLabel, SearchLineEdit,
                            IconWidget, CardWidget, BodyLabel, ColorPickerButton, SwitchButton, isDarkTheme,
                            DropDownPushButton, TitleLabel, RoundMenu, Action, HyperlinkButton)
from qfluentwidgets import FluentIcon as FIF
import sys

class VerticalSettingCard(CardWidget):

    def __init__(self, icon, title, content, parent=None, option = 1):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.titleLabel.setObjectName("VerticalSettingCardTitle")
        
        #if isDarkTheme: self.titleLabel.setStyleSheet("""#VerticalSettingCardTitle{background: transparent; color: white; font-weight: bold;}""")
        self.contentLabel = CaptionLabel(content, self)
        self.contentLabel.setObjectName("VerticalSettingCardContent")
        #if isDarkTheme: self.contentLabel.setStyleSheet("""#VerticalSettingCardContent{background: transparent; color: white}""")

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(65)
        self.iconWidget.setFixedSize(20, 20)
 
        self.hBoxLayout.setContentsMargins(20, 11, 20, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.hBoxLayout.addStretch(1)
        
        if option == 1:
            self.toggleButton = SwitchButton(self)
            self.hBoxLayout.addWidget(self.toggleButton, 0, alignment=Qt.AlignmentFlag.AlignRight)  
        elif option == 2:
            self.menu = RoundMenu(parent=self)
            self.menu.addAction(Action('Dark'))
            self.menu.addAction(Action('Light'))
            self.menu.addAction(Action('System'))
            self.themeButton = DropDownPushButton("Dark", self, FIF.CONSTRACT)
            self.themeButton.setMenu(self.menu)         
            self.menu.triggered.connect(self.changeThemeButtonText)
            self.hBoxLayout.addWidget(self.themeButton, 0, alignment=Qt.AlignmentFlag.AlignRight)
        elif option == 3:
            self.colorPickerButton = ColorPickerButton(QColor("#5012aaa2"), title = "Color", parent=self)
            self.colorPickerButton.setFixedSize(32, 32)
            self.colorPickerButton.clicked.connect(self.changeThemeColor)
            self.hBoxLayout.addWidget(self.colorPickerButton, 0, alignment=Qt.AlignmentFlag.AlignRight)
        elif option == 4:
            self.linkButton = HyperlinkButton(
                url='https://contacts.google.com/person/c9172142090268153275',
                text='Documentation',
                parent=self,
                icon=FIF.LINK
            )
            self.hBoxLayout.addWidget(self.linkButton, 0, alignment=Qt.AlignmentFlag.AlignRight)
        elif option == 5:
            self.linkButton = HyperlinkButton(
                url='https://contacts.google.com/person/c9172142090268153275',
                text='Buy us a Coffee',
                parent=self,
                icon=FIF.CAFE
            )
            self.hBoxLayout.addWidget(self.linkButton, 0, alignment=Qt.AlignmentFlag.AlignRight)

    def changeThemeColor(self):
        setThemeColor(self.colorPickerButton.color)

    def changeThemeButtonText(self, action):
        self.themeButton.setText(action.text())
        if action.text() == "Dark" or action.text() == "System":
            setTheme(Theme.DARK)
        elif action.text() == "Light":
            setTheme(Theme.LIGHT)

    def toggleMicaEffect(self):
        print("Does nothing!")

class SettingsScreen(QWidget):
    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setObjectName("SettingsScreen")
        # if isDarkTheme: self.setStyleSheet('#SettingsScreen{background:"#272727"}')

        self.vBoxLayout = QVBoxLayout(self)
        self.title1 = TitleLabel("Settings")
        self.title3 = SubtitleLabel("Personalisation")
        self.title2 = SubtitleLabel("About")
        self.vBoxLayout.addWidget(self.title1)
        self.vBoxLayout.addWidget(self.title3)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        self.vBoxLayout.addWidget(VerticalSettingCard(
            icon=FIF.TRANSPARENT,
            title="Mica effect",
            content="Apply semi transparent to windows and surfaces",
            option = 1
        ))

        self.vBoxLayout.addWidget(VerticalSettingCard(
            icon=FIF.BRUSH,
            title="Application Theme",
            content="Change the appearance of your application",
            option = 2
        ))

        self.vBoxLayout.addWidget(VerticalSettingCard(
            icon=FIF.PALETTE,
            title="Theme Color",
            content="Change the theme color of your application",
            option = 3
        ))

        self.vBoxLayout.addWidget(self.title2)

        self.vBoxLayout.addWidget(VerticalSettingCard(
            icon=FIF.HELP,
            title="Help Center",
            content="Check out our documentation",
            option = 4
        ))

        self.vBoxLayout.addWidget(VerticalSettingCard(
            icon=FIF.PEOPLE,
            title="Find Us",
            content="Get to know about the developers behind this project",
            option = 5
        ))

        self.scrollArea = QScrollArea()
        """self.scrollArea.setStyleSheet('''
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
                                        ''')"""

        self.scrollAreaWidget = QWidget()
        self.scrollAreaWidget.setObjectName('scrollAreaWidget')
        # if isDarkTheme: self.scrollAreaWidget.setStyleSheet('#scrollAreaWidget{background:"#272727"}')
        # else: self.scrollAreaWidget.setStyleSheet('#scrollAreaWidget{background: white}')
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
    w = SettingsScreen()
    w.show()
    app.exec_()