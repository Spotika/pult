# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_ykazka import Ui_Ykazka

import sys



class App(QMainWindow, Ui_Ykazka):
    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
        



def main():
    app = QApplication(sys.argv)
    
    mainWindow = App()
    
    mainWindow.show()
    
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()

# def main():
#     app = QApplication(sys.argv)
    
#     window = QMainWindow()    
    
    
#     window.setWindowTitle("test title")
#     window.setGeometry(0, 400, 500, 500)
    
#     window.show()
    
#     sys.exit(app.exec_())
    
# if __name__ == "__main__":
#     main()