from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCompleter, QGridLayout, QScrollArea, QSizePolicy, QAction
from PyQt5.QtCore import Qt
from qfluentwidgets import (MessageBoxBase, SubtitleLabel, LineEdit, PushButton, setTheme, Theme, CaptionLabel, SearchLineEdit,
                            IconWidget, CardWidget, BodyLabel, PillPushButton, FluentIcon, InfoBadge, InfoLevel, ToolButton, TransparentToolButton,
                            TransparentDropDownToolButton, RoundMenu, PrimaryToolButton, TitleLabel, Dialog)
from qfluentwidgets import FluentIcon as FIF
import sys

class VerticalDraftCard(CardWidget):

    def __init__(self, icon, title, content, archi_type, total_parameters, is_published, parent=None, saved = False):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.titleLabel.setObjectName("VerticalDraftCardTitle")
        self.titleLabel.setStyleSheet("""#VerticalDraftCardTitle{background: transparent; color: white}""")
        self.contentLabel = CaptionLabel(content, self)
        self.contentLabel.setObjectName("VerticalDraftCardContent")
        self.contentLabel.setStyleSheet("""#VerticalDraftCardContent{background: transparent; color: white}""")
        self.openButton = PushButton('Edit', self)

        self.architypeInfoBadge = InfoBadge.info(f"Architype: {archi_type}")
        self.architypeInfoBadge.setFixedHeight(22)
        self.totalParametersInfoBadge = InfoBadge.attension(f"Total Parameters: {total_parameters}")
        self.totalParametersInfoBadge.setFixedHeight(22)

        if saved:
            self.publishButton = PillPushButton(FluentIcon.PEOPLE, 'Publish')
            self.publishButton.setChecked(is_published)
            self.publishButton.clicked.connect(self.publishProject)
        else:
            self.saveButton = ToolButton(FluentIcon.SAVE)
            self.saveButton.clicked.connect(self.saveProject)

        self.menu = RoundMenu(parent=self)

        duplicate_action = QAction(FIF.DICTIONARY_ADD.icon(), 'Duplicate')
        delete_action = QAction(FIF.DELETE.icon(), 'Delete')

        self.menu.addAction(duplicate_action)
        self.menu.addAction(delete_action)

        duplicate_action.triggered.connect(self.duplicateProject)
        delete_action.triggered.connect(self.deleteProject)

        self.transparentDropDownToolButton = TransparentDropDownToolButton(FIF.MORE, self)
        self.transparentDropDownToolButton.setMenu(self.menu)


        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(65)
        self.iconWidget.setFixedSize(32, 32)
        # self.contentLabel.setTextColor("#606060", "#d2d2d2")
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
            self.hBoxLayout.addWidget(self.publishButton, 0, Qt.AlignRight)
            self.hBoxLayout.addWidget(self.transparentDropDownToolButton, 0, Qt.AlignRight)

            self.publishButton.setFixedSize(100, 32)
        else:
            self.hBoxLayout.addWidget(self.openButton, 0, Qt.AlignRight)
            self.hBoxLayout.addWidget(self.saveButton, 0, Qt.AlignRight)
            self.hBoxLayout.addWidget(self.transparentDropDownToolButton, 0, Qt.AlignRight)

            self.saveButton.setFixedSize(32, 32)

    def publishProject(self):

        state = self.publishButton.isChecked()

        if state:
            title = 'Are you sure you want to publish?'
            content = """Other users can access or potentially clone your project!"""
            
        else:
            title = 'Are you sure you want to unpublish?'
            content = """Your project will no longer be accessible to other users. But cloned projects won't be blocked"""

        w = Dialog(title, content, self)
        w.setTitleBarVisible(False)

        if state:
            w.yesButton.setText("Publish")
            w.yesButton.setIcon(FIF.GLOBE)
        else:
            w.yesButton.setText("Unpublish")
            w.yesButton.setIcon(FIF.REMOVE_FROM)
        
        if w.exec():
            # TODO: Set project to global using project name and user name and commit
            # ! That depends on the toggle state of the publishButton   
            print("Project is published!")
            projectName = self.titleLabel.text()
            
            pass

    def saveProject(self):
        title = 'Are you sure you want to save?'
        content = """Your project will be saved locally and accessible later. You can also publish it."""
        w = Dialog(title, content, self)
        w.setTitleBarVisible(False)
        w.yesButton.setText("Save")
        w.yesButton.setIcon(FIF.SAVE)
        if w.exec():
            # TODO: Save project to database using project name and user name and commit
            print("Project is saved!")
            projectName = self.titleLabel.text()
            pass
    
    def deleteProject(self):
        title = 'Are you sure you want to delete?'
        content = """This action cannot be undone. Your project will be removed from your saved projects list."""
        w = Dialog(title, content, self)
        w.setTitleBarVisible(False)
        w.yesButton.setText("Delete")
        w.yesButton.setIcon(FIF.DELETE)
        if w.exec():
            # TODO: Delete project from database using project name and user name and commit
            print("Project is deleted!")
            projectName = self.titleLabel.text()
            pass

    def duplicateProject(self):
        title = 'Are you sure you want to duplicate?'
        content = """This will create a new project with the same name and parameters."""
        w = Dialog(title, content, self)
        w.setTitleBarVisible(False)
        w.yesButton.setText("Duplicate")
        w.yesButton.setIcon(FIF.DICTIONARY_ADD)
        if w.exec():
            # TODO: Duplicate project using project name and user name and commit
            print("Project is duplicated!")
            projectName = self.titleLabel.text()
            pass

class DraftScreen(QWidget):
    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setStyleSheet('DraftScreen{background:"#272727"}')

        self.vBoxLayout = QVBoxLayout(self)

        self.title0 = TitleLabel("My Projects")
        self.title1 = SubtitleLabel("Saved")
        self.title2 = SubtitleLabel("Draft")

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
        self.scrollAreaWidget.setObjectName("scrollAreaWidgetDrafts")
        self.scrollAreaWidget.setStyleSheet('#scrollAreaWidgetDrafts{background:"#272727"}')
        self.scrollAreaWidget.setLayout(self.vBoxLayout)

        self.scrollArea.setWidget(self.scrollAreaWidget)
        self.scrollArea.setWidgetResizable(True)  

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.scrollArea)

        self.init_components()

    def init_components(self):
        while self.vBoxLayout.count() > 0:
            item = self.vBoxLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.vBoxLayout.addWidget(self.title0)
        self.vBoxLayout.addWidget(self.title1)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        # TODO: Fetch all the local project meta that are saved

        titles = [
            "ResNet50 Model",
            "MobileNetV2 Model",
            "VGG16 Model",
            "EfficientNetB0 Model",
            "DenseNet121 Model"
        ]

        lastUpdated = [
            "2024-08-01",
            "2024-07-15",
            "2024-09-05",
            "2024-09-01",
            "2024-08-25"
        ]

        archi_types = [
            "CNN",
            "Mobile Architecture",
            "Deep CNN",
            "Efficient Architecture",
            "Dense CNN"
        ]

        total_parameters = [
            "25.6M",
            "3.5M",
            "138M",
            "5.3M",
            "7.9M"
        ]

        is_published = [
            True,
            False,
            True,
            False,
            True
        ]

        is_savedall = [
            True,
            True,
            True,
            True,
            True
        ]

        for x in range(len(titles)):

            self.vBoxLayout.addWidget(VerticalDraftCard(
                icon="gui\images\logo.png",
                title=titles[x],
                content=f"last updated on {lastUpdated[x]}",
                archi_type=archi_types[x],
                total_parameters=total_parameters[x],
                is_published=is_published[x],
                saved=is_savedall[x]
            ))

        self.vBoxLayout.addWidget(self.title2)

        # TODO: Fetch all the local project meta that are drafts

        titles = [
            "InceptionV3 Model",
            "AlexNet Model",
            "Xception Model",
            "NASNetMobile Model",
            "SqueezeNet Model"
        ]

        lastUpdated = [
            "2024-07-30",
            "2024-06-20",
            "2024-08-18",
            "2024-09-03",
            "2024-07-10"
        ]

        archi_types = [
            "Inception Architecture",
            "Classic CNN",
            "Extreme Inception",
            "Neural Architecture Search",
            "Lightweight CNN"
        ]

        total_parameters = [
            "23.8M",
            "61M",
            "22.9M",
            "5.3M",
            "1.2M"
        ]

        is_published = [
            True,
            False,
            False,
            True,
            True
        ]

        is_savedall = [
            False,
            False,
            False,
            False,
            False
        ]

        for x in range(len(titles)):

            self.vBoxLayout.addWidget(VerticalDraftCard(
                icon="gui\images\logo.png",
                title=titles[x],
                content=f"last updated on {lastUpdated[x]}",
                archi_type=archi_types[x],
                total_parameters=total_parameters[x],
                is_published=is_published[x],
                saved=is_savedall[x]
            ))

if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = DraftScreen()
    w.show()
    app.exec_()