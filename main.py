import sys
import serial.tools.list_ports

from PyQt5.QtCore import QSize, QTimer

from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5 import QtWidgets

from Ui_ykazka import Ui_Ykazka

import mouse
# import pyautogui as pag
# pag.PAUSE = 0.01
# pag.FAILSAFE = False


class AppPult(QMainWindow, Ui_Ykazka):
    
    ITERATIONS: int = 1000

    sensitivity: int = 1
    
    currentPort = None

    serialPort = None
    
    btnBarrier = 250
    
    leftBtnI = 1010
    rightBtnI = 1010

    def __init__(self):

        super().__init__()

        self.setupUi(self)
        

        """привязка событий"""

        self.sensitivitySlider.valueChanged.connect(self.sensitivity_set_event)
        
        self.applyBtn.clicked.connect(self.apply_btn_event)
        
        self.comPortsList.mousePressEvent = self.com_ports_update

        self.connectBtn.clicked.connect(self.connect_event)

        self.timer = QTimer(self)
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.iter_pult_work)
        self.timer.start()


    """методы"""
    def write_to_console(self, message):
        self.outputText.append(str(message))


    def iter_pult_work(self):
        if self.currentPort is not None:
            try:
                request = self.serialPort.readline().decode("utf-8")

                request = list(map(float, request[1:].split()))
            except Exception as e:
                return
            
            if len(request) != 5:
                return
                
            self.write_to_console(request)


            # if request[4] < self.btnBarrier and :
            #     mouse.press(button="left")
            # else:
            #     mouse.release(button="left")


            # self.leftBtnI = request[4]
            # self.rightBtnI = request[3]
            # left btn

            # right btn

            # if request[3] > self.btnBarrier and not self.leftBtn:
            #     pag.mouseUp(button="left")
            #     self.leftLabel.setStyleSheet("background-color: rgb(209, 209, 209);\n")
            # else:
            #     self.leftLabel.setStyleSheet("background-color: rgb(100, 100, 100);\n")
            #     pag.mouseDown(button="left")

            # self.leftBtn = request[3] > self.btnBarrier

            # if request[4] > self.btnBarrier:
            #     self.rightLabel.setStyleSheet("background-color: rgb(209, 209, 209);\n")
            # else:
            #     self.rightLabel.setStyleSheet("background-color: rgb(100, 100, 100);\n")
            #     pag.click(button="left")


    """события"""
    def connect_event(self):

        comPort = self.comPortsList.currentText()
        self.connectLabel.setText("Подключение...")


        if comPort[:-1] != "COM":
            self.write_to_console("Неверно выбран порт")
            self.connectLabel.setText("Нет подключения")
            return


        connected = False
        connectedPort = serial.Serial(comPort, 115200)
        for iter in range(1, self.ITERATIONS + 1):

            try:
                request = connectedPort.readline().decode("utf-8")
            except Exception as e:
                continue

            if "O" in request:
                connected = True
                break

            self.progressBar.setValue(round((iter/self.ITERATIONS) * 100))

        self.progressBar.setValue(100)
        self.progressBar.setValue(0)


        if connected:
            self.currentPort = comPort
            self.connectLabel.setText(f"Подключено к {self.currentPort}")
            self.write_to_console(f"Подключено к {self.currentPort}")
            self.serialPort = connectedPort
        else:
            self.write_to_console("Неверно выбран порт")
            self.connectLabel.setText("Нет подключения")


    def sensitivity_set_event(self, value):
        self.sensitivity = value
        self.SensitivityValue.setText(f"{self.sensitivity}%")
        

    def com_ports_change(self, value):
        self.write_to_console(value)


    def com_ports_update(self, *args):

        comPorts = serial.tools.list_ports.comports()

        self.comPortsList.clear()

        self.comPortsList.showPopup()

        for port in comPorts:
            self.comPortsList.addItem(str(port.device), str(port.device))

        self.comPortsList.showPopup()


    def connect_btn_event(self):
        
        for i in range(100):

            self.progressBar.setValue(i + 1)

            QTimer.singleShot(100, lambda *args: None)
        
        self.progressBar.setValue(0)


    def apply_btn_event(self, *args):

        self.outputText.append("OK")

        
        


def main():

    app = QApplication(sys.argv)
    

    mainWindow = AppPult()


    mainWindow.show()
    

    sys.exit(app.exec_())




if __name__ == "__main__":
    main()


