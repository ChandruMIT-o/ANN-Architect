import sys, csv
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QSpacerItem
from qfluentwidgets import (MessageBoxBase, SubtitleLabel, PushButton, setTheme, Theme, TableWidget, CheckBox,
                            ProgressBar, setCustomStyleSheet, SegmentedWidget, CaptionLabel, PrimaryPushButton,
                            LineEdit, PasswordLineEdit, InfoBar, InfoBarPosition, FluentThemeColor)
from qfluentwidgets import FluentIcon as FIF

class SignInUpDialog(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pivot = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.signInLayout = QVBoxLayout()
        self.signUpLayout = QVBoxLayout()

        self.signInLayout.setAlignment(Qt.AlignTop)
        self.signUpLayout.setAlignment(Qt.AlignTop)

        self.signInLayout.addWidget(QWidget(self))
        self.signUpLayout.addWidget(QWidget(self))

        self.addSubInterface(self.signInLayout, 'signInInterface', 'Sign In')
        self.addSubInterface(self.signUpLayout, 'signUpInterface', 'Sign Up')

        self.vBoxLayout.addWidget(self.pivot)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setAlignment(Qt.AlignRight)
        self.vBoxLayout.setContentsMargins(10, 10, 10, 10)

        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))
        self.pivot.setCurrentItem('signInInterface')
        self.pivot.currentItemChanged.connect(
            lambda k: self.stackedWidget.setCurrentWidget(self.findChild(QWidget, k))
        )

        self.yesButton.setText('Sign In')
        self.cancelButton.setText('Close')
        self.cancelButton.clicked.connect(self.close)
        # self.cancelButton.setDisabled(True)

        self.yesButton.disconnect()
        self.yesButton.clicked.connect(self.sign_me_in)

        self.widget.setMinimumWidth(350)
        self.widget.setMaximumWidth(750)

        self.viewLayout.addWidget(self.pivot)

        self.viewLayout.addWidget(self.stackedWidget)

        self.pivot.currentItemChanged.connect(self.switchYesButton)

    def switchYesButton(self):
        if (self.pivot.currentItem().text() == "Sign In"):
            self.yesButton.clicked.connect(self.sign_me_in)
            self.yesButton.setText("Sign In")
        elif (self.pivot.currentItem().text() == 'Sign Up'):
            self.yesButton.clicked.connect(self.sign_me_up)
            self.yesButton.setText("Sign Up")

    def addSubInterface(self, layout: QVBoxLayout, objectName, text):

        layout.setSpacing(10)

        if text == 'Sign In':

            self.userNameLabel1 = CaptionLabel("Email Address")
            self.passwordLabel1 = CaptionLabel("Password")

            self.emailInputEdit1 = LineEdit(self)
            self.emailInputEdit1.setPlaceholderText("Email")
            self.validateEmailText1 = CaptionLabel("We need a unique email address")
            self.validateEmailText1.setHidden(True)
            self.passwordInputEdit1 = PasswordLineEdit(self)
            self.passwordInputEdit1.setPlaceholderText("Min 3 Characters")
            
            layout.addWidget(self.userNameLabel1)
            layout.addWidget(self.emailInputEdit1)
            layout.addWidget(self.passwordLabel1)
            layout.addWidget(self.passwordInputEdit1)

        elif text == 'Sign Up':

            self.userNameLabel = CaptionLabel("Enter email address")
            self.passwordLabel = CaptionLabel("Enter Password")

            self.emailInputEdit = LineEdit(self)
            self.emailInputEdit.setPlaceholderText("Email")
            self.emailInputEdit.textChanged.connect(self.validateEmail)
            self.validateEmailText = CaptionLabel("We need a unique email address")
            self.validateEmailText.setHidden(True)
            self.passwordInputEdit = PasswordLineEdit(self)
            self.passwordInputEdit.setPlaceholderText("Min 3 Characters!")
            self.passwordInputEdit.textChanged.connect(self.checkPasswordStrength)

            self.progressStatus = CaptionLabel("Not a password game!")

            self.progressBar = ProgressBar(self)              
            
            layout.addWidget(self.userNameLabel)
            layout.addWidget(self.emailInputEdit)
            layout.addWidget(self.validateEmailText, alignment=Qt.AlignmentFlag.AlignRight)
            layout.addWidget(self.passwordLabel)
            layout.addWidget(self.passwordInputEdit)
            layout.addWidget(self.progressStatus, alignment=Qt.AlignmentFlag.AlignRight)
            layout.addWidget(self.progressBar)

        widget = QWidget(self)
        widget.setLayout(layout)
        widget.setObjectName(objectName)

        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(routeKey=objectName, text=text)

        self.viewLayout.addWidget(self.stackedWidget)

    def sign_me_up(self):
        if self.validateEmail() and self.checkPasswordStrength() > 80:
            w = InfoBar.success(
                title='SignUp',
                content="Account Created!",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=3500, 
                parent=self
            )
            w.show()
            self.close()
        else:
            w = InfoBar.error(
                title='SignUp',
                content="Email Address or Password Error",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=3500, 
                parent=self
            )
            w.show()

    def sign_me_in(self):

        email = self.emailInputEdit1.text().strip()
        password = self.passwordInputEdit1.text().strip()

        print(email, password)

        # TODO: use the given email and password to check if the user is signed in or not.
        # * (essentially return true or false from the database)

        if email == "chandru@gmail.com" and password == "Chandru@0503":
            w = InfoBar.success(
                title='SignIn',
                content="Signing In like old times!",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=3500, 
                parent=self
            )
            w.show()
            self.close()
        else:
            w = InfoBar.error(
                title='SignIn',
                content="Invalid Email Address or Password",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=3500, 
                parent=self
            )
            w.show()

    def validateEmail(self):
        emails = ["rameez@gmail.com"]  # Predefined list of existing emails
        email = self.emailInputEdit.text().strip()

        self.validateEmailText.setHidden(not bool(email))

        if not email:
            self.validateEmailText.setText("Email address cannot be empty")
            return False

        if "@" not in email or "." not in email:
            self.validateEmailText.setText("Enter a valid email address")
            return False
        
        # TODO: check if the email address already exists or not. 
        # * (essentially return False or True)

        if email in emails:
            self.validateEmailText.setText("Email is already in use")
            return False

        self.validateEmailText.setHidden(True)
        return True


    def checkPasswordStrength(self):
        password = self.passwordInputEdit.text()
        strength = self.getPasswordStrength(password)
        self.progressBar.setValue(strength)
        self.progressStatus.setText(self.getPasswordStrengthLabel(strength))

        return strength

    def getPasswordStrength(self, password):
        # Simple password strength check logic (scored out of 100)
        length = len(password)
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_-+=<>,.?" for c in password)

        strength = 20 * (has_lower + has_upper + has_digit + has_special)
        if length >= 8:
            strength += 20
        return min(strength, 100)

    def getPasswordStrengthLabel(self, strength):
        if strength < 40:
            self.progressBar.setCustomBarColor(FluentThemeColor.DEFAULT_BLUE.color(), FluentThemeColor.NAVY_BLUE.color())
            return "Bruh!"
        elif strength < 60:
            self.progressBar.setCustomBarColor(FluentThemeColor.DEFAULT_BLUE.color(), FluentThemeColor.ORANGE_BRIGHT.color())
            return "You can do better!"
        elif strength < 80:
            self.progressBar.setCustomBarColor(FluentThemeColor.DEFAULT_BLUE.color(), FluentThemeColor.YELLOW_GOLD.color())
            return "Maybe slightly more?"
        else:
            self.progressBar.setCustomBarColor(FluentThemeColor.DEFAULT_BLUE.color(), FluentThemeColor.GREEN.color())
            return "Now you got it!"


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setStyleSheet('Demo{background:rgb(32,32,32)}')

        self.hBxoLayout = QHBoxLayout(self)
        self.button = PushButton('Summary', self)

        self.resize(600, 600)
        self.hBxoLayout.addWidget(self.button, 0, Qt.AlignCenter)
        self.button.clicked.connect(self.showDialog)

    def showDialog(self):
        w = SignInUpDialog(self)
        if w.exec():
            pass

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()
