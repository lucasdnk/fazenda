import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teste do Sistema")
        self.setGeometry(100, 100, 400, 300)

        # Create a central widget and a layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add a label
        label = QLabel("Sistema de Gestão Agrícola")
        layout.addWidget(label)

        # Add a test button
        button = QPushButton("Testar Conexão")
        button.clicked.connect(self.test_connection)
        layout.addWidget(button)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

    def test_connection(self):
        try:
            import requests
            response = requests.get('http://localhost:5000/farms')
            if response.status_code == 200:
                self.status_label.setText("Conexão bem sucedida!")
            else:
                self.status_label.setText(f"Erro na conexão: {response.status_code}")
        except Exception as e:
            self.status_label.setText(f"Erro: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 