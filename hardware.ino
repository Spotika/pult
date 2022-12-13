#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
// подключение библиотек для работы с гироскопом

MPU6050 mpu;
uint8_t fifoBuffer[45]; // буфер


struct yaw_pitch_roll 
{
// структура хранения данных о положении гироскопа в пространстве
  float yaw;  
  float pitch;
  float roll;
};


yaw_pitch_roll get_ypr()
{
// функция для получения положения гироскопа в пространстве. Учитывается ускорение свободного падения
  static uint32_t tmr;
  yaw_pitch_roll res; // создание структуры
  
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
      // сохранение данных в структуру
      res.yaw = ypr[0];
      res.pitch = ypr[1];
      res.roll = ypr[2];            
      tmr = millis();   // сброс таймера
    }
  }
  return res; 
  // возврат ссылки на структуру с данными   
}

void setup() {
  Serial.begin(115200); // Объявление о начале работы с передачей данных на максимальной частоте
  
  // инициализация I2C и запуск гироскопа
  Wire.begin(); 
  mpu.initialize();
  mpu.dmpInitialize();
  mpu.setDMPEnabled(true);
}

void loop()
{
// отправка по Serial порту данные с гироскопа с префиксом "O" для определения передатчика  
  yaw_pitch_roll oInfo = get_ypr();
  Serial.print("O");
  Serial.print(oInfo.yaw);
  Serial.print(" ");
  Serial.print(oInfo.pitch);
  Serial.print(" ");
  Serial.print(oInfo.roll);
  Serial.println();
}
