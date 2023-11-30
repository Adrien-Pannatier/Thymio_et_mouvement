#include <WiFiNINA.h>
#include <Arduino_LSM6DS3.h>
#include <PS2MouseHandler.h>

// Wi-Fi info
// char ssid[] = "bwm-11914";      // Your WiFi network SSID
// char pass[] = "Bruniere11?";  // Your WiFi network password
// const char server[] = "192.168.1.111"; // IP address of your Python script

char ssid[] = "Adrien's Galaxy A52 5G";      // Your WiFi network SSID
char pass[] = "mqbm9064";  // Your WiFi network password
const char server[] = "192.168.249.225"; // IP address of your Python script
int status = WL_IDLE_STATUS;   // WiFi status
unsigned long last_time;

WiFiClient client;

const int port = 2222;                // Port number for communication

// Mouse info
#define MOUSE_DATA 5
#define MOUSE_CLOCK 6
#define ARRAY_SIZE 40

// Mode info
int mode = 0; // 0 = idle, 1 = record

// Count sending data
int count = 0;

String data_to_send[ARRAY_SIZE];

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
  float gx, gy, gz;  // gyroscope values [in rad/s]
  unsigned long time, dt; // time values [in ms]
  float status_mouse, x_mvt_raw, y_mvt_raw; // mouse values
  
  if (client.connected()) {

    if (mode == 1) {
        while(count <= ARRAY_SIZE) {
          // get optical mouse data
          if (millis() - last_time > 20) {
            Serial.println("getting mouse data");
            mouse.get_data();
            status_mouse = mouse.status(); // Status Byte
            x_mvt_raw = mouse.x_movement(); // X Movement Data [in pixels]
            y_mvt_raw = mouse.y_movement(); // Y Movement Data [in pixels]
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
          String dataStr = "s," + timeStr + "," + timeDiffStr + "," + gxStr + "," + gyStr + "," + gzStr + "," + xMvtRawStr + "," + yMvtRawStr + ",n";

          data_to_send[count] = dataStr;

          Serial.print("saved : ");
          Serial.println(data_to_send[count]);

          last_time = time;
          count = count + 1;
        }
      }

    // Check for a response from the server
    while (client.available()) {
      String msg = client.readString();
      
      // Serial.write(c);
      Serial.print("Message recieved: ");
      Serial.println(msg);
      if (msg == "start"){
        count = 0;
        mode = 1;
        Serial.println("Mode changed to record");
      }
      else if (msg == "stop"){
        mode = 0;
        Serial.println("Mode changed to idle, sending whole data");

        // Send your string to the Python script
        for (int i = 0; i <= ARRAY_SIZE; i++) {
          Serial.print("sending : ");
          Serial.println(data_to_send[i]);
          client.print(data_to_send[i]); 
        }
        client.print("c");

        Serial.println("empty the data buffer");
        // empty table
        for (int i = 0; i <= ARRAY_SIZE; i++) {
          data_to_send[i] = "";
        }
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

  // delay(500);  // Send data every 0.5 second
}


