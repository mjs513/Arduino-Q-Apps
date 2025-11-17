#include <Arduino_RouterBridge.h>

#include <Wire.h>
#include "SparkFun_BMI270_Arduino_Library.h"
// Create a new sensor object
BMI270 imu;

#include "DFRobot_BMM150.h"
DFRobot_BMM150_I2C bmm150(&Wire1, 0x13); //0x10-nano, 0x13dfrobot

// I2C address selection
uint8_t i2cAddress = BMI2_I2C_PRIM_ADDR; // 0x68
//uint8_t i2cAddress = BMI2_I2C_SEC_ADDR; // 0x69

char roll_text[30];
char pitch_text[30];
char yaw_text[30];

void setup()
{
    // Start serial
    Serial.begin(115200);
    Serial.println("BMI270 Example 1 - Basic Readings I2C");

    // Initialize the I2C library
    Wire1.begin();
    Wire1.setClock(100000);
    // Check if sensor is connected and initialize
    // Address is optional (defaults to 0x68)
    while(imu.beginI2C(BMI2_I2C_PRIM_ADDR, Wire1) != BMI2_OK)
    {
        // Not connected, inform user
        Serial.println("Error: BMI270 not connected, check wiring and I2C address!");
        // Wait a bit to see if connection is established
        delay(1000);
    }
    Serial.println("BMI270 connected!");

  while(bmm150.begin()){
    Serial.println("bmm150 init failed, Please try again!");
    delay(1000);
  } Serial.println("bmm150 init success!");
  bmm150.setOperationMode(BMM150_POWERMODE_NORMAL);
  bmm150.setPresetMode(BMM150_PRESETMODE_HIGHACCURACY);
  bmm150.setRate(BMM150_DATA_RATE_25HZ);
  bmm150.setMeasurementXYZ();

  Bridge.begin();
  Bridge.provide("get_euler", get_euler);
}

void loop()
{
    // Get measurements from the sensor. This must be called before accessing
    // the sensor data, otherwise it will never update
    imu.getSensorData();
/*
    // Print acceleration data
    Serial.print("Acceleration in g's");
    Serial.print("\t");
    Serial.print("X: ");
    Serial.print(imu.data.accelX, 3);
    Serial.print("\t");
    Serial.print("Y: ");
    Serial.print(imu.data.accelY, 3);
    Serial.print("\t");
    Serial.print("Z: ");
    Serial.print(imu.data.accelZ, 3);

    Serial.print("\t");

    // Print rotation data
    Serial.print("Rotation in deg/sec");
    Serial.print("\t");
    Serial.print("X: ");
    Serial.print(imu.data.gyroX, 3);
    Serial.print("\t");
    Serial.print("Y: ");
    Serial.print(imu.data.gyroY, 3);
    Serial.print("\t");
    Serial.print("Z: ");
    Serial.println(imu.data.gyroZ, 3);
*/
    sBmm150MagData_t magData = bmm150.getGeomagneticData();
/*
    Serial.print("mag x = "); Serial.print(magData.x); Serial.println(" uT");
    Serial.print("mag y = "); Serial.print(magData.y); Serial.println(" uT");
    Serial.print("mag z = "); Serial.print(magData.z); Serial.println(" uT");

    float compassDegree = bmm150.getCompassDegree();
    Serial.print("the angle between the pointing direction and north (counterclockwise) is:");
    Serial.println(compassDegree);
    Serial.println("--------------------------------");
*/
    Bridge.notify("get_data", imu.data.accelX, imu.data.accelY, imu.data.accelZ, imu.data.gyroX, imu.data.gyroY, imu.data.gyroZ, magData.x, magData.y, magData.z);

  
    delay(50);
}

void get_euler(float roll, float pitch, float yaw )
{
  /*
  Serial.print("Roll:");
  Serial.print(roll);  Serial.print(" \t");
  Serial.print("Pitch:");Serial.print(pitch);  Serial.print(" \t");
  Serial.print("Yaw:");Serial.println(yaw);  Serial.println("-----------------");
  */

	dtostrf(roll, 10, 10, roll_text);
	dtostrf(pitch, 10, 10, pitch_text);
	dtostrf(yaw, 10, 10, yaw_text);

	char text[94];
	snprintf(text, 94, "%s,%s,%s", roll_text, pitch_text, yaw_text);
	Serial.println(text);
}

char* dtostrf(float val, int width, unsigned int precision, char* buffer) {
snprintf(buffer, width + 1, "%*.*f", width, precision, val);
return buffer;
}
