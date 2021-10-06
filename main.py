from PyQt5 import QtWidgets # import PyQt5 widgets
import sys
from login_win import Ui_MainWindow

# Create the application object
if __name__ == "__main__":
    app = QtWidgets(sys.argv)
    widget = Ui_MainWindow()
    widget.show()
    sys.exit(app.exec_())