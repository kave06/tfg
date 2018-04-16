#include <DHT.h>
#include <Adafruit_Sensor.h>
#include <SoftwareSerial.h>

#define DHTPIN 2
#define DHTTYPE DHT22
#define SENSOR 1

DHT dht(DHTPIN, DHTTYPE);
SoftwareSerial bt (5,6);

float humidity;
float temperature;

void setup(){
    dht.begin();
    bt.begin(9600);
}

void loop(){

    humidity = dht.readHumidity();
    temperature = dht.readTemperature();


    bt.print(" ");
    bt.print(SENSOR);
    bt.print(" T: ");
    bt.print(temperature);
    bt.print(" ");
    bt.print(humidity);
    bt.print(" :H ");
    // cada 10 seg
    delay(60000);
}
