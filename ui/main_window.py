from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QStatusBar, QToolBar
)
from PyQt5.QtCore import Qt

from .tabs.maquinario_tab import MaquinarioTab
from .tabs.funcionarios_tab import FuncionariosTab
from .tabs.financeiro_tab import FinanceiroTab
from .tabs.producao_tab import ProducaoTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Sistema de Gerenciamento de Fazenda")
        self.setGeometry(100, 100, 1200, 800)
        
        # Criar widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout principal
        self.layout = QVBoxLayout(self.central_widget)
        
        # Criar barra de status
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Sistema iniciado com sucesso")
        
        # Criar barra de ferramentas
        self.toolbar = QToolBar("Barra de Ferramentas Principal")
        self.addToolBar(self.toolbar)
        
        # Adicionar ações à barra de ferramentas
        self.setup_toolbar()
        
        # Criar tabs
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)
        
        # Adicionar tabs
        self.setup_tabs()
        
        # Botões de rodapé
        self.setup_footer()
    
    def setup_toolbar(self):
        # Barra de ferramentas vazia
        pass
    
    def setup_tabs(self):
        # Tab de Financeiro (Despesas e Receitas)
        self.financeiro_tab = FinanceiroTab()
        self.tab_widget.addTab(self.financeiro_tab, "Financeiro")
        
        # Tab de Maquinário
        self.maquinario_tab = MaquinarioTab()
        self.tab_widget.addTab(self.maquinario_tab, "Maquinário")
        
        # Tab de Produção
        self.producao_tab = ProducaoTab()
        self.tab_widget.addTab(self.producao_tab, "Produção")
        
        # Tab de Funcionários
        self.funcionarios_tab = FuncionariosTab()
        self.tab_widget.addTab(self.funcionarios_tab, "Funcionários")
    
    def setup_footer(self):
        # Rodapé sem botões
        footer_layout = QHBoxLayout()
        self.layout.addLayout(footer_layout) 