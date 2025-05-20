from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QLabel, QDialog,
    QFormLayout, QLineEdit, QDateEdit, QTextEdit, QComboBox,
    QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt, QDate

from database import get_session, Producao

class ProducaoTab(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal
        self.layout = QVBoxLayout(self)
        
        # Título
        self.title_label = QLabel("Gerenciamento de Produção")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(self.title_label)
        
        # Botões de ação
        self.action_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Adicionar Produção")
        self.add_button.clicked.connect(self.add_producao)
        self.action_layout.addWidget(self.add_button)
        
        self.delete_button = QPushButton("Excluir Selecionada")
        self.delete_button.clicked.connect(self.delete_producao)
        self.action_layout.addWidget(self.delete_button)
        
        self.refresh_button = QPushButton("Atualizar Lista")
        self.refresh_button.clicked.connect(self.load_producoes)
        self.action_layout.addWidget(self.refresh_button)
        
        self.layout.addLayout(self.action_layout)
        
        # Tabela de produções
        self.table = QTableWidget()
        self.table.setColumnCount(8)  # Aumentado para incluir coluna do botão Editar
        self.table.setHorizontalHeaderLabels([
            "Produto", "Quantidade", "Unidade", "Data Início", 
            "Data Fim", "Área (ha)", "Custo Total (R$)", "Ações"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Definir largura da coluna de ações
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.layout.addWidget(self.table)
        
        # Carregar dados iniciais
        self.load_producoes()
        
        # Dicionário para armazenar os botões de editar
        self.edit_buttons = {}
    
    def load_producoes(self):
        """Carrega as produções do banco de dados para a tabela."""
        try:
            session = get_session()
            producoes = session.query(Producao).all()
            
            self.table.setRowCount(0)  # Limpar tabela
            self.edit_buttons = {}  # Limpar referências de botões
            
            for i, producao in enumerate(producoes):
                self.table.insertRow(i)
                self.table.setItem(i, 0, QTableWidgetItem(producao.produto))
                
                # Formatação de quantidade com separador de milhar
                quantidade = f"{producao.quantidade:,.2f}".replace(".", "X").replace(",", ".").replace("X", ",")
                self.table.setItem(i, 1, QTableWidgetItem(quantidade))
                
                self.table.setItem(i, 2, QTableWidgetItem(producao.unidade or ""))
                
                data_inicio = "-"
                if producao.data_inicio:
                    data_inicio = producao.data_inicio.strftime("%d/%m/%Y")
                self.table.setItem(i, 3, QTableWidgetItem(data_inicio))
                
                data_fim = "-"
                if producao.data_fim:
                    data_fim = producao.data_fim.strftime("%d/%m/%Y")
                self.table.setItem(i, 4, QTableWidgetItem(data_fim))
                
                area = "-"
                if producao.area:
                    # Formatação com separador de milhar
                    area = f"{producao.area:,.2f}".replace(".", "X").replace(",", ".").replace("X", ",")
                self.table.setItem(i, 5, QTableWidgetItem(area))
                
                custo = "-"
                if producao.custo_total:
                    # Formatação com separador de milhar
                    custo = f"R$ {float(producao.custo_total):,.2f}".replace(".", "X").replace(",", ".").replace("X", ",")
                self.table.setItem(i, 6, QTableWidgetItem(custo))
                
                # Adiciona botão editar na última coluna
                edit_btn = QPushButton("Editar")
                edit_btn.setMaximumWidth(60)  # Reduz largura do botão
                edit_btn.setStyleSheet("font-size: 10px;")  # Reduz tamanho da fonte
                
                # Conectar o botão à edição do registro específico
                edit_btn.clicked.connect(lambda checked, row=i: self.edit_producao_from_button(row))
                
                # Armazenar referência ao botão para evitar coleta de lixo
                self.edit_buttons[i] = edit_btn
                
                # Adicionar à tabela
                self.table.setCellWidget(i, 7, edit_btn)
            
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar produções: {str(e)}")
    
    def edit_producao_from_button(self, row):
        """Edita a produção na linha especificada pelo botão."""
        session = get_session()
        producoes = session.query(Producao).all()
        
        if row >= len(producoes):
            QMessageBox.warning(self, "Aviso", "Produção não encontrada.")
            session.close()
            return
        
        producao = producoes[row]
        
        dialog = ProducaoDialog(self, producao)
        if dialog.exec() == QDialog.Accepted:
            self.load_producoes()
        
        session.close()
    
    def add_producao(self):
        """Abre o diálogo para adicionar uma nova produção."""
        dialog = ProducaoDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.load_producoes()
    
    def edit_producao(self):
        """Abre o diálogo para editar a produção selecionada."""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione uma produção para editar.")
            return
        
        row = selected_items[0].row()
        
        session = get_session()
        producoes = session.query(Producao).all()
        
        if row >= len(producoes):
            QMessageBox.warning(self, "Aviso", "Produção não encontrada.")
            session.close()
            return
        
        producao = producoes[row]
        
        dialog = ProducaoDialog(self, producao)
        if dialog.exec() == QDialog.Accepted:
            self.load_producoes()
        
        session.close()
    
    def delete_producao(self):
        """Exclui a produção selecionada."""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione uma produção para excluir.")
            return
        
        row = selected_items[0].row()
        
        confirm = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            "Tem certeza que deseja excluir esta produção?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                session = get_session()
                producoes = session.query(Producao).all()
                
                if row < len(producoes):
                    producao = producoes[row]
                    session.delete(producao)
                    session.commit()
                    QMessageBox.information(self, "Sucesso", "Produção excluída com sucesso.")
                    self.load_producoes()
                else:
                    QMessageBox.warning(self, "Aviso", "Produção não encontrada.")
                
                session.close()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir produção: {str(e)}")


class ProducaoDialog(QDialog):
    """Diálogo para adicionar ou editar produção."""
    
    def __init__(self, parent=None, producao=None):
        super().__init__(parent)
        self.producao = producao
        self.setup_ui()
        
        if producao:
            self.setWindowTitle("Editar Produção")
            self.populate_fields()
        else:
            self.setWindowTitle("Adicionar Produção")
    
    def setup_ui(self):
        """Configura a interface do diálogo."""
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Formulário
        form_layout = QFormLayout()
        
        # Campos do formulário
        # Produto com botão Editar
        produto_layout = QHBoxLayout()
        self.produto_input = QComboBox()
        self.produto_input.addItems([
            "Soja", "Milho", "Trigo", "Feijão", "Algodão", 
            "Café", "Cana-de-açúcar", "Outro"
        ])
        self.produto_input.setEditable(True)
        produto_layout.addWidget(self.produto_input)
        
        self.editar_produto_button = QPushButton("Editar")
        # self.editar_produto_button.clicked.connect(self.editar_produtos)
        produto_layout.addWidget(self.editar_produto_button)
        
        form_layout.addRow("Produto:", produto_layout)
        
        self.quantidade_input = QLineEdit()
        form_layout.addRow("Quantidade:", self.quantidade_input)
        
        # Unidade com botão Editar
        unidade_layout = QHBoxLayout()
        self.unidade_input = QComboBox()
        self.unidade_input.addItems([
            "kg", "ton", "sacos", "fardos", "litros", "unidades"
        ])
        self.unidade_input.setEditable(True)
        unidade_layout.addWidget(self.unidade_input)
        
        self.editar_unidade_button = QPushButton("Editar")
        # self.editar_unidade_button.clicked.connect(self.editar_unidades)
        unidade_layout.addWidget(self.editar_unidade_button)
        
        form_layout.addRow("Unidade:", unidade_layout)
        
        self.data_inicio_input = QDateEdit()
        self.data_inicio_input.setDisplayFormat("dd/MM/yyyy")
        self.data_inicio_input.setCalendarPopup(True)
        self.data_inicio_input.setDate(QDate.currentDate())
        form_layout.addRow("Data de Início:", self.data_inicio_input)
        
        self.data_fim_input = QDateEdit()
        self.data_fim_input.setDisplayFormat("dd/MM/yyyy")
        self.data_fim_input.setCalendarPopup(True)
        self.data_fim_input.setDate(QDate.currentDate().addDays(90))  # Default: 3 meses depois
        form_layout.addRow("Data de Fim:", self.data_fim_input)
        
        self.area_input = QLineEdit()
        form_layout.addRow("Área (hectares):", self.area_input)
        
        self.custo_input = QLineEdit()
        form_layout.addRow("Custo Total (R$):", self.custo_input)
        
        self.valor_venda_input = QLineEdit()
        form_layout.addRow("Valor de Venda (R$):", self.valor_venda_input)
        
        self.obs_input = QTextEdit()
        form_layout.addRow("Observações:", self.obs_input)
        
        layout.addLayout(form_layout)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.save_producao)
        buttons_layout.addWidget(self.save_button)
        
        layout.addLayout(buttons_layout)
    
    def populate_fields(self):
        """Preenche os campos com os dados da produção a ser editada."""
        if self.producao.produto:
            index = self.produto_input.findText(self.producao.produto)
            if index >= 0:
                self.produto_input.setCurrentIndex(index)
            else:
                self.produto_input.setCurrentText(self.producao.produto)
        
        if self.producao.quantidade:
            # Formatação com separador de milhar
            quantidade_formatada = f"{self.producao.quantidade:,.2f}".replace(".", "X").replace(",", ".").replace("X", ",")
            self.quantidade_input.setText(quantidade_formatada)
        
        if self.producao.unidade:
            index = self.unidade_input.findText(self.producao.unidade)
            if index >= 0:
                self.unidade_input.setCurrentIndex(index)
            else:
                self.unidade_input.setCurrentText(self.producao.unidade)
        
        if self.producao.data_inicio:
            date = QDate.fromString(
                self.producao.data_inicio.strftime("%Y-%m-%d"),
                "yyyy-MM-dd"
            )
            self.data_inicio_input.setDate(date)
        
        if self.producao.data_fim:
            date = QDate.fromString(
                self.producao.data_fim.strftime("%Y-%m-%d"),
                "yyyy-MM-dd"
            )
            self.data_fim_input.setDate(date)
        
        if self.producao.area:
            # Formatação com separador de milhar
            area_formatada = f"{self.producao.area:,.2f}".replace(".", "X").replace(",", ".").replace("X", ",")
            self.area_input.setText(area_formatada)
        
        if self.producao.custo_total:
            # Formatação com separador de milhar
            custo_formatado = f"{float(self.producao.custo_total):,.2f}".replace(".", "X").replace(",", ".").replace("X", ",")
            self.custo_input.setText(custo_formatado)
        
        if self.producao.valor_venda:
            # Formatação com separador de milhar
            valor_venda_formatado = f"{float(self.producao.valor_venda):,.2f}".replace(".", "X").replace(",", ".").replace("X", ",")
            self.valor_venda_input.setText(valor_venda_formatado)
        
        self.obs_input.setText(self.producao.observacoes or "")
    
    def save_producao(self):
        """Salva a produção no banco de dados."""
        # Validar campos obrigatórios
        if not self.produto_input.currentText().strip():
            QMessageBox.warning(self, "Aviso", "O produto é obrigatório.")
            return
        
        if not self.quantidade_input.text().strip():
            QMessageBox.warning(self, "Aviso", "A quantidade é obrigatória.")
            return
        
        try:
            # Remover possíveis separadores de milhar e trocar vírgula por ponto
            quantidade_texto = self.quantidade_input.text().strip().replace(".", "").replace(",", ".")
            quantidade = float(quantidade_texto)
            if quantidade <= 0:
                QMessageBox.warning(self, "Aviso", "A quantidade deve ser maior que zero.")
                return
        except ValueError:
            QMessageBox.warning(self, "Aviso", "A quantidade deve ser um número válido.")
            return
        
        try:
            session = get_session()
            
            # Criar ou atualizar produção
            if not self.producao:
                self.producao = Producao()
                session.add(self.producao)
            
            # Atualizar dados
            self.producao.produto = self.produto_input.currentText().strip()
            self.producao.quantidade = quantidade
            self.producao.unidade = self.unidade_input.currentText().strip()
            self.producao.data_inicio = self.data_inicio_input.date().toPyDate()
            self.producao.data_fim = self.data_fim_input.date().toPyDate()
            
            if self.area_input.text().strip():
                area_texto = self.area_input.text().strip().replace(".", "").replace(",", ".")
                self.producao.area = float(area_texto)
            else:
                self.producao.area = None
            
            if self.custo_input.text().strip():
                custo_texto = self.custo_input.text().strip().replace(".", "").replace(",", ".")
                self.producao.custo_total = float(custo_texto)
            else:
                self.producao.custo_total = None
            
            if self.valor_venda_input.text().strip():
                valor_venda_texto = self.valor_venda_input.text().strip().replace(".", "").replace(",", ".")
                self.producao.valor_venda = float(valor_venda_texto)
            else:
                self.producao.valor_venda = None
            
            self.producao.observacoes = self.obs_input.toPlainText().strip()
            
            # Commit
            session.commit()
            
            # Fechar diálogo
            self.accept()
            
            QMessageBox.information(
                self,
                "Sucesso",
                "Produção salva com sucesso!"
            )
            
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar produção: {str(e)}")
            session.rollback()
            session.close() 