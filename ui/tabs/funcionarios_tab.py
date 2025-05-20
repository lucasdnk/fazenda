from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QLabel, QDialog,
    QFormLayout, QLineEdit, QDateEdit, QTextEdit, QComboBox,
    QMessageBox, QHeaderView, QCheckBox
)
from PyQt5.QtCore import Qt, QDate

from database import get_session, Funcionario

class FuncionariosTab(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal
        self.layout = QVBoxLayout(self)
        
        # Título
        self.title_label = QLabel("Gerenciamento de Funcionários")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(self.title_label)
        
        # Botões de ação
        self.action_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Adicionar Funcionário")
        self.add_button.clicked.connect(self.add_funcionario)
        self.action_layout.addWidget(self.add_button)
        
        self.delete_button = QPushButton("Excluir Selecionado")
        self.delete_button.clicked.connect(self.delete_funcionario)
        self.action_layout.addWidget(self.delete_button)
        
        self.refresh_button = QPushButton("Atualizar Lista")
        self.refresh_button.clicked.connect(self.load_funcionarios)
        self.action_layout.addWidget(self.refresh_button)
        
        self.layout.addLayout(self.action_layout)
        
        # Tabela de funcionários
        self.table = QTableWidget()
        self.table.setColumnCount(7)  # Aumentado para incluir coluna do botão Editar
        self.table.setHorizontalHeaderLabels([
            "Nome", "CPF", "Cargo", "Salário (R$)", 
            "Data Contratação", "Ativo", "Ações"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Definir largura da coluna de ações
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.layout.addWidget(self.table)
        
        # Carregar dados iniciais
        self.load_funcionarios()
        
        # Dicionário para armazenar os botões de editar
        self.edit_buttons = {}
    
    def load_funcionarios(self):
        """Carrega os funcionários do banco de dados para a tabela."""
        try:
            session = get_session()
            funcionarios = session.query(Funcionario).all()
            
            self.table.setRowCount(0)  # Limpar tabela
            self.edit_buttons = {}  # Limpar referências de botões
            
            for i, funcionario in enumerate(funcionarios):
                self.table.insertRow(i)
                self.table.setItem(i, 0, QTableWidgetItem(funcionario.nome))
                self.table.setItem(i, 1, QTableWidgetItem(funcionario.cpf or ""))
                self.table.setItem(i, 2, QTableWidgetItem(funcionario.cargo or ""))
                
                salario = "-"
                if funcionario.salario:
                    salario = f"R$ {float(funcionario.salario):,.2f}".replace(".", "X").replace(",", ".").replace("X", ",")
                self.table.setItem(i, 3, QTableWidgetItem(salario))
                
                data = "-"
                if funcionario.data_contratacao:
                    data = funcionario.data_contratacao.strftime("%d/%m/%Y")
                self.table.setItem(i, 4, QTableWidgetItem(data))
                
                ativo = "Sim" if funcionario.ativo else "Não"
                self.table.setItem(i, 5, QTableWidgetItem(ativo))
                
                # Adiciona botão editar na última coluna
                edit_btn = QPushButton("Editar")
                edit_btn.setMaximumWidth(60)  # Reduz largura do botão
                edit_btn.setStyleSheet("font-size: 10px;")  # Reduz tamanho da fonte
                
                # Conectar o botão à edição do registro específico
                edit_btn.clicked.connect(lambda checked, row=i: self.edit_funcionario_from_button(row))
                
                # Armazenar referência ao botão para evitar coleta de lixo
                self.edit_buttons[i] = edit_btn
                
                # Adicionar à tabela
                self.table.setCellWidget(i, 6, edit_btn)
            
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar funcionários: {str(e)}")
    
    def edit_funcionario_from_button(self, row):
        """Edita o funcionário na linha especificada pelo botão."""
        session = get_session()
        funcionarios = session.query(Funcionario).all()
        
        if row >= len(funcionarios):
            QMessageBox.warning(self, "Aviso", "Funcionário não encontrado.")
            session.close()
            return
        
        funcionario = funcionarios[row]
        
        dialog = FuncionarioDialog(self, funcionario)
        if dialog.exec() == QDialog.Accepted:
            self.load_funcionarios()
        
        session.close()
    
    def add_funcionario(self):
        """Abre o diálogo para adicionar um novo funcionário."""
        dialog = FuncionarioDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.load_funcionarios()
    
    def edit_funcionario(self):
        """Abre o diálogo para editar o funcionário selecionado."""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione um funcionário para editar.")
            return
        
        row = selected_items[0].row()
        
        session = get_session()
        funcionarios = session.query(Funcionario).all()
        
        if row >= len(funcionarios):
            QMessageBox.warning(self, "Aviso", "Funcionário não encontrado.")
            session.close()
            return
        
        funcionario = funcionarios[row]
        
        dialog = FuncionarioDialog(self, funcionario)
        if dialog.exec() == QDialog.Accepted:
            self.load_funcionarios()
        
        session.close()
    
    def delete_funcionario(self):
        """Exclui o funcionário selecionado."""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione um funcionário para excluir.")
            return
        
        row = selected_items[0].row()
        
        confirm = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            "Tem certeza que deseja excluir este funcionário?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                session = get_session()
                funcionarios = session.query(Funcionario).all()
                
                if row < len(funcionarios):
                    funcionario = funcionarios[row]
                    session.delete(funcionario)
                    session.commit()
                    QMessageBox.information(self, "Sucesso", "Funcionário excluído com sucesso.")
                    self.load_funcionarios()
                else:
                    QMessageBox.warning(self, "Aviso", "Funcionário não encontrado.")
                
                session.close()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir funcionário: {str(e)}")


class FuncionarioDialog(QDialog):
    """Diálogo para adicionar ou editar funcionário."""
    
    def __init__(self, parent=None, funcionario=None):
        super().__init__(parent)
        self.funcionario = funcionario
        self.setup_ui()
        
        if funcionario:
            self.setWindowTitle("Editar Funcionário")
            self.populate_fields()
        else:
            self.setWindowTitle("Adicionar Funcionário")
    
    def setup_ui(self):
        """Configura a interface do diálogo."""
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Formulário
        form_layout = QFormLayout()
        
        # Campos do formulário
        self.nome_input = QLineEdit()
        form_layout.addRow("Nome:", self.nome_input)
        
        self.cpf_input = QLineEdit()
        self.cpf_input.setInputMask("999.999.999-99")
        form_layout.addRow("CPF:", self.cpf_input)
        
        # Cargo como ComboBox com botão Editar
        cargo_layout = QHBoxLayout()
        self.cargo_input = QComboBox()
        self.cargo_input.addItems([
            "Gerente", "Administrador", "Operador", "Motorista", 
            "Trabalhador Rural", "Secretário", "Técnico", "Outro"
        ])
        self.cargo_input.setEditable(True)
        cargo_layout.addWidget(self.cargo_input)
        
        self.editar_cargo_button = QPushButton("Editar")
        # self.editar_cargo_button.clicked.connect(self.editar_cargos)
        cargo_layout.addWidget(self.editar_cargo_button)
        
        form_layout.addRow("Cargo:", cargo_layout)
        
        self.salario_input = QLineEdit()
        form_layout.addRow("Salário (R$):", self.salario_input)
        
        self.data_input = QDateEdit()
        self.data_input.setDisplayFormat("dd/MM/yyyy")
        self.data_input.setCalendarPopup(True)
        self.data_input.setDate(QDate.currentDate())
        form_layout.addRow("Data de Contratação:", self.data_input)
        
        self.ativo_input = QCheckBox("Funcionário Ativo")
        self.ativo_input.setChecked(True)
        form_layout.addRow("", self.ativo_input)
        
        self.telefone_input = QLineEdit()
        self.telefone_input.setInputMask("(99) 99999-9999")
        form_layout.addRow("Telefone:", self.telefone_input)
        
        self.endereco_input = QTextEdit()
        form_layout.addRow("Endereço:", self.endereco_input)
        
        layout.addLayout(form_layout)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.save_funcionario)
        buttons_layout.addWidget(self.save_button)
        
        layout.addLayout(buttons_layout)
    
    def populate_fields(self):
        """Preenche os campos com os dados do funcionário a ser editado."""
        self.nome_input.setText(self.funcionario.nome)
        self.cpf_input.setText(self.funcionario.cpf or "")
        
        # Atualizar para usar ComboBox
        if self.funcionario.cargo:
            index = self.cargo_input.findText(self.funcionario.cargo)
            if index >= 0:
                self.cargo_input.setCurrentIndex(index)
            else:
                self.cargo_input.setCurrentText(self.funcionario.cargo)
        
        if self.funcionario.salario:
            self.salario_input.setText(str(float(self.funcionario.salario)))
        
        if self.funcionario.data_contratacao:
            date = QDate.fromString(
                self.funcionario.data_contratacao.strftime("%Y-%m-%d"),
                "yyyy-MM-dd"
            )
            self.data_input.setDate(date)
        
        self.ativo_input.setChecked(self.funcionario.ativo)
        self.telefone_input.setText(self.funcionario.telefone or "")
        self.endereco_input.setText(self.funcionario.endereco or "")
    
    def save_funcionario(self):
        """Salva o funcionário no banco de dados."""
        # Validar campos obrigatórios
        if not self.nome_input.text().strip():
            QMessageBox.warning(self, "Aviso", "O nome do funcionário é obrigatório.")
            return
        
        try:
            session = get_session()
            
            # Criar ou atualizar funcionário
            if not self.funcionario:
                self.funcionario = Funcionario()
                session.add(self.funcionario)
            
            # Atualizar dados
            self.funcionario.nome = self.nome_input.text().strip()
            self.funcionario.cpf = self.cpf_input.text().strip()
            self.funcionario.cargo = self.cargo_input.currentText().strip()
            
            if self.salario_input.text().strip():
                # Remover possíveis separadores de milhar e trocar vírgula por ponto
                salario_texto = self.salario_input.text().strip().replace(".", "").replace(",", ".")
                self.funcionario.salario = float(salario_texto)
            else:
                self.funcionario.salario = None
            
            self.funcionario.data_contratacao = self.data_input.date().toPyDate()
            self.funcionario.ativo = self.ativo_input.isChecked()
            self.funcionario.telefone = self.telefone_input.text().strip()
            self.funcionario.endereco = self.endereco_input.toPlainText().strip()
            
            # Commit
            session.commit()
            
            # Fechar diálogo
            self.accept()
            
            QMessageBox.information(
                self,
                "Sucesso",
                "Funcionário salvo com sucesso!"
            )
            
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar funcionário: {str(e)}")
            session.rollback()
            session.close() 