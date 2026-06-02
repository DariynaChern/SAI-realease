from PyQt5.QtWidgets import QApplication
from ui_role_select import RoleSelectWindow
import sys

app = QApplication(sys.argv)

window = RoleSelectWindow()
window.show()

sys.exit(app.exec_())
