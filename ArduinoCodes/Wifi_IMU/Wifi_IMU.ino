#include <ArduinoHttpClient.h>
#include <SPI.h>
#include <WiFiNINA.h>
#include <Arduino_LSM6DS3.h>

char ssid[] = "HOME TEAM";
char pass[] = "jesaispas";
int keyIndex = 0;

int status = WL_IDLE_STATUS;
WiFiServer server(80); // might be a reason to change the port

// Variable to store the HTTP request
String header;

void setup() {
  Serial.begin(9600);

  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to Network named: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
    delay(10000); // 10 sec delay
  }
  server.begin();

  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());
  IPAddress ip = WiFi.localIP(); // to connect into the web browser
  Serial.print("IP Address: ");
  Serial.println(ip);
   
  while (!Serial);  // wait for serial initialization
  Serial.print("LSM6DS3 IMU initialization ");
  if (IMU.begin()) {  // initialize IMU
    Serial.println("completed successfully.");
  } else {
    Serial.println("FAILED.");
    IMU.end();
    while (1);
  }
  Serial.println();
}

void loop() {
  char buffer[8];    // string buffer for use with dtostrf() function
  float ax, ay, az;  // accelerometer values
  float gx, gy, gz;  // gyroscope values
  WiFiClient client = server.available();   
  if (client) {                             
    Serial.println("new client"); // if a client is connecting to the arduino wifi          
    String currentLine = "";                
    while (client.connected()) {            
      if (client.available()) {             
        char c = client.read(); // once the browser has finish communicating basics, prints "hello world"          
        Serial.write(c);    
        header += c;                
        if (c == '\n') {                    

          if (currentLine.length() == 0) {
            // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
            // and a content-type so the client knows what's coming, then a blank line:
            // client.println("HTTP/1.1 200 OK");
            // client.println("Content-type:text/html");
            // client.println("Connection: close");
            // client.println();

            // client.println("<!DOCTYPE html><html>");
            // client.println("<head>");
            // client.println("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">");
            // client.println("<meta http-equiv=\"refresh\" content=\"30\>");
            // // CSS to style the on/off buttons 
            // // Feel free to change the background-color and font-size attributes to fit your preferences
            // client.println("<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}");
            // client.println(".button { background-color: #4CAF50; border: none; color: white; padding: 16px 40px;");
            // client.println("text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}");
            // client.println(".button2 {background-color: #555555;}</style></head>");
            
            // Web Page Heading
            // client.println("<body><h1>Curling</h1>");

            // client.println("</body></html>");

            // The HTTP response ends with another blank line
            // client.println();
            // Break out of the while loop
            // break;

            // Retrieve and print IMU values
            while(1){
              if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()
                && IMU.readAcceleration(ax, ay, az) && IMU.readGyroscope(gx, gy, gz)) {
                client.print("gx = ");  client.print(dtostrf(gx, 7, 1, buffer));  client.print(" °/s, ");
                client.print("gy = ");  client.print(dtostrf(gy, 7, 1, buffer));  client.print(" °/s, ");
                client.print("gz = "); client.print(dtostrf(gz, 7, 1, buffer));  client.println(" °/s");
              }
              delay(1000);  // wait one second between readings
              client.print("document.body.innerHTML=""");
            }
          } else {
            currentLine = "";
          }
        } else if (c != '\r') {
          currentLine += c;
        }
      }
    }
    header = ""; 
    client.stop();
    Serial.println("client disonnected");
    Serial.println("");
  }
}