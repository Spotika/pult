import pyautogui as pag

pag.PAUSE = 0
pag.FAILSAFE = False


class Data:
    lastMpuX = 0
    lastMpuY = 0
    sensitive = 500
    stopMode = 0


class Functional:

    @staticmethod
    def btn_left_click(mpu, buttons, num):
        if buttons[num] == "1":
            pag.mouseDown(button=1)
        else:
            pag.mouseDown(button=1)
        print(num, buttons[num])

    @staticmethod
    def btn_right_click(mpu, buttons, num):
        # if buttons[num] == "1":
        
        #     pag.mouseDown(3)
        # else:
        #     pag.mouseDown(3)
        # print(num, buttons[num])
        ...


    @staticmethod
    def btn_stop_move(mpu, buttons, num):
        if buttons[num] == "1":
            Data.stopMode = True
        else:
            Data.stopMode = False

    @staticmethod
    def move(mpu, buttons):
        dx = mpu[0] - Data.lastMpuX
        dy = mpu[1] - Data.lastMpuY

        Data.lastMpuX, Data.lastMpuY = mpu[0], mpu[1]

        if Data.stopMode:
            return

        pag.move(dx * Data.sensitive, -dy * Data.sensitive)

    @staticmethod
    def nothing(*args, **kwargs):
        ...


class Button:
    state = False
    """
    True is pressed
    """

    def __init__(self, function=Functional.nothing):
        self.event = function

    def update(self, mode):
        if mode == "1" and self.state is False:
            self.state = True
            return True
        elif mode == "0":
            if self.state:
                self.state = False
                return True
        return False

    def __call__(self, mpu, buttons, num):
        if self.update(buttons[num]):
            self.event(mpu, buttons, num)


class AlgoCore:
    buttonObjects = [
        Button(Functional.btn_left_click),
        Button(Functional.btn_left_click),
        Button(Functional.btn_stop_move),
        Button(),
        Button(),
        Button(),
    ]

    functions = [
        Functional.move
    ]

    @classmethod
    def tick(cls, mpu: tuple[int, int], buttons: str):
        print(buttons)
        for i in range(len(buttons)):
            cls.buttonObjects[i](mpu, buttons, i)

        for func in cls.functions:
            func(mpu, buttons)
