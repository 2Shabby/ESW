#include <Arduino.h>
#include "esp32ModbusRTU.h"
#include <algorithm>  // for std::reverse
#include <Wire.h>
#include "WiFi.h"
#include "HTTPClient.h"
#include "ArduinoJson.h"
uint8_t newdata[10][4]; // The datastorage array
const char* wifi_ssid ="JioFi3_B51E5B"; // SSID for the WiFi Network
const char* wifi_pwd ="um9edttwd5"; // Password for the WiFi Network
String cse_ip = "onem2m.iiit.ac.in"; // The OneM2M network to be pushed to 
#define si7021Addr 0x40 // SI7021 I2C address is 0x40(64)
StaticJsonBuffer<200> jsonBuffer;
JsonObject& user_data = jsonBuffer.createObject();
JsonObject& temp_user_data = jsonBuffer.createObject();
JsonObject& sensor_data = jsonBuffer.createObject();

// String cse_port = "443"; To be used if a particular port is being pushed to
String server = "http://"+cse_ip+"/~/in-cse/in-name/"; // add +cse_port incase of a particuler port being pushed to

void createCI(String server, String ae, String cnt, String val)
{
  HTTPClient http;
  http.begin(server + ae + "/" + cnt + "/");
  http.addHeader("X-M2M-Origin", "admin:admin");
  http.addHeader("Content-Type", "application/json;ty=4");
  http.addHeader("Content-Length", "100");
  http.addHeader("Connection", "close");
  int code = http.POST("{\"m2m:cin\": {\"cnf\": \"text/plain:0\",\"con\": "+ String(val) +"}}");
  http.end();
  Serial.println(String(val));
  Serial.println(code);
  delay(300);
}
 
esp32ModbusRTU modbus(&Serial1, 25);  // use Serial1 and pin 16 as RTS
uint8_t data2[4];
void setup() {
  Wire.begin();
  Serial.begin(9600);
  Wire.beginTransmission(si7021Addr);
  Wire.endTransmission();
  delay(300);
  Serial.begin(9600);  // Serial output
  Serial1.begin(9600, SERIAL_8E1, 26, 27);  // Modbus connection

  modbus.onData([](uint8_t serverAddress, esp32Modbus::FunctionCode fc, uint8_t* data, size_t length) {
    data2[0] = data[1];
    data2[1] = data[0];
    data2[2] = data[3];
    data2[3] = data[2];
    //Conversion of data little-big endian
  });
  modbus.onError([](esp32Modbus::Error error) {
    Serial.printf("Got error: 0x%02x\n\n", static_cast<uint8_t>(error)); //Print the error code
  });
  modbus.begin();
  // Set WiFi to station mode and disconnect from an AP if it was previously connected
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);
  WiFi.begin(wifi_ssid, wifi_pwd);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000); // Recheck Wifi connection at 1second timegaps
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network"); // Confirmation of Wifi Setup on serialmonitor
  Serial.println("Setup done"); // Confirmation of the entire setup complete

}
/*
  The error codes that that are returned from the modbus request incase of an error that are printed on the serial monitor
  
  SUCCES                = 0x00,
  ILLEGAL_FUNCTION      = 0x01,
  ILLEGAL_DATA_ADDRESS  = 0x02,
  ILLEGAL_DATA_VALUE    = 0x03,
  SERVER_DEVICE_FAILURE = 0x04,
  ACKNOWLEDGE           = 0x05,
  SERVER_DEVICE_BUSY    = 0x06,
  NEGATIVE_ACKNOWLEDGE  = 0x07,
  MEMORY_PARITY_ERROR   = 0x08,
  TIMEOUT               = 0xE0,
  INVALID_SLAVE         = 0xE1,
  INVALID_FUNCTION      = 0xE2,
  CRC_ERROR             = 0xE3,  // only for Modbus-RTU
  COMM_ERROR            = 0xE4  // general communication error
 */
void loop() {
   unsigned int daddata[2];
   
  Wire.beginTransmission(si7021Addr);
  //Send humidity measurement command
  Wire.write(0xF5);
  Wire.endTransmission();
  delay(500);
     
  // Request 2 bytes of data
  Wire.requestFrom(si7021Addr, 2);
  // Read 2 bytes of data to get humidity
  if(Wire.available() == 2)
  {
    daddata[0] = Wire.read();
    daddata[1] = Wire.read();
  }
     
  // Convert the data
  float humidity  = ((daddata[0] * 256.0) + daddata[1]);
  humidity = ((125 * humidity) / 65536.0) - 6;
 
  Wire.beginTransmission(si7021Addr);
  // Send temperature measurement command
  Wire.write(0xF3);
  Wire.endTransmission();
  delay(500);
     
  // Request 2 bytes of data
  Wire.requestFrom(si7021Addr, 2);
   
  // Read 2 bytes of data for temperature
  if(Wire.available() == 2)
  {
    daddata[0] = Wire.read();
    daddata[1] = Wire.read();
  }
 
  // Convert the data
  float temp  = ((daddata[0] * 256.0) + daddata[1]);
  float celsTemp = ((175.72 * temp) / 65536.0) - 46.85;
  float fahrTemp = celsTemp * 1.8 + 32;
  delay(1000);
  static uint32_t lastMillis = 0;
  if (millis() - lastMillis > 10000) {
    lastMillis = millis();
    Serial.print("sending Modbus request...\n");
    //readHoldingRegisters(uint8_t slaveAddress, uint16_t address, uint16_t numberRegisters) is the format of the modbus request
    //Read from the 5 energy meters
    modbus.readHoldingRegisters(0x01,158,2);
    for(int j=0;j<4;j++)
      newdata[0][j]=data2[j];
      delay(2000);
    modbus.readHoldingRegisters(0x02,158,2);
    for(int j=0;j<4;j++)
      newdata[1][j]=data2[j];
      delay(2000);
    modbus.readHoldingRegisters(0x03,158,2);
    for(int j=0;j<4;j++)
      newdata[2][j]=data2[j];
      delay(2000); 
    modbus.readHoldingRegisters(0x04,158,2);
    for(int j=0;j<4;j++)
      newdata[3][j]=data2[j];
      delay(2000);
    modbus.readHoldingRegisters(0x05,158,2);
    for(int j=0;j<4;j++)
      newdata[4][j]=data2[j];
      delay(2000);
    modbus.readHoldingRegisters(0x01,100,2);
    for(int j=0;j<4;j++)
      newdata[5][j]=data2[j];
      delay(2000);
    modbus.readHoldingRegisters(0x02,100,2);
    for(int j=0;j<4;j++)
      newdata[6][j]=data2[j];
      delay(2000);
    modbus.readHoldingRegisters(0x03,100,2);
    for(int j=0;j<4;j++)
      newdata[7][j]=data2[j];
      delay(2000); 
    modbus.readHoldingRegisters(0x04,100,2);
    for(int j=0;j<4;j++)
      newdata[8][j]=data2[j];
      delay(2000);
    modbus.readHoldingRegisters(0x05,100,2);
    for(int j=0;j<4;j++)
      newdata[9][j]=data2[j];
      delay(2000);  
    for(int i=0;i<10;i++)
      Serial.printf("\nval %d: %.2f",i, *reinterpret_cast<float*>(newdata[i]));
  }
  
  String sensor1 = String(humidity) + " " + String(celsTemp) + " " + String(fahrTemp);
  for(int i = 0;i<10;i++)
    sensor1 += " " + String(*reinterpret_cast<float*>(newdata[i])); 
    
  //when single sensor gives single value
  String sensor2 = String(10); 

  // Make it a single string
  String sensor_string = sensor1; // + "," + sensor2;

  // Make it OneM2M complaint
  sensor_string = "\"" + sensor_string + "\""; // DO NOT CHANGE THIS LINE
  
  // Send data to OneM2M server
  createCI(server, "Team32_Campus_energy_and_demand_dashboard", "pr_1_esp32_1", sensor_string);
  delay(1*60*60*1000); //1000 minutes delay between uploads
}
