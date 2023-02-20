#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include "Wire.h"
#include "GyverOLED.h"


MPU6050 mpu;
uint8_t fifoBuffer[45];         // буфер

GyverOLED<SSD1306_128x32, OLED_NO_BUFFER> oled;

int timeDelay = 0.1;

// buttons
int buttons[6] = {A0, A1, A2, A3, A6, A7};

char terminator = '!';


struct yaw_pitch_roll 
{
  float yaw;  
  float pitch;
  float roll;
};


yaw_pitch_roll get_ypr()
{
  static uint32_t tmr;
  yaw_pitch_roll res;
  if (millis() - tmr >= 11) {  // таймер на 11 мс (период готовности значений)    
    if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) {
      // переменные для расчёта (ypr можно вынести в глобал)
      Quaternion q;
      VectorFloat gravity;
      float ypr[3];
      // расчёты
      mpu.dmpGetQuaternion(&q, fifoBuffer);
      mpu.dmpGetGravity(&gravity, &q);
      mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
      // выводим результат в радианах (-3.14, 3.14)
      res.yaw = ypr[0];
      res.pitch = ypr[1];
      res.roll = ypr[2];            
      tmr = millis();   // сброс таймера
    }
  }
  return res;
}

void mpu_init()
{
  mpu.initialize();
  mpu.dmpInitialize();
  mpu.setDMPEnabled(true);
}

void oled_init()
{
  oled.init();
  oled.clear();
  oled.home();
}

String get_button_info()
{
  String result = "";

  for (auto button : buttons)
  {
    int responce = analogRead(button);
    bool isPressed = false;

    if (responce < 30)
    {
      isPressed = true;
    }

    if (isPressed)
    {
      result = result + "1";
    }
    else
    {
      result = result + "0";
    }
  }
  return result;
}

String ypr_to_string(yaw_pitch_roll ypr)
{
  return String(ypr.yaw) + " " + String(ypr.pitch) + " " + String(ypr.roll);
}

void setup() {
  Serial.begin(115200);
  Wire.begin();

  mpu_init();
  oled_init();

  for (auto button : buttons)
  {
    pinMode(button, INPUT_PULLUP);
  }
}



void loop()
{
  String transferData = "", recivedData = "";
  transferData = "O" + ypr_to_string(get_ypr());

  transferData = transferData + " " + get_button_info() + "\n";


  Serial.print(transferData);

  if (Serial.available())
  {
    char command = Serial.read();
    if (command == 'C') // clear display
    {
      oled.clear();
    }
    else if (command == 'W') // write text
    {
      String text = Serial.readStringUntil(terminator);
      oled.print(text);
    }
    else if (command == 'M') // move cursor
    {
      int x = Serial.parseInt();
      Serial.read();
      int y = Serial.parseInt();
      oled.setCursor(x, y);
    }
    else if (command == 'S') // set scale
    {
      int scale = Serial.parseInt();
      oled.setScale(scale);
    }

    Serial.readStringUntil(terminator);
  }

  delay(timeDelay);
}
