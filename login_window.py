import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import requests
from main_window import MainWindow

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
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
        login_button.setStyleSheet("""
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
        """)
        layout.addWidget(login_button)

        # Estilo da janela
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

    def do_login(self):
        try:
            response = requests.post('http://localhost:5000/auth/login', json={
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

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 