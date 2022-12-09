#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"


MPU6050 mpu;
uint8_t fifoBuffer[45];         // буфер




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
      // Serial.print(ypr[0]); // вокруг оси Z
      // Serial.print(',');
      // Serial.print(ypr[1]); // вокруг оси Y
      // Serial.print(',');
      // Serial.print(ypr[2]); // вокруг оси X
      // Serial.println();
      // для градусов можно использовать degrees()
      tmr = millis();   // сброс таймера
    }
  }
  return res;
}


void setup() {
  Serial.begin(9600);
  Wire.begin();
  //Wire.setClock(1000000UL);   // разгоняем шину на максимум
  // инициализация DMP
  mpu.initialize();
  mpu.dmpInitialize();
  mpu.setDMPEnabled(true);
  connect();
}


void connect()
{
  while (true)
  {
    Serial.println("test");
    if (Serial.available())
    {
      char data = Serial.read();
      if (data == 'k')
      {
        break;
      }
      Serial.print(data);
    }
  }
  Serial.println("connected");
}

// commands prefix O - ypr info, B - btn info

void loop()
{
  // O
  yaw_pitch_roll oInfo = get_ypr();
  Serial.print("O");
  Serial.print(oInfo.yaw);
  Serial.print(" ");
  Serial.print(oInfo.pitch);
  Serial.print(" ");
  Serial.print(oInfo.roll);
  Serial.println();
}
