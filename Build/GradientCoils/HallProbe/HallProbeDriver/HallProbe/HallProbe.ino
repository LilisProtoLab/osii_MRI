#include <Wire.h>

// Define the I2C address for the TMAG5273D1
#define TMAG5273_ADDRESS 0x44

// Register addresses for measurement data
#define T_MSB_RESULT 0x10
#define T_LSB_RESULT 0x11
#define X_MSB_RESULT 0x12
#define X_LSB_RESULT 0x13
#define Y_MSB_RESULT 0x14
#define Y_LSB_RESULT 0x15
#define Z_MSB_RESULT 0x16
#define Z_LSB_RESULT 0x17
#define DEVICE_CONFIG_1 0x00
#define DEVICE_CONFIG_2 0x01
#define SENSOR_CONFIG_1 0x02
#define SENSOR_CONFIG_2 0x03


// Sensitivity values for the TMAG5273D2
#define SENSITIVITY_LOW_RANGE 820.0  // LSB/mT for ±40 mT range
#define SENSITIVITY_HIGH_RANGE 410.0 // LSB/mT for ±80 mT range

// Set the magnetic range (0 for ±40mT, 1 for ±80mT)
#define MAGNETIC_RANGE 0 // Change to 1 for ±80 mT range

void setup() {
  Wire.begin(); // Initialize I2C
  Serial.begin(9600); // Initialize serial communication

  // Configure the TMAG5273
  configureTMAG5273();

  // Print the magnetic range being used
  if (MAGNETIC_RANGE == 0) {
    Serial.println("Using ±40 mT range (Low range)");
  } else {
    Serial.println("Using ±80 mT range (High range)");
  }
}

void loop() {
  // Read temperature and magnetic field raw data
  int16_t temperature = read16BitData(T_MSB_RESULT, T_LSB_RESULT);
  int16_t xField = read16BitData(X_MSB_RESULT, X_LSB_RESULT);
  int16_t yField = read16BitData(Y_MSB_RESULT, Y_LSB_RESULT);
  int16_t zField = read16BitData(Z_MSB_RESULT, Z_LSB_RESULT);

  // Calculate temperature in degrees Celsius
  float temperatureC = 25 + (temperature - 17508) / 60.1;

  // Calculate magnetic field in mT
  float sensitivity = (MAGNETIC_RANGE == 0) ? SENSITIVITY_LOW_RANGE : SENSITIVITY_HIGH_RANGE;
  float xField_mT = xField / sensitivity;
  float yField_mT = yField / sensitivity;
  float zField_mT = zField / sensitivity;

  // Print the results to the Serial Monitor
  /*
  Serial.print("Temperature (C): ");
  Serial.println(temperatureC);
  */
  //Serial.print("X-axis (mT): ");
  Serial.print(xField_mT, 3);
  Serial.print(",");
  //Serial.print("Y-axis (mT): ");
  Serial.print(yField_mT, 3);
  Serial.print(",");
 // Serial.print("Z-axis (mT): ");
  Serial.println(zField_mT, 3);

  // Wait for 1 second before the next reading
  delay(100);
}

void configureTMAG5273() {
  // Set DEVICE_CONFIG_1: standard I2C read mode should be 0x14 for 32 times average
  writeRegister(DEVICE_CONFIG_1, 0x14);

  // Set DEVICE_CONFIG_2: Continuous measure mode
  writeRegister(DEVICE_CONFIG_2, 0x02);

  // Set SENSOR_CONFIG_1: Enable X, Y, Z, and temperature channels
  // Configure the magnetic range (MAGNETIC_RANGE sets X_Y_RANGE and Z_RANGE bits)
  writeRegister(SENSOR_CONFIG_1,0x70);
  if (MAGNETIC_RANGE == 0) {
    writeRegister(SENSOR_CONFIG_2,0x00); // Set X_Y_RANGE=0 and Z_RANGE=0 for ±40 mT 
  } else {
    writeRegister(SENSOR_CONFIG_2,0x03); // Set X_Y_RANGE=1 and Z_RANGE=1 for ±80 mT
  }

}

int16_t read16BitData(uint8_t msbRegister, uint8_t lsbRegister) {
  uint8_t msb = readRegister(msbRegister);
  uint8_t lsb = readRegister(lsbRegister);
  return (int16_t)((msb << 8) | lsb);
}

void writeRegister(uint8_t reg, uint8_t value) {
  Wire.beginTransmission(TMAG5273_ADDRESS);
  Wire.write(reg);
  Wire.write(value);
  Wire.endTransmission();
}

uint8_t readRegister(uint8_t reg) {
  Wire.beginTransmission(TMAG5273_ADDRESS);
  Wire.write(reg);
  Wire.endTransmission(false); // Send stop condition after request
  Wire.requestFrom(TMAG5273_ADDRESS, 1); // Request 1 byte
  return Wire.read();
}
