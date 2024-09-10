from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCompleter, QGridLayout, QScrollArea, QSizePolicy, QAction, QStackedWidget,
                             QSpacerItem)
from PyQt5.QtCore import Qt
from qfluentwidgets import (setTheme, Theme, CaptionLabel, SearchLineEdit,
                            ToolButton, CardWidget, SpinBox, DoubleSpinBox,
                            SegmentedWidget, SwitchButton, TransparentToolButton,
                            EditableComboBox)
from qfluentwidgets import FluentIcon as FIF

from content.dictionary_representation import CONSTANTS as CONT
import sys

class ParametersSelectionMenuItem(CardWidget):
    def __init__(self, propertyName, parent=None):
        super().__init__(parent)

        self.hBoxLayout = QHBoxLayout(self)

        self.titleLabel = CaptionLabel(propertyName, self)
        self.titleLabel.setObjectName("ParametersSelectionMenuItemTitle")
        self.titleLabel.setStyleSheet("""#ParametersSelectionMenuItemTitle{
                font: 400 16px 'Segoe UI';
                background: transparent;
                border-radius: 8px;
                color: white;
                }
                """)

        self.addParameterButton = ToolButton(FIF.ADD, self)
        self.aboutParameterButton = ToolButton(FIF.INFO, self)

        # Add the title label to the left
        self.hBoxLayout.addWidget(self.titleLabel)

        # Add a spacer to push the buttons to the right
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hBoxLayout.addItem(spacer)

        # Add the buttons to the right
        self.hBoxLayout.addWidget(self.aboutParameterButton)
        self.hBoxLayout.addWidget(self.addParameterButton)

        self.setFixedHeight(50)
        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)

class ParametersSelectionWidget(CardWidget):
    def __init__(self, propertyName, parent=None):
        super().__init__(parent)

        self.vBoxLayout = QVBoxLayout(self)

        self.collapsableMenuLayout = QHBoxLayout()

        self.titleLabel = CaptionLabel(propertyName, self)
        self.titleLabel.setObjectName("ParametersSelectionWidgetTitle")
        self.titleLabel.setStyleSheet("""#ParametersSelectionWidgetTitle{
                font: 900 14px 'Segoe UI';
                background: transparent;
                border-radius: 8px;
                color: white;
                padding: 2px;
                }
                """)

        self.collapseButton = TransparentToolButton(FIF.ARROW_DOWN)
        self.collapseButton.clicked.connect(self.collapse)
        self.collapsableMenuLayout.addWidget(self.titleLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        self.collapsableMenuLayout.addWidget(self.collapseButton, alignment=Qt.AlignmentFlag.AlignRight)

        self.vBoxLayout.addLayout(self.collapsableMenuLayout)

        # Create a QWidget to hold the vSubSection layout
        self.subSectionWidget = QWidget()
        self.vSubSection = QVBoxLayout(self.subSectionWidget)
        self.vSubSection.setContentsMargins(0, 0, 0, 0)

        self.parameters = dict()
        parametersNames = [
            "Conv2D", "DepthwiseConv2D", "SeparableConv2D", "MaxPooling2D", "AveragePooling2D",
            "GlobalMaxPooling2D", "GlobalAveragePooling2D", "Dropout", "Flatten", "BatchNormalization",
            "ReLU", "LeakyReLU", "ELU", "PReLU", "Softmax", "Dense", "Activation", "InputLayer",
            "Add", "Multiply", "Subtract", "Divide", "Concatenate", "Lambda", "ZeroPadding2D", "Cropping2D"
        ]

        for parameterName in parametersNames:
            self.parameters[parameterName] = ParametersSelectionMenuItem(parameterName)
            self.parameters[parameterName].setStyleSheet("ParametersSelectionMenuItem{background: transparent}")
            self.vSubSection.addWidget(self.parameters[parameterName])

        # Create a QScrollArea to make the vSubSection scrollable
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setContentsMargins(0, 0, 0, 0)
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
        background: transparent;
    }        
                                        ''')
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.subSectionWidget)
        self.scrollArea.setFixedHeight(300)  # Set the desired maximum height before scrolling

        # Add the scroll area to the main layout
        self.vBoxLayout.addWidget(self.scrollArea)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # self.vBoxLayout.setContentsMargins(11, 11, 11, 11)

        self.collapsed = False  # Initial state of the collapse

    def collapse(self):

        if self.collapsed:
            # Expand
            self.collapseButton.setIcon(FIF.ARROW_DOWN)
            self.scrollArea.show()  # Show scrollable area
            self.setFixedHeight(self.sizeHint().height())  # Reset to fit content
            self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        else:
            # Collapse
            self.collapseButton.setIcon(FIF.UP)
            self.scrollArea.hide()  # Hide scrollable area
            self.setFixedHeight(50)  # Fixed height when collapsed
            self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.collapsed = not self.collapsed  # Toggle state

class PropertyBooleanMenuItem(CardWidget):

    def __init__(self, propertyName, parent=None):
        super().__init__(parent)

        self.hBoxLayout = QHBoxLayout(self)

        self.titleLabel = CaptionLabel(propertyName, self)
        self.titleLabel.setObjectName("titleLabelPBMI")
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.titleLabel.setStyleSheet("""#titleLabelPBMI{
                font: 400 16px 'Segoe UI';
                background: transparent;
                border-radius: 8px;
                color: white;
                }
                """)
        
        self.toggleButton = SwitchButton("False", self)

        self.toggleButton.checkedChanged.connect(self.onCheckedChanged)

        self.hBoxLayout.addWidget(self.titleLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addWidget(self.toggleButton, alignment=Qt.AlignmentFlag.AlignRight)

        self.setFixedHeight(50)
        self.hBoxLayout.setContentsMargins(20, 11, 20, 11)
    
    def onCheckedChanged(self, isChecked: bool):
        text = 'True' if isChecked else 'False'
        self.toggleButton.setText(text)

class PropertyDropDownMenuItem(CardWidget):

    def __init__(self, propertyName, items, parent=None):
        super().__init__(parent)

        self.hBoxLayout = QHBoxLayout(self)

        self.titleLabel = CaptionLabel(propertyName, self)
        self.titleLabel.setObjectName("titleLabelDDMI")

        self.titleLabel.setStyleSheet("""#titleLabelDDMI{
                font: 400 16px 'Segoe UI';
                background: transparent;
                border-radius: 8px;
                color: white;
                }         
        """)
        
        self.comboBox = EditableComboBox(self)
        
        self.comboBox.addItems(items)
        self.comboBox.setPlaceholderText(items[0])
        self.comboBox.setCurrentIndex(-1)

        self.completer = QCompleter(items, self)
        self.comboBox.setCompleter(self.completer)

        self.hBoxLayout.addWidget(self.titleLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addWidget(self.comboBox, alignment=Qt.AlignmentFlag.AlignRight)

        self.setFixedHeight(50)
        self.hBoxLayout.setContentsMargins(20, 0, 8, 0)

class PropertyIntInputMenuItem(CardWidget):

    def __init__(self, propertyName, type = "double", parent=None):
        super().__init__(parent)

        self.hBoxLayout = QHBoxLayout(self)

        self.titleLabel = CaptionLabel(propertyName, self)
        self.titleLabel.setObjectName("titleLabelPIIMI")
        self.titleLabel.setStyleSheet("""#titleLabelPIIMI{
                font: 400 16px 'Segoe UI';
                background: transparent;
                border-radius: 8px;
                color: white;
                }         
        """)

        if type == "int":
            self.intInput = SpinBox(self)
        elif type == "double":
            self.intInput = DoubleSpinBox(self)

        self.intInput.setMinimum(0)
        self.intInput.setMaximum(100000)

        self.hBoxLayout.addWidget(self.titleLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addWidget(self.intInput, alignment=Qt.AlignmentFlag.AlignRight)

        self.setFixedHeight(50)
        self.hBoxLayout.setContentsMargins(20, 0, 8, 0)

class PropertySubSectionMenuItem(CardWidget):

    def __init__(self, propertyName, type = "double", parent=None):
        super().__init__(parent)

        self.hBoxLayout = QVBoxLayout(self)

        self.titleLabel = CaptionLabel(propertyName, self)
        self.titleLabel.setObjectName("titleLabelPSSMI")
        self.titleLabel.setStyleSheet("""#titleLabelPSSMI{
                font: 400 16px 'Segoe UI';
                background: transparent;
                border-radius: 8px;
                color: white;
                }         
        """)

        if type == "int":
            self.intInput = SpinBox(self)
        elif type == "double":
            self.intInput = DoubleSpinBox(self)

        self.intInput.setMinimum(0)
        self.intInput.setMaximum(100000)

        self.vBoxLayout = QHBoxLayout(self)
        self.vBoxLayout.setContentsMargins(12, 0, 0, 0)

        self.vBoxLayout.addWidget(self.titleLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        self.vBoxLayout.addWidget(self.intInput, alignment=Qt.AlignmentFlag.AlignRight)

        self.vSubSection = QVBoxLayout()

        self.SubParameter1 = PropertyDropDownMenuItem("SubParameter")
        self.SubParameter1.setStyleSheet("PropertyDropDownMenuItem{background: transparent}")
        self.vSubSection.addWidget(self.SubParameter1)

        # self.setFixedHeight(100)
        self.hBoxLayout.setContentsMargins(8, 8, 8, 8)

        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.hBoxLayout.addLayout(self.vSubSection)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

class RightSection(QWidget):

    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setStyleSheet("""
            RightSection{background: "#272727"}
            QLabel{
                font: 20px 'Segoe UI';
                background: rgb(242,242,242);
                border-radius: 8px;
            }
        """)
        self.resize(400, 400)

        self.pivot = SegmentedWidget(self)
        # self.pivot.setMaximumWidth(500)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.songLayout = QVBoxLayout()
        self.albumLayout = QVBoxLayout()
        self.artistLayout = QVBoxLayout()

        self.songLayout.setAlignment(Qt.AlignTop)
        self.albumLayout.setAlignment(Qt.AlignTop)
        self.artistLayout.setAlignment(Qt.AlignTop)

        # Add content to layouts (can be widgets, labels, etc.)
        self.songLayout.addWidget(QWidget(self))  # Example widget inside the layout
        self.albumLayout.addWidget(QWidget(self))
        self.artistLayout.addWidget(QWidget(self))

        # Add layouts wrapped in widgets to the interface
        self.addSubInterface(self.songLayout, 'songInterface', 'Layers')
        self.addSubInterface(self.albumLayout, 'albumInterface', 'Parameters')
        self.addSubInterface(self.artistLayout, 'artistInterface', 'Document')

        self.vBoxLayout.addWidget(self.pivot)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setAlignment(Qt.AlignRight)
        self.vBoxLayout.setContentsMargins(10, 10, 10, 10)

        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))
        self.pivot.setCurrentItem('songInterface')
        self.pivot.currentItemChanged.connect(
            lambda k: self.stackedWidget.setCurrentWidget(self.findChild(QWidget, k))
        )

        self.setLayout(self.vBoxLayout)

    def addSubInterface(self, layout: QVBoxLayout, objectName, text):

        self.rightVLayout = layout

        if text == 'Layers':
            layout.addWidget(ParametersSelectionWidget("Convolution"))
        
        elif text == 'Parameters':
            self.init_parameters(layer_name="DENSE_LAYER")
        elif text == 'Document':

            pass

        widget = QWidget(self)  # Wrap layout inside a QWidget
        widget.setLayout(layout)
        widget.setObjectName(objectName)
        widget.setStyleSheet("#"+str(objectName)+'{background: "#232323"}')

        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(routeKey=objectName, text=text)

    def init_parameters(self, layer_name):

        self.titleLabel = CaptionLabel(layer_name, self)
        self.titleLabel.setObjectName("ParametersTitleLabel")
        self.titleLabel.setStyleSheet("""#ParametersTitleLabel{
            font: 900 14px 'Segoe UI';
            background: transparent;
            border-radius: 8px;
            color: white;
            padding: 2px;
            }
            """)
        self.rightVLayout.addWidget(self.titleLabel)

        if layer_name in CONT().LAYER_INFO:

            DICT = CONT().LAYER_INFO[layer_name]
            BASIC_DICT = DICT['basic']
            ADVANCED_DICT = DICT['advanced']

        self.basicLabel = CaptionLabel("Basic Paramaters")
        self.basicLabel.setObjectName("basicParametersLabel")
        self.basicLabel.setStyleSheet("""#basicParametersLabel{
            font: 400 14px 'Segoe UI';
            background: transparent;
            border-radius: 8px;
            color: white;
            padding: 2px;
            }
            """)
        self.rightVLayout.addWidget(self.basicLabel)

        for PARAM in BASIC_DICT.keys():
            type = BASIC_DICT[PARAM]['type']
            structure = BASIC_DICT[PARAM]['structure']
            options = BASIC_DICT[PARAM]['options']

            if structure == 'linear':
                if type == 'dropdown':
                    self.rightVLayout.addWidget(PropertyDropDownMenuItem(PARAM, options))



        self.advancedLabel = CaptionLabel("Advanced Paramaters")
        self.advancedLabel.setObjectName("advancedParametersLabel")
        self.advancedLabel.setStyleSheet("""#advancedParametersLabel{
            font: 400 14px 'Segoe UI';
            background: transparent;
            border-radius: 8px;
            color: white;
            padding: 2px;
            }
            """)
        self.rightVLayout.addWidget(self.advancedLabel)

        # self.rightVLayout.addWidget(PropertyBooleanMenuItem("verbose"))
        # self.rightVLayout.addWidget(PropertyIntInputMenuItem("volume"))
        # self.rightVLayout.addWidget(PropertySubSectionMenuItem("subvolume"))


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = RightSection()
    w.show()
    app.exec_()
