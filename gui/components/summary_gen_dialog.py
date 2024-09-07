import sys, csv
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QTableWidgetItem
from qfluentwidgets import (MessageBoxBase, SubtitleLabel, PushButton, setTheme, Theme, TableWidget,
                            TransparentPushButton, setCustomStyleSheet)
from qfluentwidgets import FluentIcon as FIF

class GeneratedSummaryMessageBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('ModelSummary', self)
        
        self.viewLayout.addWidget(self.titleLabel)

        self.yesButton.setText('Export as CSV')
        self.yesButton.clicked.connect(self.export_to_csv)
        self.cancelButton.setText('Close')

        self.tableView = TableWidget(self)

        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)

        self.tableView.setWordWrap(True)

        self.columns = ['Layer (type)', 'Output Shape', 'Param #']
        
        self.data = [
            ['conv2d (Conv2D)', '(None, 26, 26, 32)', '320'],
            ['batch_normalization', '(None, 26, 26, 32)', '96'],
            ['conv2d_1 (Conv2D)', '(None, 26, 26, 64)', '36864'],
            ['batch_normalization_1', '(None, 26, 26, 64)', '256']
        ]
        self.tableView.setRowCount(len(self.data))
        self.tableView.setColumnCount(len(self.data[0]))

        self.data += self.data
        for i, songInfo in enumerate(self.data):
            for j in range(3):
                self.tableView.setItem(i, j, QTableWidgetItem(songInfo[j]))

        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(self.columns)
        self.tableView.resizeColumnsToContents()
        self.viewLayout.addWidget(self.tableView)

        self.textButton1 = TransparentPushButton("Total params: 225,034 (879.04 KB)")
        self.textButton2 = TransparentPushButton("Trainable params: 225,034 (879.04 KB)")
        self.textButton3 = TransparentPushButton("Non-trainable params: 0 (0.00 B)")

        self.viewLayout.addWidget(self.textButton1)
        self.viewLayout.addWidget(self.textButton2)
        self.viewLayout.addWidget(self.textButton3)

        self.widget.setMinimumWidth(550)
        self.widget.setMaximumWidth(900)

    def export_to_csv(self):
        filename = 'ModelSummary.csv'

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            writer.writerow(self.columns)
            
            writer.writerows(self.data)

# class Demo(QWidget):
#     def __init__(self):
#         super().__init__()
#         setTheme(Theme.DARK)
#         self.setStyleSheet('Demo{background:rgb(32,32,32)}')

#         self.hBxoLayout = QHBoxLayout(self)
#         self.button = PushButton('Summary', self)

#         self.resize(600, 600)
#         self.hBxoLayout.addWidget(self.button, 0, Qt.AlignCenter)
#         self.button.clicked.connect(self.showDialog)

#     def showDialog(self):
#         w = GeneratedSummaryMessageBox(self)
#         if w.exec():
#             pass

# if __name__ == '__main__':
#     # enable dpi scale
#     QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
#     QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
#     QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

#     app = QApplication(sys.argv)
#     w = Demo()
#     w.show()
#     app.exec_()
