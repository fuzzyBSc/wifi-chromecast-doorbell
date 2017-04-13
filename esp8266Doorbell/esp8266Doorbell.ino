#include <Arduino.h>
#include <Client.h>
#include <ArduinoJson.h>

/*******************************************************************
inspired by: https://github.com/pinae/ESP8266-Dash
 *******************************************************************/


#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
// #include <credentials.h>

//------- Replace the following! ------
const int LED = 2;

const char *mySSID = "TODO";
const char *myPASSWORD = "TODO";
const char *myServer = "192.168.2.50";
const int myPort = 80;
const char *myURL = "http://tori.stig/iot/doorbell.py/handler";

WiFiClient client;

bool sendRequest()
{
  int result = client.connect(myServer, myPort);
  if (!result) {
    Serial.printf("Unable to connect to %s:%d\n", myServer, myPort);
    return false;
  }
  client.printf("POST %s HTTP/1.1\n", myURL);
  client.println("Host:");
  client.println("Content-Length:0");
  client.println("Connection: close");
  client.println("");
  long timeout = millis() + 30000;
  while (millis() < timeout && client.connected()) {
    // Read and log, but ignore response
    while (client.available()) {
      char c = client.read();
      Serial.write(c);
    }
  }
  client.stop();
}

void setup() {
  Serial.begin(115200);
  delay(100);
  Serial.println("Start");

  pinMode(LED, OUTPUT);
  digitalWrite(LED, HIGH);

  // Set WiFi to station mode and disconnect from an AP if it was Previously
  // connected
  WiFi.mode(WIFI_STA);
  //  WiFi.disconnect();
  delay(100);

  // Attempt to connect to Wifi network:
  Serial.print("Connecting Wifi: ");
  Serial.println(mySSID); // your network SSID (name)
  WiFi.begin(mySSID, myPASSWORD); //your WiFi password
  int retries = 50;
  while (WiFi.status() != WL_CONNECTED && --retries > 0) {
    Serial.print(".");
    delay(500);
  }
  if (retries == 0) ESP.restart();
  Serial.println("");
  Serial.print("WiFi connected ");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Connecting IFTTT: ");
  retries = 10;
  digitalWrite(LED, HIGH);
  unsigned long entry = millis();
  while (!sendRequest() && retries > 0) {
    Serial.println((millis() - entry) / 1000.0);
    entry = millis();
    Serial.print("!");
  }
  if (retries > 0)  {
    Serial.println("Successfully sent");
    blinkSuccess();
  }
  else {
    Serial.println("Got no success message.");
    blinkError();
  }
  Serial.println("Going to sleep.");
  shutdown();
}

void loop() {
  yield();
}

void blinkSuccess() {
  for (int i = 4; i < 50; i = (5 * i) >> 2) {
    digitalWrite(LED, HIGH);   // turn the LED off
    delay(10 * i);             // wait
    digitalWrite(LED, LOW);    // turn the LED on
    delay(10 * i);             // wait
  }
}

void blinkError() {
  for (int i = 0; i < 28; i++) {
    digitalWrite(LED, HIGH);   // turn the LED off
    delay(125);                        // wait
    digitalWrite(LED, LOW);    // turn the LED on
    delay(125);                        // wait
  }
}

void shutdown() {
  Serial.println("Shutting down.");
  Serial.println("Going to sleep.");
  //digitalWrite(PORT, LOW); // make sure, the ESP is enabled even if button is released
  ESP.deepSleep(0);
  Serial.println("Sleep failed.");
  while (1) {
    blinkError();
  }
}
