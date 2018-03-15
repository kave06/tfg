#define RELAY 7
int value=0;

void setup(){
      Serial.begin(9600);
      pinMode(RELAY, OUTPUT);
      digitalWrite (RELAY, LOW);
      Serial.println("Connection established...");
}

void loop(){
    while (Serial.available()){
           value = Serial.read();
    }

    if (value == '1')
        digitalWrite (RELAY, HIGH);

    else if (value == '0')
        digitalWrite (RELAY, LOW);
}