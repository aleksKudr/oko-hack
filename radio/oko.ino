#define MBEE_SERIAL SoftwareSerial
#include <SoftwareSerial.h>

SoftwareSerial mySerial(10, 11); // RX, TX

void setup() {
  // открываем Serial-соединение с MBee-модулем
  // и передаём скорсть 9600 бод
  Serial.begin(9600);
  mySerial.begin(9600);
  // начало работы с кнопкой
  // светодиод в режим выхода
  pinMode(13, OUTPUT);

}
 
void loop() {
  if (Serial.available() > 0)
  {
    char data = Serial.read();        // читаем байт из буфера
    Serial.print(data);          // выводим байт в последовательный порт
    mySerial.print(data); 
  }

}
