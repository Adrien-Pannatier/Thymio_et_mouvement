#include <SPI.h>
#include <WiFiNINA.h>

char ssid[] = "HOME TEAM";
char pass[] = "jesaispas";
int keyIndex = 0;

int status = WL_IDLE_STATUS;
WiFiServer server(80); // might be a reason to change the port

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
}

void loop() {
  WiFiClient client = server.available();   
  if (client) {                             
    Serial.println("new client"); // if a client is connecting to the arduino wifi          
    String currentLine = "";                
    while (client.connected()) {            
      if (client.available()) {             
        char c = client.read(); // once the browser has finish communicating basics, prints "hello world"          
        Serial.write(c);                    
        if (c == '\n') {                    

          if (currentLine.length() == 0) {

            client.println("Hello World");
            for (int i = 0; i <= 6; i++) {
              client.println(i);
              delay(10);
            }

            break;
          } else {
            currentLine = "";
          }
        } else if (c != '\r') {
          currentLine += c;
        }
      }
    }

    client.stop();
    Serial.println("client disonnected");
  }
}