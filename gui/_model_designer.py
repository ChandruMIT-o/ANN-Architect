from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QHBoxLayout, QSizePolicy, QSpacerItem)
from PyQt5.QtCore import Qt
from qfluentwidgets import (setTheme, Theme, CaptionLabel, Action, RoundMenu,
                            ToolButton, CardWidget, PillToolButton, PushButton, PrimaryPushButton, TransparentToolButton)
from qfluentwidgets import FluentIcon as FIF
import sys

class LayerBar(CardWidget):
    def __init__(self, propertyName, parameters, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.hBoxLayout = QHBoxLayout(self)
        self.parameters = parameters

        self.paramterButtons = []

        self.statusButton = TransparentToolButton(FIF.ACCEPT, self)
        self.statusButton.setDisabled(True)

        self.layerName = CaptionLabel(propertyName, self)
        self.layerName.setObjectName("layerNameLayerBar")
        self.layerName.setStyleSheet("""#layerNameLayerBar{
                font: 400 16px 'Segoe UI';
                background: transparent;
                border-radius: 8px;
                color: white;
                }
                """)
        
        self.morePropertiesButton = PushButton("View Params", self, FIF.VIEW)

        # Overriding the mouse press event of the button
        self.morePropertiesButton.mousePressEvent = self.onMorePropertiesButtonClick

        self.duplicateButton = ToolButton(FIF.DICTIONARY_ADD, self)
        self.moveUpButton = ToolButton(FIF.UP, self)
        self.moveDownButton = ToolButton(FIF.DOWN, self)
        self.editButton = PillToolButton(FIF.EDIT, self)

        self.hBoxLayout.addWidget(self.statusButton)
        self.hBoxLayout.addWidget(self.layerName)

        for param in self.parameters:
            self.paramterButtons.append(PrimaryPushButton(param))
            self.paramterButtons[-1].setDisabled(True)
            self.hBoxLayout.addWidget(self.paramterButtons[-1])

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hBoxLayout.addItem(spacer)
        self.hBoxLayout.addWidget(self.morePropertiesButton)
        self.hBoxLayout.addWidget(self.duplicateButton)
        self.hBoxLayout.addWidget(self.moveDownButton)
        self.hBoxLayout.addWidget(self.moveUpButton)
        self.hBoxLayout.addWidget(self.editButton)

        self.setFixedHeight(55)
        self.hBoxLayout.setContentsMargins(11, 11, 11, 11)

        # Connect move buttons to actions
        self.moveUpButton.clicked.connect(self.move_up)
        self.moveDownButton.clicked.connect(self.move_down)
        self.duplicateButton.clicked.connect(self.duplicate_layer)

    def move_up(self):
        index = self.parent.vBoxLayout.indexOf(self)
        if index > 0:
            self.parent.vBoxLayout.removeWidget(self)
            self.parent.vBoxLayout.insertWidget(index - 1, self)

    def move_down(self):
        index = self.parent.vBoxLayout.indexOf(self)
        if index < self.parent.vBoxLayout.count() - 1:
            self.parent.vBoxLayout.removeWidget(self)
            self.parent.vBoxLayout.insertWidget(index + 1, self)

    def duplicate_layer(self):
        duplicated_layer = LayerBar(self.layerName.text(), self.parameters, self.parent)
        index = self.parent.vBoxLayout.indexOf(self)
        self.parent.vBoxLayout.insertWidget(index + 1, duplicated_layer)

    def onMorePropertiesButtonClick(self, event):
        pos = self.morePropertiesButton.mapToGlobal(event.pos())
        self.showProperties(event)

    def showProperties(self, e):
        menu = RoundMenu(parent=self)

        menu.addActions([
            Action('Regulariser: 50'),
            Action('Bias Initializer: 45'),
            Action('Kernel constraint: Stop'),
        ])
        menu.addSeparator()
        menu.addAction(Action(FIF.SETTING, 'Sample'))
        menu.exec(e.globalPos())

class ModelDesigner(QWidget):
    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setStyleSheet('ModelDesigner{background:"#272727"}')

        self.vBoxLayout = QVBoxLayout(self)

        parameters1 = ['Shape : (3,4,5)', 'Activation: "RELU"', 'Regulariser: "L1"']

        self.layer1 = LayerBar("Dense", parameters1, self)
        self.layer2 = LayerBar("RNN", parameters1, self)
        self.layer3 = LayerBar("ANN", parameters1, self)

        self.vBoxLayout.addWidget(self.layer1)
        self.vBoxLayout.addWidget(self.layer2)
        self.vBoxLayout.addWidget(self.layer3)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = ModelDesigner()
    w.show()
    app.exec_()
