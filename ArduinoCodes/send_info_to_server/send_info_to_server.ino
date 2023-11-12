#include <WiFiNINA.h>
#include <Arduino_LSM6DS3.h>
#include <PS2MouseHandler.h>


// Wi-Fi info
char ssid[] = "bwm-11914";      // Your WiFi network SSID
char pass[] = "Bruniere11?";  // Your WiFi network password
int status = WL_IDLE_STATUS;   // WiFi status

WiFiClient client;
const char server[] = "192.168.1.111"; // IP address of your Python script
const int port = 8888;                // Port number for communication

// Mouse info
#define MOUSE_DATA 5
#define MOUSE_CLOCK 6

// Mode info
int mode = 0; // 0 = idle, 1 = record

PS2MouseHandler mouse(MOUSE_CLOCK, MOUSE_DATA, PS2_MOUSE_REMOTE);


void setup() {
  // Initialize serial communication for debugging
  Serial.begin(9600);

  // Connect to WiFi
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
    delay(10000);  // Try connecting every 10 seconds
  }
  // Print your Arduino's IP address
  IPAddress localIP = WiFi.localIP();
  Serial.print("Connected to WiFi. Local IP address: ");
  Serial.println(localIP);
  // Wait for a successful connection
  while (!client.connect(server, port)) {
    Serial.println("Failed to connect to server... trying again");
    delay(5000);
  }
  Serial.println("server connected successfully.");
  Serial.println();


  // setup mouse
  Serial.print("Connecting the mouse...");
  Serial.print(mouse.initialise());
  if(mouse.initialise() != 0){
    // mouse error
    Serial.println("mouse error");
  };
  Serial.println(mouse.device_id());
  Serial.println("Mouse connected successfully.");
  Serial.println();
  

  // Setup IMU
  Serial.print("LSM6DS3 IMU initialization ");
  if (IMU.begin()) {  // initialize IMU
    Serial.println("completed successfully.");
  } else {
    Serial.println("FAILED to connect IMU.");
    IMU.end();
    while (1);
  }

  Serial.println();
}




void loop() {
  float gx, gy, gz;  // gyroscope values
  unsigned long last_run = millis(); // mouse check
  unsigned long time, last_time, dt; // time values
  float status_mouse, x_mvt_raw, y_mvt_raw; // mouse values
  
  if (client.connected()) {

    if (mode == 1) {
      // get optical mouse data
      if (millis() - last_run > 200) {
        last_run = millis();
        mouse.get_data();
        status_mouse = mouse.status(); // Status Byte
        x_mvt_raw = mouse.x_movement(); // X Movement Data
        y_mvt_raw = mouse.y_movement(); // Y Movement Data
      }

      // get IMU data
      if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(gx, gy, gz);
        }

      // get time
      time = millis();
      dt = time - last_time;

      // Convert data to strings
      String gxStr = String(gx);
      String gyStr = String(gy);
      String gzStr = String(gz);
      String xMvtRawStr = String(x_mvt_raw);
      String yMvtRawStr = String(y_mvt_raw);
      String timeStr = String(time);
      String timeDiffStr = String(dt);

      //create the message to send
      String dataStr = timeStr + "," + timeDiffStr + "," + gxStr + "," + gyStr + "," + gzStr + "," + xMvtRawStr + "," + yMvtRawStr;

      // Send your string to the Python script
      client.println(dataStr);

      last_time = time;
    }

    // Check for a response from the server
    while (client.available()) {
      String msg = client.readString();
      
      // Serial.write(c);
      Serial.println(msg);
      if (msg == "strt"){
        mode = 1;
        Serial.println("Mode changed to record");
      }
      else if (msg == "stop"){
        mode = 0;
        Serial.println("Mode changed to idle");
      }
    }
  
  } else {
    Serial.println("Connection lost. Reconnecting...");
    client.stop();
    delay(5000);
    if (client.connect(server, port)) {
      Serial.println("Reconnected to the server.");
    }
  }

  delay(1000);  // Send data every 1 second
}


