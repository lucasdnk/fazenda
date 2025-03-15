import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
import requests
from datetime import datetime
from config import config

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, token):
        super(MainWindow, self).__init__()
        # Carrega o arquivo UI
        uic.loadUi('main_window.ui', self)
        
        self.token = token
        self.api_url = f'http://{config.API_HOST}:{config.API_PORT}'
        
        # Conectar botões aos métodos
        self.btn_add_farm.clicked.connect(self.add_farm)
        self.btn_refresh_farms.clicked.connect(self.load_farms)
        self.btn_add_field.clicked.connect(self.add_field)
        self.btn_refresh_fields.clicked.connect(self.load_fields)
        
        # Carregar dados iniciais
        self.load_farms()

    def show_error(self, message):
        QMessageBox.critical(self, "Erro", message)
        
    def load_farms(self):
        try:
            headers = {'Authorization': f'Bearer {self.token}'}
            response = requests.get(f"{self.api_url}/farms", headers=headers)
            farms = response.json()
            
            self.table_farms.setRowCount(0)
            for farm in farms:
                row = self.table_farms.rowCount()
                self.table_farms.insertRow(row)
                self.table_farms.setItem(row, 0, QtWidgets.QTableWidgetItem(farm['id']))
                self.table_farms.setItem(row, 1, QtWidgets.QTableWidgetItem(farm['name']))
                self.table_farms.setItem(row, 2, QtWidgets.QTableWidgetItem(farm['location']))
                
            # Atualizar combobox de fazendas
            self.combo_farm_fields.clear()
            for farm in farms:
                self.combo_farm_fields.addItem(farm['name'], farm['id'])
                
        except Exception as e:
            self.show_error(f"Erro ao carregar fazendas: {str(e)}")

    def load_fields(self):
        try:
            farm_id = self.combo_farm_fields.currentData()
            if not farm_id:
                return
                
            headers = {'Authorization': f'Bearer {self.token}'}
            response = requests.get(f"{self.api_url}/farms/{farm_id}/fields", headers=headers)
            fields = response.json()
            
            self.table_fields.setRowCount(0)
            for field in fields:
                row = self.table_fields.rowCount()
                self.table_fields.insertRow(row)
                self.table_fields.setItem(row, 0, QtWidgets.QTableWidgetItem(field['id']))
                self.table_fields.setItem(row, 1, QtWidgets.QTableWidgetItem(field['name']))
                self.table_fields.setItem(row, 2, QtWidgets.QTableWidgetItem(str(field['area'])))
                
        except Exception as e:
            self.show_error(f"Erro ao carregar talhões: {str(e)}")

    def add_farm(self):
        name, ok = QtWidgets.QInputDialog.getText(self, 'Nova Fazenda', 'Nome da Fazenda:')
        if ok and name:
            location, ok = QtWidgets.QInputDialog.getText(self, 'Nova Fazenda', 'Localização:')
            if ok and location:
                try:
                    headers = {'Authorization': f'Bearer {self.token}'}
                    response = requests.post(f"{self.api_url}/farms", 
                                          json={'name': name, 'location': location},
                                          headers=headers)
                    if response.status_code == 201:
                        self.load_farms()
                    else:
                        self.show_error("Erro ao criar fazenda")
                except Exception as e:
                    self.show_error(f"Erro ao criar fazenda: {str(e)}")

    def add_field(self):
        farm_id = self.combo_farm_fields.currentData()
        if not farm_id:
            self.show_error("Selecione uma fazenda primeiro")
            return
            
        name, ok = QtWidgets.QInputDialog.getText(self, 'Novo Talhão', 'Nome do Talhão:')
        if ok and name:
            area, ok = QtWidgets.QInputDialog.getDouble(self, 'Novo Talhão', 'Área (ha):', 0, 0, 10000, 2)
            if ok:
                try:
                    headers = {'Authorization': f'Bearer {self.token}'}
                    response = requests.post(f"{self.api_url}/fields", 
                                          json={'farm_id': farm_id, 'name': name, 'area': area},
                                          headers=headers)
                    if response.status_code == 201:
                        self.load_fields()
                    else:
                        self.show_error("Erro ao criar talhão")
                except Exception as e:
                    self.show_error(f"Erro ao criar talhão: {str(e)}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 