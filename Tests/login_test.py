from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QLabel, QVBoxLayout, QWidget, QPushButton, QStackedWidget
from PySide6.QtCore import Signal, QThread
import sys
import bcrypt
import db
from session import validate_session, create_session
from bsed import stat_increment
def validate_username(username: str) -> bool:
    return 3 <= len(username) <= 32 and username.isalnum()
def validate_password(pw: str) -> bool:
    return (len(pw) >= 8 and any(c.islower() for c in pw) and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw) and any(not c.isalnum() for c in pw))
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
class AuthWorker(QThread):
    finished = Signal(bool, str)  # success, message

    def __init__(self, mode, username, password, password2=None, save_blob=stat_increment):
        super().__init__()
        self.mode = mode
        self.username = username
        self.password = password
        self.password2 = password2
        self.save_blob = save_blob

    def run(self):
        try:
            if self.mode == "register":
                if self.password != self.password2:
                    self.finished.emit(False, "Passwords do not match")
                    return

                hashed = hash_password(self.password)

                success = db.create_account(
                    self.username,
                    hashed,
                    self.save_blob
                )

                if success:
                    self.finished.emit(True, "Account created")
                else:
                    self.finished.emit(False, "Username already exists")

            elif self.mode == "login":
                row = db.get_account(self.username)

                if not row:
                    self.finished.emit(False, "Account not found")
                    return
                if check_password(self.password, row[0]['password_hash']):
                    self.finished.emit(True, "Login successful")
                else:
                    self.finished.emit(False, "Incorrect password")

        except Exception as e:
            self.finished.emit(False, f"Error: {e}")
class LoginWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.status = QLabel("")
        self.login_btn = QPushButton("Login")
        register_alternative = QPushButton("Don't have an account? Create one instead!")
        self.login_btn.clicked.connect(parent.login)
        register_alternative.clicked.connect(parent.open_register)
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password)
        layout.addWidget(self.login_btn)
        layout.addWidget(register_alternative)
        layout.addWidget(self.status)
        self.setLayout(layout)
class RegisterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password2 = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password2.setEchoMode(QLineEdit.Password)
        self.status = QLabel("")
        self.register_btn = QPushButton("Register")
        login_alternative = QPushButton("Already have an account? Login instead!")
        self.register_btn.clicked.connect(self.parent().register)
        login_alternative.clicked.connect(self.parent().open_login)
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password)
        layout.addWidget(QLabel("Repeat Password"))
        layout.addWidget(self.password2)
        layout.addWidget(self.register_btn)
        layout.addWidget(login_alternative)
        layout.addWidget(self.status)
        self.setLayout(layout)
class AuthWindow(QDialog):
    def __init__(self, type, parent=None):
        super().__init__(parent)
        self.registered = Signal()
        self.type = type
        self.central = QStackedWidget()
        layout = QVBoxLayout()
        
        self.login_w = LoginWidget(self)
        self.register_w = RegisterWidget(self)
        
        self.central.addWidget(self.login_w)
        self.central.addWidget(self.register_w)
        layout.addWidget(self.central)
        self.setLayout(layout)
        if type == "Register":
            self.central.setCurrentWidget(self.register_w)
        else:
            self.central.setCurrentWidget(self.login_w)
        self.worker = None

    def register(self):
        u = self.register_w.username.text().strip()
        p1 = self.register_w.password.text()
        p2 = self.register_w.password2.text()

        if not validate_username(u):
            self.register_w.status.setText("Invalid username")
            return

        if not validate_password(p1):
            self.register_w.status.setText("Weak password")
            return

        self.start_worker("register", u, p1, p2)
    def login(self):
        u = self.login_w.username.text().strip()
        p = self.login_w.password.text()

        self.start_worker("login", u, p)

    def start_worker(self, mode, username, password, password2=None):
        self.worker = AuthWorker(mode, username, password, password2)
        self.worker.finished.connect(self.on_result)
        self.worker.start()

        self.central.currentWidget().status.setText("Working...")

    def on_result(self, success, message):
        self.central.currentWidget().status.setText(message)

        if success:
            if not validate_session():
              create_session(self.central.currentWidget().username.text().strip())
    def open_register(self):
        self.central.setCurrentWidget(self.register_w)
    def open_login(self):
        self.central.setCurrentWidget(self.login_w)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    user = validate_session()
    if not user:
     root = AuthWindow("Login")
     root.show()
    else:
     print(f"Hello {user}!")
     sys.exit()
    sys.exit(app.exec())