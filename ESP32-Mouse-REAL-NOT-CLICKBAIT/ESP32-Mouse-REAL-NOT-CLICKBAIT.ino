#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

// Create BNO055 object
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28); // 0x28 is the default I2C address

void setup() {
  Serial.begin(115200);
  delay(1000);

  if (!bno.begin()) {
    Serial.println("BNO055 not detected. Check wiring or I2C address.");
    while (1);
  }

bno.setMode(adafruit_bno055_opmode_t::OPERATION_MODE_NDOF);

bno.setExtCrystalUse(true);
}

void loop() {

  //Gyroscope data in quaternions:
  imu::Quaternion quat = bno.getQuat();

  Serial.print("x:"); 
  Serial.println(quat.x(), 2);
  Serial.print("y:"); 
  Serial.println(quat.y(), 2);
  Serial.print("z:"); 
  Serial.println(quat.z(), 2);
  //Serial.println(piezo);
  delay(200);

  
}
