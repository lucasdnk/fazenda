from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QLabel, QDialog,
    QFormLayout, QLineEdit, QDateEdit, QTextEdit, QComboBox,
    QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt, QDate

from database import get_session, Maquinario

class MaquinarioTab(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal
        self.layout = QVBoxLayout(self)
        
        # Título
        self.title_label = QLabel("Gerenciamento de Maquinário")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(self.title_label)
        
        # Botões de ação
        self.action_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Adicionar Maquinário")
        self.add_button.clicked.connect(self.add_maquinario)
        self.action_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton("Editar Selecionado")
        self.edit_button.clicked.connect(self.edit_maquinario)
        self.action_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Excluir Selecionado")
        self.delete_button.clicked.connect(self.delete_maquinario)
        self.action_layout.addWidget(self.delete_button)
        
        self.refresh_button = QPushButton("Atualizar Lista")
        self.refresh_button.clicked.connect(self.load_maquinarios)
        self.action_layout.addWidget(self.refresh_button)
        
        self.layout.addLayout(self.action_layout)
        
        # Tabela de maquinários
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Nome", "Modelo", "Ano", "Valor (R$)", 
            "Data Aquisição", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)
        
        # Carregar dados iniciais
        self.load_maquinarios()
    
    def load_maquinarios(self):
        """Carrega os maquinários do banco de dados para a tabela."""
        try:
            session = get_session()
            maquinarios = session.query(Maquinario).all()
            
            self.table.setRowCount(0)  # Limpar tabela
            
            for i, maquinario in enumerate(maquinarios):
                self.table.insertRow(i)
                self.table.setItem(i, 0, QTableWidgetItem(maquinario.nome))
                self.table.setItem(i, 1, QTableWidgetItem(maquinario.modelo))
                self.table.setItem(i, 2, QTableWidgetItem(str(maquinario.ano or "")))
                
                valor = "-"
                if maquinario.valor_aquisicao:
                    valor = f"R$ {float(maquinario.valor_aquisicao):.2f}"
                self.table.setItem(i, 3, QTableWidgetItem(valor))
                
                data = "-"
                if maquinario.data_aquisicao:
                    data = maquinario.data_aquisicao.strftime("%d/%m/%Y")
                self.table.setItem(i, 4, QTableWidgetItem(data))
                
                self.table.setItem(i, 5, QTableWidgetItem(maquinario.status or ""))
            
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar maquinários: {str(e)}")
    
    def add_maquinario(self):
        """Abre o diálogo para adicionar um novo maquinário."""
        dialog = MaquinarioDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.load_maquinarios()
    
    def edit_maquinario(self):
        """Abre o diálogo para editar o maquinário selecionado."""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione um maquinário para editar.")
            return
        
        row = selected_items[0].row()
        
        session = get_session()
        maquinarios = session.query(Maquinario).all()
        
        if row >= len(maquinarios):
            QMessageBox.warning(self, "Aviso", "Maquinário não encontrado.")
            session.close()
            return
        
        maquinario = maquinarios[row]
        
        dialog = MaquinarioDialog(self, maquinario)
        if dialog.exec() == QDialog.Accepted:
            self.load_maquinarios()
        
        session.close()
    
    def delete_maquinario(self):
        """Exclui o maquinário selecionado."""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione um maquinário para excluir.")
            return
        
        row = selected_items[0].row()
        
        confirm = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            "Tem certeza que deseja excluir este maquinário?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                session = get_session()
                maquinarios = session.query(Maquinario).all()
                
                if row < len(maquinarios):
                    maquinario = maquinarios[row]
                    session.delete(maquinario)
                    session.commit()
                    QMessageBox.information(self, "Sucesso", "Maquinário excluído com sucesso.")
                    self.load_maquinarios()
                else:
                    QMessageBox.warning(self, "Aviso", "Maquinário não encontrado.")
                
                session.close()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir maquinário: {str(e)}")


class MaquinarioDialog(QDialog):
    """Diálogo para adicionar ou editar maquinário."""
    
    def __init__(self, parent=None, maquinario=None):
        super().__init__(parent)
        self.maquinario = maquinario
        self.setup_ui()
        
        if maquinario:
            self.setWindowTitle("Editar Maquinário")
            self.populate_fields()
        else:
            self.setWindowTitle("Adicionar Maquinário")
    
    def setup_ui(self):
        """Configura a interface do diálogo."""
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Formulário
        form_layout = QFormLayout()
        
        # Campos do formulário
        self.nome_input = QLineEdit()
        form_layout.addRow("Nome:", self.nome_input)
        
        self.modelo_input = QLineEdit()
        form_layout.addRow("Modelo:", self.modelo_input)
        
        self.ano_input = QLineEdit()
        form_layout.addRow("Ano:", self.ano_input)
        
        self.valor_input = QLineEdit()
        form_layout.addRow("Valor de Aquisição (R$):", self.valor_input)
        
        self.data_input = QDateEdit()
        self.data_input.setDisplayFormat("dd/MM/yyyy")
        self.data_input.setCalendarPopup(True)
        self.data_input.setDate(QDate.currentDate())
        form_layout.addRow("Data de Aquisição:", self.data_input)
        
        self.status_input = QComboBox()
        self.status_input.addItems(["Ativo", "Em manutenção", "Inativo"])
        form_layout.addRow("Status:", self.status_input)
        
        self.obs_input = QTextEdit()
        form_layout.addRow("Observações:", self.obs_input)
        
        layout.addLayout(form_layout)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.save_maquinario)
        buttons_layout.addWidget(self.save_button)
        
        layout.addLayout(buttons_layout)
    
    def populate_fields(self):
        """Preenche os campos com os dados do maquinário a ser editado."""
        self.nome_input.setText(self.maquinario.nome)
        self.modelo_input.setText(self.maquinario.modelo or "")
        self.ano_input.setText(str(self.maquinario.ano or ""))
        
        if self.maquinario.valor_aquisicao:
            self.valor_input.setText(str(float(self.maquinario.valor_aquisicao)))
        
        if self.maquinario.data_aquisicao:
            date = QDate.fromString(
                self.maquinario.data_aquisicao.strftime("%Y-%m-%d"),
                "yyyy-MM-dd"
            )
            self.data_input.setDate(date)
        
        if self.maquinario.status:
            index = self.status_input.findText(self.maquinario.status)
            if index >= 0:
                self.status_input.setCurrentIndex(index)
        
        self.obs_input.setText(self.maquinario.observacoes or "")
    
    def save_maquinario(self):
        """Salva o maquinário no banco de dados."""
        # Validar campos obrigatórios
        if not self.nome_input.text().strip():
            QMessageBox.warning(self, "Aviso", "O nome do maquinário é obrigatório.")
            return
        
        try:
            session = get_session()
            
            # Criar ou atualizar maquinário
            if not self.maquinario:
                self.maquinario = Maquinario()
                session.add(self.maquinario)
            
            # Atualizar dados
            self.maquinario.nome = self.nome_input.text().strip()
            self.maquinario.modelo = self.modelo_input.text().strip()
            
            if self.ano_input.text().strip():
                self.maquinario.ano = int(self.ano_input.text().strip())
            else:
                self.maquinario.ano = None
            
            if self.valor_input.text().strip():
                self.maquinario.valor_aquisicao = float(self.valor_input.text().strip())
            else:
                self.maquinario.valor_aquisicao = None
            
            self.maquinario.data_aquisicao = self.data_input.date().toPython()
            self.maquinario.status = self.status_input.currentText()
            self.maquinario.observacoes = self.obs_input.toPlainText().strip()
            
            # Commit
            session.commit()
            
            # Fechar diálogo
            self.accept()
            
            QMessageBox.information(
                self,
                "Sucesso",
                "Maquinário salvo com sucesso!"
            )
            
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar maquinário: {str(e)}")
            session.rollback()
            session.close() 