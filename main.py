import serial
import serial.tools.list_ports
import macros
import pyautogui
import time


pyautogui.FAILSAFE = False

pyautogui.PAUSE = 0


class SerialInterface:
    WELCOME_TEXT = """Welcome"""

    HELP_TEXT = """
    None
    """

    DELAY = 1 / 60

    class Utility:

        NUM_OF_ITER = 10
        ITER_DELAY = 0.3

        @classmethod
        def identification(cls):
            for port in serial.tools.list_ports.comports():
                print("Trying port", port.name + "...")

                connectedSerial = serial.Serial(port.name, 115200, timeout=1)
                while connectedSerial is None:
                    ...
                for _ in range(cls.NUM_OF_ITER):

                    data = connectedSerial.readline().decode("utf-8")
                    try:
                        if data[0] == "O":
                            return connectedSerial
                    except IndexError:
                        ...
            return None

    mainRun = True
    serialRun = False
    connectedPort = None

    buttonsState = [0, 0, 0, 0, 0, 0]
    prevX, prevY = 0, 0

    def __init__(self):
        print(self.WELCOME_TEXT)

    def serial_loop(self):
        self.serialRun = True
        if self.connectedPort is None:
            connectedPort = self.connect()
        else:
            connectedPort = self.connectedPort
        if connectedPort is None:
            print("Connection error")
            return

        self.connectedPort = connectedPort
        print("Connected")

        try:
            while self.serialRun:
                try:

                    receivedData = connectedPort.readline().decode("utf-8")[1:].split()

                    # mpu
                    mpu = tuple(map(float, receivedData[:2]))

                    # buttons
                    btnData = receivedData[-1]

                    macros.AlgoCore.tick(mpu, btnData)


                except Exception:
                    ...

        except KeyboardInterrupt:
            self.serialRun = False

    def main_loop(self):
        while self.mainRun:
            try:
                command = input(">>> ")
            except UnicodeDecodeError:
                command = [""]

            match command.split():
                case [""]:
                    ...

                case ["run"]:
                    self.serial_loop()

                case ["help"]:
                    print(self.HELP_TEXT)

                case ["exit"]:
                    self.mainRun = False

                case ["sensitive", value]:
                    if value.isnumeric():
                        print("Sensitive set to", value)
                        macros.Data.sensitive = int(value)

                case ["text", text]:
                    if self.connectedPort is None:
                        self.connectedPort = self.connect()
                    if self.connectedPort is None:
                        print("Connection error")
                    else:
                        self.connectedPort.write("C!".encode("utf-8"))
                        time.sleep(1)
                        self.connectedPort.write(f"W{text}!".encode("utf-8"))

                case [unknown]:
                    print(f"'{unknown}' is not a command, try 'help', to see a list of commands")

    def connect(self):
        return self.Utility.identification()


def main():
    app = SerialInterface()
    app.main_loop()


if __name__ == "__main__":
    main()
