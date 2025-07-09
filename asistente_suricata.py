import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QLineEdit,
    QPushButton, QVBoxLayout, QScrollArea, QMessageBox, QFormLayout
)
from PyQt5.QtCore import Qt

RUTA_REGLAS = "/etc/suricata/rules/my.rules"

class ReglaSuricata(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Constructor de Reglas - Chamorro Juan")
        self.setGeometry(100, 100, 500, 600)
        self.init_ui()

    def init_ui(self):
        layout_principal = QVBoxLayout()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        contenedor = QWidget()
        formulario = QFormLayout()

        self.accion_cb = QComboBox()
        self.accion_cb.addItems(["alert", "drop", "reject"])
        formulario.addRow("Acción:", self.accion_cb)

        self.protocolo_cb = QComboBox()
        self.protocolo_cb.addItems(["tcp", "udp", "icmp", "ip"])
        formulario.addRow("Protocolo:", self.protocolo_cb)

        self.ip_origen = QLineEdit("any")
        formulario.addRow("IP Origen:", self.ip_origen)

        self.puerto_origen = QLineEdit("any")
        formulario.addRow("Puerto Origen:", self.puerto_origen)

        self.direccion_cb = QComboBox()
        self.direccion_cb.addItems(["->", "<-", "<->"])
        formulario.addRow("Dirección:", self.direccion_cb)

        self.ip_destino = QLineEdit("any")
        formulario.addRow("IP Destino:", self.ip_destino)

        self.puerto_destino = QLineEdit("80")
        formulario.addRow("Puerto Destino:", self.puerto_destino)

        self.msg = QLineEdit("Posible ataque")
        formulario.addRow('Mensaje (msg):', self.msg)

        self.sid = QLineEdit("1000001")
        formulario.addRow('SID:', self.sid)

        self.rev = QLineEdit("1")
        formulario.addRow('Revisión (rev):', self.rev)

        self.otras_opciones = QLineEdit('')
        formulario.addRow("Otras opciones:", self.otras_opciones)

        self.btn_guardar = QPushButton("Guardar Regla")
        self.btn_guardar.clicked.connect(self.guardar_regla)
        formulario.addRow(self.btn_guardar)

        contenedor.setLayout(formulario)
        scroll.setWidget(contenedor)
        layout_principal.addWidget(scroll)
        self.setLayout(layout_principal)

    def guardar_regla(self):
        try:
            accion = self.accion_cb.currentText()
            protocolo = self.protocolo_cb.currentText()
            ip_src = self.ip_origen.text().strip()
            port_src = self.puerto_origen.text().strip()
            direccion = self.direccion_cb.currentText()
            ip_dst = self.ip_destino.text().strip()
            port_dst = self.puerto_destino.text().strip()

            msg = self.msg.text().strip()
            sid = self.sid.text().strip()
            rev = self.rev.text().strip()
            otras = self.otras_opciones.text().strip().rstrip(";")

            if not msg or not sid or not rev:
                QMessageBox.warning(self, "Error", "Los campos msg, sid y rev son obligatorios.")
                return

            opciones = f'msg:"{msg}"; sid:{sid}; rev:{rev};'
            if otras:
                opciones += f' {otras};'

            regla = f"{accion} {protocolo} {ip_src} {port_src} {direccion} {ip_dst} {port_dst} ({opciones})"

            with open(RUTA_REGLAS, "a") as f:
                f.write(regla + "\n")

            QMessageBox.information(self, "Éxito", f"Regla guardada:\n{regla}")

            reiniciar = QMessageBox.question(
                self,
                "Reiniciar Suricata",
                "¿Deseás reiniciar Suricata para aplicar la nueva regla?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reiniciar == QMessageBox.Yes:
                try:
                    subprocess.Popen(
                        ["sudo", "-n", "/usr/sbin/service", "suricata", "restart"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                except Exception:
                    pass 

            self.close()
            QApplication.quit()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ReglaSuricata()
    ventana.show()
    sys.exit(app.exec_())

