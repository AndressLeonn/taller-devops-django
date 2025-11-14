import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QHeaderView)

class ClienteUsuarios(QWidget):
	def __init__(self):
		super().__init__()
		self.api_url = "http://192.168.58.2:30007/api/usuarios/"

		self.init_ui()
		self.cargar_usuarios()

	def init_ui(self):
		self.setWindowTitle("Gestión de Usuarios - Cliente Desktop")
		self.setGeometry(100, 100, 600, 400)
        
		layout = QVBoxLayout()

        # --- Formulario de Entrada ---
		form_layout = QHBoxLayout()
        
		self.input_codigo = QLineEdit()
		self.input_codigo.setPlaceholderText("Código (ID)")
		form_layout.addWidget(self.input_codigo)
	        
		self.input_nombre = QLineEdit()
		self.input_nombre.setPlaceholderText("Nombre Completo")
		form_layout.addWidget(self.input_nombre)
        
		btn_agregar = QPushButton("Agregar Usuario")
		btn_agregar.clicked.connect(self.agregar_usuario)
		btn_agregar.setStyleSheet("background-color: #4CAF50; color: white;")
		form_layout.addWidget(btn_agregar)
        
		layout.addLayout(form_layout)

        # --- Tabla de Usuarios ---
		self.tabla = QTableWidget()
		self.tabla.setColumnCount(3)
		self.tabla.setHorizontalHeaderLabels(["Código", "Nombre", "Acciones"])
		self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		layout.addWidget(self.tabla)

        # --- Botón de Actualizar ---
		btn_actualizar = QPushButton("Refrescar Lista")
		btn_actualizar.clicked.connect(self.cargar_usuarios)
		layout.addWidget(btn_actualizar)

		self.setLayout(layout)

	def cargar_usuarios(self):
		try:
			response = requests.get(self.api_url)
			if response.status_code == 200:
				usuarios = response.json()
				self.tabla.setRowCount(0)
				for row, usuario in enumerate(usuarios):
					self.tabla.insertRow(row)
					self.tabla.setItem(row, 0, QTableWidgetItem(str(usuario['codigo'])))
					self.tabla.setItem(row, 1, QTableWidgetItem(usuario['nombre']))
                    
                    # Botón de eliminar por fila
					btn_eliminar = QPushButton("Eliminar")
					btn_eliminar.clicked.connect(lambda _, c=usuario['codigo']: self.eliminar_usuario(c))
					self.tabla.setCellWidget(row, 2, btn_eliminar)
			else:
				QMessageBox.warning(self, "Error", "No se pudo conectar con el servidor")
		except Exception as e:
			QMessageBox.critical(self, "Error de Conexión", f"Asegúrate que el servidor Django esté corriendo.\n{str(e)}")

	def agregar_usuario(self):
		codigo = self.input_codigo.text()
		nombre = self.input_nombre.text()
        
		if codigo and nombre:
			data = {"codigo": codigo, "nombre": nombre}
			try:
				response = requests.post(self.api_url, json=data)
				if response.status_code == 201:
					self.input_codigo.clear()
					self.input_nombre.clear()
					self.cargar_usuarios()
				else:
					QMessageBox.warning(self, "Error", f"Error al crear: {response.text}")
			except Exception as e:
				QMessageBox.critical(self, "Error", str(e))
		else:
			QMessageBox.warning(self, "Alerta", "Completa todos los campos")

	def eliminar_usuario(self, codigo):
		try:
			url_delete = f"{self.api_url}{codigo}/"
			response = requests.delete(url_delete)
			if response.status_code == 204:
				self.cargar_usuarios()
			else:
				QMessageBox.warning(self, "Error", "No se pudo eliminar el usuario")
		except Exception as e:
			QMessageBox.critical(self, "Error", str(e))

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = ClienteUsuarios()
	ex.show()
	sys.exit(app.exec_())
