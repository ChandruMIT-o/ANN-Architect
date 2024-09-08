import sys
from PyQt5.QtCore import Qt, QRect, QUrl
from PyQt5.QtGui import QIcon, QPainter, QImage, QBrush, QColor, QFont, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QStackedWidget, QHBoxLayout, QLabel, QWidget

from qfluentwidgets import (NavigationInterface, NavigationItemPosition, NavigationWidget, MessageBox,
                            isDarkTheme, setTheme, Theme, setThemeColor, qrouter, FluentWindow, NavigationAvatarWidget)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, StandardTitleBar

from gui.home import HomeScreen
from gui.drafts import DraftScreen
from gui.projects import ProjectsScreen
from gui.settings import SettingsScreen

class Widget(QFrame):
    def __init__(self, arg=None, parent=None):
        super().__init__(parent=parent)

        if isinstance(arg, str):
            # If the argument is a string, treat it as the text for the label
            self.label = QLabel(arg, self)
            self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.hBoxLayout = QHBoxLayout(self)
            self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
            self.setObjectName(arg.replace(' ', '-'))

        elif isinstance(arg, QWidget):
            # If the argument is a QWidget, treat it as a widget to add to the layout
            self.hBoxLayout = QHBoxLayout(self)
            self.hBoxLayout.addWidget(arg)

        else:
            # Handle the case where arg is neither a str nor a QWidget
            raise TypeError("Argument must be a string or a QWidget")

class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))

        setTheme(Theme.DARK)

        # change the theme color
        # setThemeColor('#0078d4')

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, showMenuButton=True)
        self.stackWidget = QStackedWidget(self)

        self.homewidget = HomeScreen()
        self.draftScreen = DraftScreen()
        self.projectsScreen = ProjectsScreen()
        self.settingsScreen = SettingsScreen()

        # create sub interface
        self.homeInterface = Widget(self.homewidget)
        self.projectInterface = Widget(self.projectsScreen)
        self.draftsInterface = Widget(self.draftScreen)
        # self.draftsInterface = Widget("Drafts", self)
        self.settingInterface = Widget(self.settingsScreen)
        # self.settingInterface = Widget("settings", self)

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        # enable acrylic effect
        # self.navigationInterface.setAcrylicEnabled(True)

        self.addSubInterface(self.homeInterface, FIF.HOME, 'Home')
        self.addSubInterface(self.projectInterface, FIF.IOT, 'Project')
        self.addSubInterface(self.draftsInterface, FIF.DOCUMENT, 'Drafts')

        self.navigationInterface.addSeparator()

        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('Rameez', 'gui\\images\\logo.png'),
            onClick=self.showMessageBox,
            position=NavigationItemPosition.BOTTOM,
        )

        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

        # set the maximum width
        self.navigationInterface.setExpandWidth(200)

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.stackWidget.setCurrentIndex(1)

        # always expand
        # self.navigationInterface.setCollapsible(False)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('gui\\images\\logo.png'))

        self.setWindowTitle('ΛNN Architect')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        self.setQss()

    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP, parent=None):
        # Generate and assign a unique objectName based on the text if it's not already set
        # unique_name = text.replace(' ', '-').lower()
        interface.setObjectName(text)

        # Add widget to stack and navigation interface
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),  # Use the object name as the route key
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text,
            parentRouteKey=parent.objectName() if parent else None
        )


    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'gui/styles/{color}/main.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())

    def showMessageBox(self):
        w = MessageBox(
            'All Hail Rameez!',
            'Mirsha bald',
            self
        )
        w.yesButton.setText('Okay')
        w.cancelButton.setText('Cancel')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://contacts.google.com/person/c9172142090268153275"))


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()