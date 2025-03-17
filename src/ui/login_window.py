from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import requests
from src.ui.main_window import MainWindow
from src.config.settings import API_BASE_URL

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):
        """Initialize and setup UI components"""
        self.setWindowTitle("Login - Sistema de Gestão Agrícola")
        self.setGeometry(100, 100, 400, 200)

        # Widget central
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Form layout para os campos
        form_layout = QtWidgets.QFormLayout()

        # Campos de entrada
        self.username_input = QtWidgets.QLineEdit()
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        # Adiciona campos ao form layout
        form_layout.addRow("Usuário:", self.username_input)
        form_layout.addRow("Senha:", self.password_input)

        # Adiciona o form layout ao layout principal
        layout.addLayout(form_layout)

        # Botão de login
        login_button = QtWidgets.QPushButton("Entrar")
        login_button.clicked.connect(self.do_login)
        login_button.setStyleSheet(self.get_button_style())
        layout.addWidget(login_button)

    def setup_styles(self):
        """Setup window and component styles"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)

    @staticmethod
    def get_button_style():
        """Return the style for the login button"""
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

    def do_login(self):
        """Handle login attempt"""
        try:
            response = requests.post(f'{API_BASE_URL}/auth/login', json={
                'username': self.username_input.text(),
                'password': self.password_input.text()
            })

            if response.status_code == 200:
                token = response.json()['token']
                self.main_window = MainWindow(token)
                self.main_window.show()
                self.close()
            else:
                QMessageBox.critical(self, "Erro", "Usuário ou senha inválidos")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao conectar ao servidor: {str(e)}") 