#include <SoftwareSerial.h>
const int RX = 0;                      
const int TX = 1; 

SoftwareSerial BT(TX,RX);
typedef struct{
    float sensor;
    uint8_t checksum;
}Datos;

Datos datos;

void setup() {
  Serial.begin(115200);
  BT.begin(115200);
}

void loop() {
  float sensorValue = analogRead(A3);
  float voltaje = sensorValue * (5.0 / 1023.0);
  datos.sensor=voltaje;
  datos.checksum = checksum((uint8_t*)&datos, sizeof(datos));
  BT.write((uint8_t*)&datos, sizeof(datos));
  Serial.write((uint8_t*)&datos, sizeof(datos));
  //Serial.println(voltaje);
  delay(100);
}
uint8_t checksum(uint8_t *packet, uint8_t n)
{
    uint32_t sum = 0;
    for (int j=0;j<n-1;j++) sum += packet[j];
    return sum & 0x00FF;
}