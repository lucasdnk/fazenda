"""
Janela principal da aplicação
"""
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QFrame
from src.config.settings import APP_NAME, WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT
from src.ui.styles.default_styles import BUTTON_STYLE, WINDOW_STYLE

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, token, role, permissions):
        super(MainWindow, self).__init__()
        self.token = token
        self.role = role
        self.permissions = permissions
        self.setup_ui()

    def setup_ui(self):
        """Configura a interface do usuário"""
        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, WINDOW_DEFAULT_WIDTH * 2, WINDOW_DEFAULT_HEIGHT * 2)

        # Widget central
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QtWidgets.QHBoxLayout(central_widget)
        
        # Sidebar (menu lateral)
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar, 1)
        
        # Área de conteúdo principal
        content_area = self.create_content_area()
        main_layout.addWidget(content_area, 4)
        
        # Aplica estilos
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel#welcome_label {
                font-size: 24px;
                color: #333;
                margin: 20px;
                font-weight: bold;
            }
            QPushButton {
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
                margin: 5px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QFrame#sidebar {
                background-color: #2C3E50;
                border-radius: 0px;
                padding: 10px;
            }
            QFrame#content {
                background-color: white;
                border-radius: 10px;
                margin: 10px;
            }
        """)

    def create_sidebar(self):
        """Cria o menu lateral"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        layout = QtWidgets.QVBoxLayout(sidebar)
        
        # Logo ou título
        logo = QtWidgets.QLabel("🌾 FAZENDA")
        logo.setStyleSheet("color: white; font-size: 20px; font-weight: bold; margin: 20px 0;")
        layout.addWidget(logo)
        
        # Informações do usuário
        user_info = QtWidgets.QLabel(f"👤 Perfil: {self.role.upper()}")
        user_info.setStyleSheet("color: #95a5a6; font-size: 12px; margin: 10px 0;")
        layout.addWidget(user_info)
        
        # Botões do menu baseados nas permissões
        menu_buttons = []
        
        if "dashboard" in self.permissions:
            menu_buttons.append(("🏠 Dashboard", self.show_dashboard))
        
        if "manage_crops" in self.permissions:
            menu_buttons.append(("🌱 Gerenciar Cultivos", self.manage_crops))
        elif "view_crops" in self.permissions:
            menu_buttons.append(("🌱 Visualizar Cultivos", self.view_crops))
            
        if "manage_farms" in self.permissions:
            menu_buttons.append(("🚜 Gerenciar Fazendas", self.manage_farms))
        elif "view_farms" in self.permissions:
            menu_buttons.append(("🚜 Visualizar Fazendas", self.view_farms))
            
        if "reports" in self.permissions:
            menu_buttons.append(("📊 Relatórios", self.show_reports))
        elif "view_reports" in self.permissions:
            menu_buttons.append(("📊 Visualizar Relatórios", self.view_reports))
            
        if "settings" in self.permissions:
            menu_buttons.append(("⚙️ Configurações", self.show_settings))
            
        if "users" in self.permissions:
            menu_buttons.append(("👥 Gerenciar Usuários", self.manage_users))

        for text, callback in menu_buttons:
            button = QtWidgets.QPushButton(text)
            button.setStyleSheet("""
                QPushButton {
                    color: white;
                    background-color: transparent;
                }
                QPushButton:hover {
                    background-color: #34495E;
                }
            """)
            button.clicked.connect(callback)
            layout.addWidget(button)

        # Espaçador para empurrar o botão de logout para baixo
        layout.addStretch()
        
        # Botão de logout
        logout_btn = QtWidgets.QPushButton("🚪 Sair")
        logout_btn.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #E74C3C;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)
        
        return sidebar

    def create_content_area(self):
        """Cria a área de conteúdo principal"""
        content = QFrame()
        content.setObjectName("content")
        layout = QtWidgets.QVBoxLayout(content)
        
        # Label de boas-vindas
        welcome_text = "Bem-vindo ao Sistema de Gestão Agrícola!"
        if self.role == "admin":
            welcome_text += " (Administrador)"
        welcome_label = QtWidgets.QLabel(welcome_text)
        welcome_label.setObjectName("welcome_label")
        welcome_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(welcome_label)
        
        # Área de cards com informações
        cards_layout = QtWidgets.QHBoxLayout()
        
        # Cards baseados nas permissões
        cards = []
        if any(p in self.permissions for p in ["manage_crops", "view_crops"]):
            cards.append(("🌾 Cultivos Ativos", "12"))
            
        if any(p in self.permissions for p in ["manage_farms", "view_farms"]):
            cards.append(("🚜 Fazendas", "3"))
            
        if any(p in self.permissions for p in ["reports", "view_reports"]):
            cards.append(("📊 Relatórios Pendentes", "5"))
            
        if "users" in self.permissions:
            cards.append(("👥 Usuários Ativos", "8"))
        
        for title, value in cards:
            card = self.create_info_card(title, value)
            cards_layout.addWidget(card)
        
        layout.addLayout(cards_layout)
        layout.addStretch()
        
        return content

    def create_info_card(self, title, value):
        """Cria um card de informação"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(card)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("font-size: 16px; color: #666;")
        
        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet("font-size: 24px; color: #2C3E50; font-weight: bold;")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        return card

    # Métodos para administradores
    def show_dashboard(self):
        QMessageBox.information(self, "Info", "Dashboard em desenvolvimento")

    def manage_farms(self):
        QMessageBox.information(self, "Info", "Gerenciamento de Fazendas em desenvolvimento")

    def manage_crops(self):
        QMessageBox.information(self, "Info", "Gerenciamento de Cultivos em desenvolvimento")

    def show_reports(self):
        QMessageBox.information(self, "Info", "Relatórios em desenvolvimento")

    def show_settings(self):
        QMessageBox.information(self, "Info", "Configurações em desenvolvimento")

    def manage_users(self):
        QMessageBox.information(self, "Info", "Gerenciamento de Usuários em desenvolvimento")

    # Métodos para usuários comuns
    def view_farms(self):
        QMessageBox.information(self, "Info", "Visualização de Fazendas em desenvolvimento")

    def view_crops(self):
        QMessageBox.information(self, "Info", "Visualização de Cultivos em desenvolvimento")

    def view_reports(self):
        QMessageBox.information(self, "Info", "Visualização de Relatórios em desenvolvimento")

    def logout(self):
        reply = QMessageBox.question(self, 'Confirmação',
                                   'Deseja realmente sair?',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close() 