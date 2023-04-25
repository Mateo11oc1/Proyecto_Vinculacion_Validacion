import sys

from PyQt6.QtWidgets import QApplication

from controlador.CtrlReporteErrores import Controlador

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controlPrincipal = Controlador()
    sys.exit(app.exec())