from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from ip import Ipv4NetworkCalc


Form, Window = uic.loadUiType("telaip.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
app.exec()