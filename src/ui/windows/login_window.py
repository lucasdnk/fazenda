"""
Janela de login da aplicação
"""
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from src.config.settings import (
    APP_NAME,
    WINDOW_DEFAULT_WIDTH,
    WINDOW_DEFAULT_HEIGHT,
    WINDOW_DEFAULT_X,
    WINDOW_DEFAULT_Y
)
from src.services.auth_service import AuthService
from src.ui.styles.default_styles import BUTTON_STYLE, WINDOW_STYLE, INPUT_STYLE

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.auth_service = AuthService()
        self.setup_ui()

    def setup_ui(self):
        """Configura a interface do usuário"""
        self.setWindowTitle(f"Login - {APP_NAME}")
        self.setGeometry(
            WINDOW_DEFAULT_X,
            WINDOW_DEFAULT_Y,
            WINDOW_DEFAULT_WIDTH,
            WINDOW_DEFAULT_HEIGHT
        )

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
        login_button.clicked.connect(self.handle_login)
        login_button.setStyleSheet(BUTTON_STYLE)
        layout.addWidget(login_button)

        # Aplica estilos
        self.setStyleSheet(WINDOW_STYLE + INPUT_STYLE)

    def handle_login(self):
        """Manipula o evento de login"""
        success, data, error_message = self.auth_service.login(
            self.username_input.text(),
            self.password_input.text()
        )

        if success:
            from src.ui.windows.main_window import MainWindow
            self.main_window = MainWindow(
                token=data['token'],
                role=data['role'],
                permissions=data['permissions']
            )
            self.main_window.show()
            self.close()
        else:
            QMessageBox.critical(self, "Erro", error_message) 