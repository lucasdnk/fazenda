from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QLabel, QDialog,
    QFormLayout, QLineEdit, QDateEdit, QTextEdit, QComboBox,
    QMessageBox, QHeaderView, QCheckBox, QTabWidget,
    QSplitter, QGroupBox
)
from PyQt5.QtCore import Qt, QDate

from database import get_session, Despesa, Entrada, Fornecedor
import datetime

class FinanceiroTab(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal
        self.layout = QVBoxLayout(self)
        
        # Título
        self.title_label = QLabel("Gestão Financeira")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(self.title_label)
        
        # Splitter para dividir a tela em duas partes (entradas e despesas)
        self.splitter = QSplitter(Qt.Vertical)
        self.layout.addWidget(self.splitter)
        
        # Parte de Entradas
        self.entradas_widget = QWidget()
        self.entradas_layout = QVBoxLayout(self.entradas_widget)
        
        # Título de Entradas
        self.entradas_group = QGroupBox("Entradas")
        self.entradas_group_layout = QVBoxLayout(self.entradas_group)
        
        # Botões de ação para Entradas
        self.entradas_action_layout = QHBoxLayout()
        
        self.add_entrada_button = QPushButton("Adicionar Entrada")
        self.add_entrada_button.clicked.connect(self.add_entrada)
        self.entradas_action_layout.addWidget(self.add_entrada_button)
        
        self.edit_entrada_button = QPushButton("Editar Selecionada")
        self.edit_entrada_button.clicked.connect(self.edit_entrada)
        self.entradas_action_layout.addWidget(self.edit_entrada_button)
        
        self.delete_entrada_button = QPushButton("Excluir Selecionada")
        self.delete_entrada_button.clicked.connect(self.delete_entrada)
        self.entradas_action_layout.addWidget(self.delete_entrada_button)
        
        self.refresh_entrada_button = QPushButton("Atualizar Lista")
        self.refresh_entrada_button.clicked.connect(self.load_entradas)
        self.entradas_action_layout.addWidget(self.refresh_entrada_button)
        
        self.entradas_group_layout.addLayout(self.entradas_action_layout)
        
        # Tabela de entradas
        self.entradas_table = QTableWidget()
        self.entradas_table.setColumnCount(5)
        self.entradas_table.setHorizontalHeaderLabels([
            "Descrição", "Valor (R$)", "Data", "Categoria", "Recebido"
        ])
        self.entradas_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.entradas_group_layout.addWidget(self.entradas_table)
        
        self.entradas_layout.addWidget(self.entradas_group)
        self.splitter.addWidget(self.entradas_widget)
        
        # Parte de Despesas
        self.despesas_widget = QWidget()
        self.despesas_layout = QVBoxLayout(self.despesas_widget)
        
        # Título de Despesas
        self.despesas_group = QGroupBox("Despesas")
        self.despesas_group_layout = QVBoxLayout(self.despesas_group)
        
        # Botões de ação para Despesas
        self.despesas_action_layout = QHBoxLayout()
        
        self.add_despesa_button = QPushButton("Adicionar Despesa")
        self.add_despesa_button.clicked.connect(self.add_despesa)
        self.despesas_action_layout.addWidget(self.add_despesa_button)
        
        self.edit_despesa_button = QPushButton("Editar Selecionada")
        self.edit_despesa_button.clicked.connect(self.edit_despesa)
        self.despesas_action_layout.addWidget(self.edit_despesa_button)
        
        self.delete_despesa_button = QPushButton("Excluir Selecionada")
        self.delete_despesa_button.clicked.connect(self.delete_despesa)
        self.despesas_action_layout.addWidget(self.delete_despesa_button)
        
        self.refresh_despesa_button = QPushButton("Atualizar Lista")
        self.refresh_despesa_button.clicked.connect(self.load_despesas)
        self.despesas_action_layout.addWidget(self.refresh_despesa_button)
        
        self.despesas_group_layout.addLayout(self.despesas_action_layout)
        
        # Tabela de despesas
        self.despesas_table = QTableWidget()
        self.despesas_table.setColumnCount(12)
        self.despesas_table.setHorizontalHeaderLabels([
            "Descrição", "Valor (R$)", "Data", "Fornecedor", "Produto Retirado", "Data de Retirada",
            "Data de Pagamento", "Categoria", "Forma Pagamento", "Pago",
            "Usuário", "Data Adicionado"
        ])
        self.despesas_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.despesas_group_layout.addWidget(self.despesas_table)
        
        self.despesas_layout.addWidget(self.despesas_group)
        self.splitter.addWidget(self.despesas_widget)
        
        # Carregar dados iniciais
        self.load_entradas()
        self.load_despesas()
        
        # Relatórios futuros
        self.setup_relatorios()
    
    def setup_relatorios(self):
        """Configura a área de relatórios financeiros (implementação futura)."""
        relatorios_group = QGroupBox("Resumo Financeiro")
        relatorios_layout = QVBoxLayout(relatorios_group)
        
        # Mensagem de implementação futura
        message_label = QLabel(
            "Os relatórios financeiros detalhados serão implementados em uma versão futura."
        )
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        relatorios_layout.addWidget(message_label)
        
        self.layout.addWidget(relatorios_group)
    
    def load_entradas(self):
        """Carrega as entradas do banco de dados para a tabela."""
        try:
            session = get_session()
            entradas = session.query(Entrada).all()
            
            self.entradas_table.setRowCount(0)  # Limpar tabela
            
            for i, entrada in enumerate(entradas):
                self.entradas_table.insertRow(i)
                self.entradas_table.setItem(i, 0, QTableWidgetItem(entrada.descricao))
                
                valor = f"R$ {float(entrada.valor):.2f}"
                self.entradas_table.setItem(i, 1, QTableWidgetItem(valor))
                
                data = "-"
                if entrada.data:
                    data = entrada.data.strftime("%d/%m/%Y")
                self.entradas_table.setItem(i, 2, QTableWidgetItem(data))
                
                self.entradas_table.setItem(i, 3, QTableWidgetItem(entrada.categoria or ""))
                
                recebido = "Sim" if entrada.recebido else "Não"
                self.entradas_table.setItem(i, 4, QTableWidgetItem(recebido))
            
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar entradas: {str(e)}")
    
    def load_despesas(self):
        """Carrega as despesas do banco de dados para a tabela."""
        try:
            session = get_session()
            despesas = session.query(Despesa).all()
            
            self.despesas_table.setRowCount(0)  # Limpar tabela
            
            for i, despesa in enumerate(despesas):
                self.despesas_table.insertRow(i)
                self.despesas_table.setItem(i, 0, QTableWidgetItem(despesa.descricao))
                
                valor = f"R$ {float(despesa.valor):.2f}"
                self.despesas_table.setItem(i, 1, QTableWidgetItem(valor))
                
                data = "-"
                if despesa.data:
                    data = despesa.data.strftime("%d/%m/%Y")
                self.despesas_table.setItem(i, 2, QTableWidgetItem(data))
                
                # Fornecedor
                self.despesas_table.setItem(i, 3, QTableWidgetItem(despesa.fornecedor or ""))
                
                # Produto Retirado
                produto_retirado = "Sim" if despesa.produto_retirado else "Não"
                self.despesas_table.setItem(i, 4, QTableWidgetItem(produto_retirado))
                
                # Data de retirada
                data_retirada = "-"
                if despesa.data_retirada:
                    data_retirada = despesa.data_retirada.strftime("%d/%m/%Y")
                self.despesas_table.setItem(i, 5, QTableWidgetItem(data_retirada))
                
                # Data de pagamento
                data_pagamento = "-"
                if despesa.data_pagamento:
                    data_pagamento = despesa.data_pagamento.strftime("%d/%m/%Y")
                self.despesas_table.setItem(i, 6, QTableWidgetItem(data_pagamento))
                
                # Categoria e forma de pagamento
                self.despesas_table.setItem(i, 7, QTableWidgetItem(despesa.categoria or ""))
                self.despesas_table.setItem(i, 8, QTableWidgetItem(despesa.forma_pagamento or ""))
                
                # Status de pagamento
                pago = "Sim" if despesa.pago else "Não"
                self.despesas_table.setItem(i, 9, QTableWidgetItem(pago))
                
                # Usuário que adicionou
                self.despesas_table.setItem(i, 10, QTableWidgetItem(despesa.usuario_adicionou or ""))
                
                # Data de adição
                data_adicionou = "-"
                if despesa.data_adicionou:
                    data_adicionou = despesa.data_adicionou.strftime("%d/%m/%Y")
                self.despesas_table.setItem(i, 11, QTableWidgetItem(data_adicionou))
            
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar despesas: {str(e)}")
    
    def add_entrada(self):
        """Abre o diálogo para adicionar uma nova entrada."""
        dialog = EntradaDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.load_entradas()
    
    def edit_entrada(self):
        """Abre o diálogo para editar a entrada selecionada."""
        selected_items = self.entradas_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione uma entrada para editar.")
            return
        
        row = selected_items[0].row()
        
        session = get_session()
        entradas = session.query(Entrada).all()
        
        if row >= len(entradas):
            QMessageBox.warning(self, "Aviso", "Entrada não encontrada.")
            session.close()
            return
        
        entrada = entradas[row]
        
        dialog = EntradaDialog(self, entrada)
        if dialog.exec() == QDialog.Accepted:
            self.load_entradas()
        
        session.close()
    
    def delete_entrada(self):
        """Exclui a entrada selecionada."""
        selected_items = self.entradas_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione uma entrada para excluir.")
            return
        
        row = selected_items[0].row()
        
        confirm = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            "Tem certeza que deseja excluir esta entrada?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                session = get_session()
                entradas = session.query(Entrada).all()
                
                if row < len(entradas):
                    entrada = entradas[row]
                    session.delete(entrada)
                    session.commit()
                    QMessageBox.information(self, "Sucesso", "Entrada excluída com sucesso.")
                    self.load_entradas()
                else:
                    QMessageBox.warning(self, "Aviso", "Entrada não encontrada.")
                
                session.close()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir entrada: {str(e)}")
    
    def add_despesa(self):
        """Abre o diálogo para adicionar uma nova despesa."""
        dialog = DespesaDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.load_despesas()
    
    def edit_despesa(self):
        """Abre o diálogo para editar a despesa selecionada."""
        selected_items = self.despesas_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione uma despesa para editar.")
            return
        
        row = selected_items[0].row()
        
        session = get_session()
        despesas = session.query(Despesa).all()
        
        if row >= len(despesas):
            QMessageBox.warning(self, "Aviso", "Despesa não encontrada.")
            session.close()
            return
        
        despesa = despesas[row]
        
        dialog = DespesaDialog(self, despesa)
        if dialog.exec() == QDialog.Accepted:
            self.load_despesas()
        
        session.close()
    
    def delete_despesa(self):
        """Exclui a despesa selecionada."""
        selected_items = self.despesas_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione uma despesa para excluir.")
            return
        
        row = selected_items[0].row()
        
        confirm = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            "Tem certeza que deseja excluir esta despesa?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                session = get_session()
                despesas = session.query(Despesa).all()
                
                if row < len(despesas):
                    despesa = despesas[row]
                    session.delete(despesa)
                    session.commit()
                    QMessageBox.information(self, "Sucesso", "Despesa excluída com sucesso.")
                    self.load_despesas()
                else:
                    QMessageBox.warning(self, "Aviso", "Despesa não encontrada.")
                
                session.close()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir despesa: {str(e)}")


class DespesaDialog(QDialog):
    """Diálogo para adicionar ou editar despesa."""
    
    def __init__(self, parent=None, despesa=None):
        super().__init__(parent)
        self.despesa = despesa
        self.setup_ui()
        
        if despesa:
            self.setWindowTitle("Editar Despesa")
            self.populate_fields()
        else:
            self.setWindowTitle("Adicionar Despesa")
    
    def setup_ui(self):
        """Configura a interface do diálogo."""
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Formulário
        form_layout = QFormLayout()
        
        # Campos do formulário
        self.descricao_input = QLineEdit()
        form_layout.addRow("Descrição:", self.descricao_input)
        
        self.valor_input = QLineEdit()
        form_layout.addRow("Valor (R$):", self.valor_input)
        
        # Fornecedor como ComboBox com botão Novo Fornecedor
        fornecedor_layout = QHBoxLayout()
        self.fornecedor_input = QComboBox()
        self.fornecedor_input.setEditable(True)
        self.carregar_fornecedores()
        fornecedor_layout.addWidget(self.fornecedor_input)
        
        self.novo_fornecedor_button = QPushButton("Novo Fornecedor")
        self.novo_fornecedor_button.clicked.connect(self.abrir_dialogo_fornecedor)
        fornecedor_layout.addWidget(self.novo_fornecedor_button)
        
        form_layout.addRow("Fornecedor:", fornecedor_layout)
        
        # Checkbox Produto Retirado
        self.produto_retirado_input = QCheckBox("Produto Retirado")
        form_layout.addRow("", self.produto_retirado_input)
        
        # Data normal
        self.data_input = QDateEdit()
        self.data_input.setDisplayFormat("dd/MM/yyyy")
        self.data_input.setCalendarPopup(True)
        self.data_input.setDate(QDate.currentDate())
        form_layout.addRow("Data:", self.data_input)
        
        # Data de retirada
        self.data_retirada_input = QDateEdit()
        self.data_retirada_input.setDisplayFormat("dd/MM/yyyy")
        self.data_retirada_input.setCalendarPopup(True)
        self.data_retirada_input.setDate(QDate.currentDate())
        form_layout.addRow("Data de Retirada:", self.data_retirada_input)
        
        # Data de pagamento
        self.data_pagamento_input = QDateEdit()
        self.data_pagamento_input.setDisplayFormat("dd/MM/yyyy")
        self.data_pagamento_input.setCalendarPopup(True)
        self.data_pagamento_input.setDate(QDate.currentDate())
        form_layout.addRow("Data de Pagamento:", self.data_pagamento_input)
        
        # Usuário que adicionou
        self.usuario_input = QLineEdit()
        form_layout.addRow("Usuário:", self.usuario_input)
        
        self.categoria_input = QComboBox()
        self.categoria_input.addItems([
            "Insumos", "Combustível", "Manutenção", "Salários", 
            "Impostos", "Aluguel", "Serviços", "Outros"
        ])
        self.categoria_input.setEditable(True)
        form_layout.addRow("Categoria:", self.categoria_input)
        
        self.forma_pagamento_input = QComboBox()
        self.forma_pagamento_input.addItems([
            "Dinheiro", "Cartão de Crédito", "Cartão de Débito", 
            "Transferência", "PIX", "Boleto", "Cheque"
        ])
        self.forma_pagamento_input.setEditable(True)
        form_layout.addRow("Forma de Pagamento:", self.forma_pagamento_input)
        
        self.pago_input = QCheckBox("Despesa Paga")
        self.pago_input.setChecked(True)
        form_layout.addRow("", self.pago_input)
        
        self.obs_input = QTextEdit()
        form_layout.addRow("Observações:", self.obs_input)
        
        layout.addLayout(form_layout)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.save_despesa)
        buttons_layout.addWidget(self.save_button)
        
        layout.addLayout(buttons_layout)
    
    def carregar_fornecedores(self):
        """Carrega a lista de fornecedores no ComboBox."""
        try:
            session = get_session()
            fornecedores = session.query(Fornecedor).order_by(Fornecedor.nome).all()
            
            self.fornecedor_input.clear()
            self.fornecedor_input.addItem("")  # Item vazio
            
            for fornecedor in fornecedores:
                self.fornecedor_input.addItem(fornecedor.nome)
                
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar fornecedores: {str(e)}")
    
    def abrir_dialogo_fornecedor(self):
        """Abre o diálogo para adicionar um novo fornecedor."""
        dialog = FornecedorDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.carregar_fornecedores()
            # Selecionar o fornecedor recém-adicionado
            if dialog.fornecedor and dialog.fornecedor.nome:
                index = self.fornecedor_input.findText(dialog.fornecedor.nome)
                if index >= 0:
                    self.fornecedor_input.setCurrentIndex(index)
    
    def populate_fields(self):
        """Preenche os campos com os dados da despesa a ser editada."""
        self.descricao_input.setText(self.despesa.descricao)
        
        if self.despesa.valor:
            self.valor_input.setText(str(float(self.despesa.valor)))
        
        # Fornecedor
        if self.despesa.fornecedor:
            index = self.fornecedor_input.findText(self.despesa.fornecedor)
            if index >= 0:
                self.fornecedor_input.setCurrentIndex(index)
            else:
                self.fornecedor_input.setCurrentText(self.despesa.fornecedor)
        
        # Produto Retirado
        self.produto_retirado_input.setChecked(self.despesa.produto_retirado)
        
        # Data normal
        if self.despesa.data:
            date = QDate.fromString(
                self.despesa.data.strftime("%Y-%m-%d"),
                "yyyy-MM-dd"
            )
            self.data_input.setDate(date)
        
        # Data de retirada
        if self.despesa.data_retirada:
            date_retirada = QDate.fromString(
                self.despesa.data_retirada.strftime("%Y-%m-%d"),
                "yyyy-MM-dd"
            )
            self.data_retirada_input.setDate(date_retirada)
        
        # Data de pagamento
        if self.despesa.data_pagamento:
            date_pagamento = QDate.fromString(
                self.despesa.data_pagamento.strftime("%Y-%m-%d"),
                "yyyy-MM-dd"
            )
            self.data_pagamento_input.setDate(date_pagamento)
        
        # Usuário que adicionou
        if self.despesa.usuario_adicionou:
            self.usuario_input.setText(self.despesa.usuario_adicionou)
        
        if self.despesa.categoria:
            index = self.categoria_input.findText(self.despesa.categoria)
            if index >= 0:
                self.categoria_input.setCurrentIndex(index)
            else:
                self.categoria_input.setCurrentText(self.despesa.categoria)
        
        if self.despesa.forma_pagamento:
            index = self.forma_pagamento_input.findText(self.despesa.forma_pagamento)
            if index >= 0:
                self.forma_pagamento_input.setCurrentIndex(index)
            else:
                self.forma_pagamento_input.setCurrentText(self.despesa.forma_pagamento)
        
        self.pago_input.setChecked(self.despesa.pago)
        self.obs_input.setText(self.despesa.observacoes or "")
    
    def save_despesa(self):
        """Salva a despesa no banco de dados."""
        # Validar campos obrigatórios
        if not self.descricao_input.text().strip():
            QMessageBox.warning(self, "Aviso", "A descrição da despesa é obrigatória.")
            return
        
        if not self.valor_input.text().strip():
            QMessageBox.warning(self, "Aviso", "O valor da despesa é obrigatório.")
            return
        
        try:
            valor = float(self.valor_input.text().strip())
            if valor <= 0:
                QMessageBox.warning(self, "Aviso", "O valor da despesa deve ser maior que zero.")
                return
        except ValueError:
            QMessageBox.warning(self, "Aviso", "O valor da despesa deve ser um número válido.")
            return
        
        try:
            session = get_session()
            
            # Criar ou atualizar despesa
            if not self.despesa:
                self.despesa = Despesa()
                session.add(self.despesa)
                # Para novas despesas, definir a data de adição atual
                self.despesa.data_adicionou = datetime.datetime.now().date()
            
            # Atualizar dados
            self.despesa.descricao = self.descricao_input.text().strip()
            self.despesa.valor = float(self.valor_input.text().strip())
            self.despesa.data = self.data_input.date().toPython()
            
            # Novas colunas
            self.despesa.fornecedor = self.fornecedor_input.currentText().strip()
            self.despesa.produto_retirado = self.produto_retirado_input.isChecked()
            self.despesa.data_retirada = self.data_retirada_input.date().toPython()
            self.despesa.data_pagamento = self.data_pagamento_input.date().toPython()
            self.despesa.usuario_adicionou = self.usuario_input.text().strip()
            
            self.despesa.categoria = self.categoria_input.currentText()
            self.despesa.forma_pagamento = self.forma_pagamento_input.currentText()
            self.despesa.pago = self.pago_input.isChecked()
            self.despesa.observacoes = self.obs_input.toPlainText().strip()
            
            # Commit
            session.commit()
            
            # Fechar diálogo
            self.accept()
            
            QMessageBox.information(
                self,
                "Sucesso",
                "Despesa salva com sucesso!"
            )
            
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar despesa: {str(e)}")
            session.rollback()
            session.close()


class EntradaDialog(QDialog):
    """Diálogo para adicionar ou editar entrada."""
    
    def __init__(self, parent=None, entrada=None):
        super().__init__(parent)
        self.entrada = entrada
        self.setup_ui()
        
        if entrada:
            self.setWindowTitle("Editar Entrada")
            self.populate_fields()
        else:
            self.setWindowTitle("Adicionar Entrada")
    
    def setup_ui(self):
        """Configura a interface do diálogo."""
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Formulário
        form_layout = QFormLayout()
        
        # Campos do formulário
        self.descricao_input = QLineEdit()
        form_layout.addRow("Descrição:", self.descricao_input)
        
        self.valor_input = QLineEdit()
        form_layout.addRow("Valor (R$):", self.valor_input)
        
        self.data_input = QDateEdit()
        self.data_input.setDisplayFormat("dd/MM/yyyy")
        self.data_input.setCalendarPopup(True)
        self.data_input.setDate(QDate.currentDate())
        form_layout.addRow("Data:", self.data_input)
        
        self.categoria_input = QComboBox()
        self.categoria_input.addItems([
            "Venda de Produção", "Prestação de Serviços", "Aluguel", 
            "Subsídios", "Outros"
        ])
        self.categoria_input.setEditable(True)
        form_layout.addRow("Categoria:", self.categoria_input)
        
        self.cliente_input = QLineEdit()
        form_layout.addRow("Cliente:", self.cliente_input)
        
        self.recebido_input = QCheckBox("Valor Recebido")
        self.recebido_input.setChecked(True)
        form_layout.addRow("", self.recebido_input)
        
        self.obs_input = QTextEdit()
        form_layout.addRow("Observações:", self.obs_input)
        
        layout.addLayout(form_layout)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.save_entrada)
        buttons_layout.addWidget(self.save_button)
        
        layout.addLayout(buttons_layout)
    
    def populate_fields(self):
        """Preenche os campos com os dados da entrada a ser editada."""
        self.descricao_input.setText(self.entrada.descricao)
        
        if self.entrada.valor:
            self.valor_input.setText(str(float(self.entrada.valor)))
        
        if self.entrada.data:
            date = QDate.fromString(
                self.entrada.data.strftime("%Y-%m-%d"),
                "yyyy-MM-dd"
            )
            self.data_input.setDate(date)
        
        if self.entrada.categoria:
            index = self.categoria_input.findText(self.entrada.categoria)
            if index >= 0:
                self.categoria_input.setCurrentIndex(index)
            else:
                self.categoria_input.setCurrentText(self.entrada.categoria)
        
        self.cliente_input.setText(self.entrada.cliente or "")
        self.recebido_input.setChecked(self.entrada.recebido)
        self.obs_input.setText(self.entrada.observacoes or "")
    
    def save_entrada(self):
        """Salva a entrada no banco de dados."""
        # Validar campos obrigatórios
        if not self.descricao_input.text().strip():
            QMessageBox.warning(self, "Aviso", "A descrição da entrada é obrigatória.")
            return
        
        if not self.valor_input.text().strip():
            QMessageBox.warning(self, "Aviso", "O valor da entrada é obrigatório.")
            return
        
        try:
            valor = float(self.valor_input.text().strip())
            if valor <= 0:
                QMessageBox.warning(self, "Aviso", "O valor da entrada deve ser maior que zero.")
                return
        except ValueError:
            QMessageBox.warning(self, "Aviso", "O valor da entrada deve ser um número válido.")
            return
        
        try:
            session = get_session()
            
            # Criar ou atualizar entrada
            if not self.entrada:
                self.entrada = Entrada()
                session.add(self.entrada)
            
            # Atualizar dados
            self.entrada.descricao = self.descricao_input.text().strip()
            self.entrada.valor = float(self.valor_input.text().strip())
            self.entrada.data = self.data_input.date().toPython()
            self.entrada.categoria = self.categoria_input.currentText()
            self.entrada.cliente = self.cliente_input.text().strip()
            self.entrada.recebido = self.recebido_input.isChecked()
            self.entrada.observacoes = self.obs_input.toPlainText().strip()
            
            # Commit
            session.commit()
            
            # Fechar diálogo
            self.accept()
            
            QMessageBox.information(
                self,
                "Sucesso",
                "Entrada salva com sucesso!"
            )
            
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar entrada: {str(e)}")
            session.rollback()
            session.close()


class FornecedorDialog(QDialog):
    """Diálogo para adicionar um novo fornecedor."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fornecedor = None
        self.setup_ui()
        self.setWindowTitle("Novo Fornecedor")
    
    def setup_ui(self):
        """Configura a interface do diálogo."""
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Formulário
        form_layout = QFormLayout()
        
        # Campos do formulário
        self.nome_input = QLineEdit()
        form_layout.addRow("Nome:", self.nome_input)
        
        self.telefone_input = QLineEdit()
        form_layout.addRow("Telefone:", self.telefone_input)
        
        self.email_input = QLineEdit()
        form_layout.addRow("E-mail:", self.email_input)
        
        self.cnpj_input = QLineEdit()
        form_layout.addRow("CNPJ:", self.cnpj_input)
        
        self.endereco_input = QTextEdit()
        self.endereco_input.setMaximumHeight(80)
        form_layout.addRow("Endereço:", self.endereco_input)
        
        self.obs_input = QTextEdit()
        self.obs_input.setMaximumHeight(80)
        form_layout.addRow("Observações:", self.obs_input)
        
        layout.addLayout(form_layout)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.save_fornecedor)
        buttons_layout.addWidget(self.save_button)
        
        layout.addLayout(buttons_layout)
    
    def save_fornecedor(self):
        """Salva o fornecedor no banco de dados."""
        # Validar campos obrigatórios
        if not self.nome_input.text().strip():
            QMessageBox.warning(self, "Aviso", "O nome do fornecedor é obrigatório.")
            return
        
        try:
            session = get_session()
            
            # Verificar se já existe um fornecedor com o mesmo nome
            nome = self.nome_input.text().strip()
            existing = session.query(Fornecedor).filter(Fornecedor.nome == nome).first()
            
            if existing:
                QMessageBox.warning(
                    self, 
                    "Aviso", 
                    f"Já existe um fornecedor com o nome '{nome}'."
                )
                session.close()
                return
            
            # Criar novo fornecedor
            self.fornecedor = Fornecedor()
            session.add(self.fornecedor)
            
            # Atualizar dados
            self.fornecedor.nome = nome
            self.fornecedor.telefone = self.telefone_input.text().strip()
            self.fornecedor.email = self.email_input.text().strip()
            self.fornecedor.cnpj = self.cnpj_input.text().strip()
            self.fornecedor.endereco = self.endereco_input.toPlainText().strip()
            self.fornecedor.observacoes = self.obs_input.toPlainText().strip()
            self.fornecedor.data_cadastro = datetime.datetime.now().date()
            
            # Commit
            session.commit()
            
            # Fechar diálogo
            self.accept()
            
            QMessageBox.information(
                self,
                "Sucesso",
                "Fornecedor cadastrado com sucesso!"
            )
            
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar fornecedor: {str(e)}")
            session.rollback()
            session.close() 