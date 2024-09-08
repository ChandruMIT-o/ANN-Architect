import sys
import keyword
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout
from qfluentwidgets import MessageBoxBase, SubtitleLabel, PushButton, setTheme, Theme, TextEdit
from qfluentwidgets import FluentIcon as FIF

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        # Define text formats
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(149, 121, 192))  # Purple
        keyword_format.setFontWeight(QFont.Bold)
        keyword_format.setFontFamily('Consolas')

        string_format = QTextCharFormat()
        string_format.setForeground(QColor(206, 145, 91))  # Orange
        string_format.setFontWeight(QFont.Bold)
        string_format.setFontFamily('Consolas')

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(106, 138, 54))  # Green
        comment_format.setFontItalic(True)
        comment_format.setFontWeight(QFont.Bold)
        comment_format.setFontFamily('Consolas')

        function_format = QTextCharFormat()
        function_format.setForeground(QColor(100, 149, 237))  # Cornflower Blue
        function_format.setFontWeight(QFont.Bold)
        function_format.setFontFamily('Consolas')

        self.highlighting_rules = []

        # Add keyword patterns
        keywords = list(keyword.kwlist)
        keyword_patterns = [f'\\b{kw}\\b' for kw in keywords]
        for pattern in keyword_patterns:
            self.highlighting_rules.append((QRegExp(pattern), keyword_format))

        # Add string pattern
        self.highlighting_rules.append((QRegExp('".*"'), string_format))
        self.highlighting_rules.append((QRegExp("'.*'"), string_format))

        # Add comment pattern
        self.highlighting_rules.append((QRegExp('#[^\n]*'), comment_format))

        # Add function call pattern (assuming functions end with a parenthesis)
        self.highlighting_rules.append((QRegExp(r'\b\w+(?=\()'), function_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

class GeneratedCodeMessageBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('TensorFlow Code', self)
        self.codeArea = TextEdit(self)
        self.codeArea.setFontFamily('Consolas')

        # Example code
        example_code = """from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input

# Define a Sequential model with an Input layer
model = Sequential([
    Input(shape=(28,28,)),  # Input layer 28X28 image
    Dense(64, activation='relu'),  # Hidden layer
    Dense(1, activation='sigmoid')  # Output layer
])
"""

        self.codeArea.setText(example_code)

        # Apply syntax highlighting
        self.highlighter = PythonHighlighter(self.codeArea.document())

        # Add widgets to layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.codeArea)

        self.yesButton.setText('Copy')
        self.cancelButton.setText('Close')

        self.yesButton.clicked.connect(self.copyCode)

        self.widget.setMinimumWidth(550)
        self.widget.setMaximumWidth(900)

    def copyCode(self):
        self.codeArea.selectAll()
        self.codeArea.copy()
        self.close()

# class Demo(QWidget):
#     def __init__(self):
#         super().__init__()
#         setTheme(Theme.DARK)
#         self.setStyleSheet('Demo{background:rgb(32,32,32)}')

#         self.hBxoLayout = QHBoxLayout(self)
#         self.button = PushButton('URL', self)

#         self.resize(600, 600)
#         self.hBxoLayout.addWidget(self.button, 0, Qt.AlignCenter)
#         self.button.clicked.connect(self.showDialog)

#     def showDialog(self):
#         w = GeneratedCodeMessageBox(self)
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
