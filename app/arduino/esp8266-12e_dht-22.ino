#include <DHT.h>

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

#define DHTPIN 5
#define DHTTYPE DHT22
#define SENSOR 1

DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "JohnColtrane";
const char* password = "comoTeLlamas?";

const int led = 13;

ESP8266WebServer server(80);


void handleRoot() {
  digitalWrite(led, 1);
  server.send(200, "text/plain", "hello from esp8266!");
  digitalWrite(led, 0);
}

void handleAmbient() {

  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
      Serial.println("Failed to read from DHT sensor!");
    }

  String t_str = String(t);

  String jsonResponse = "{\"id\": 1,\"sensor\": \"dht-22\",\"data\":{\"temperature\": ";
  jsonResponse = String(jsonResponse + t);
  jsonResponse = String(jsonResponse + ",\"humidity\": ");
  jsonResponse = String(jsonResponse + h);
  jsonResponse = String(jsonResponse + "}}");

  server.send(200, "application/json", jsonResponse);
 }

void handleNotFound(){
  digitalWrite(led, 1);
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET)?"GET":"POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i=0; i<server.args(); i++){
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
  digitalWrite(led, 0);
}

void setup(void){

  dht.begin();
  pinMode(led, OUTPUT);
  digitalWrite(led, 0);

  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleRoot);

  server.on("/amb", handleAmbient);

  server.on("/inline", [](){
    server.send(200, "text/plain", "this works as well");
  });

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void){
  server.handleClient();
}