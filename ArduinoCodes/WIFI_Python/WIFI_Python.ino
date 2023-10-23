#include <WiFiNINA.h>

char ssid[] = "HOME TEAM";      // Your WiFi network SSID
char pass[] = "jesaispas";  // Your WiFi network password
int status = WL_IDLE_STATUS;   // WiFi status

WiFiClient client;
const char server[] = "192.168.43.183"; // IP address of your Python script
const int port = 8888;                // Port number for communication

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
    Serial.println("Failed to connect to server...");
    delay(5000);
  }
}

void loop() {
  if (client.connected()) {
    // Send your string to the Python script
    client.println("Hello from Arduino!");

    // Check for a response from the server
    while (client.available()) {
      char c = client.read();
      Serial.write(c);
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
