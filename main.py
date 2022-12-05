import sys
import serial.tools.list_ports
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
from Ui_ykazka import Ui_Ykazka

class AppPult(QMainWindow, Ui_Ykazka):
    
    sensitivity: int = 1
    """min 1, max 100"""
    
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # привязка событий
        self.sensitivitySlider.valueChanged.connect(self.sensitivity_set)
        
        self.applyBtn.clicked.connect(self.apply_btn_clicked)
        
        self.connectBtn.clicked.connect(self.connect_btn_clicked)

        self.comPortsList.view().pressed.connect(self.apply_btn_clicked)

        self.comPortsList.mousePressEvent = self.com_ports_update
        
        self.add_com_ports()


    # события
    def sensitivity_set(self, value):
        self.sensitivity = value
        self.SensitivityValue.setText(f"{self.sensitivity}%")
        

    def com_ports_update(self, v):
        print(v)


    def connect_btn_clicked(self):
        pass


    def apply_btn_clicked(self, *args):
        self.outputText.append("OK")

        
        
        
        

        


def main():
    app = QApplication(sys.argv)
    
    mainWindow = AppPult()

    mainWindow.show()
    
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()

