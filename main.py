"""
Ponto de entrada principal da aplicação
"""
import sys
from PyQt5 import QtWidgets
from src.ui.windows.login_window import LoginWindow

def main():
    """Application entry point"""
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 