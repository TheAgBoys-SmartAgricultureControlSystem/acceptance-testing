int nodeid = 0;
int nodestatus = 0;
int rssi = 0;
float lat = 0;
float lng = 0;
int soil = 0;
int analogPin = A3;

void clearandhome(){
  Serial.write(27);       // ESC command
  Serial.print("[2J ");    // clear screen command
  Serial.write(27);
  Serial.print("[0;0H");     // cursor to home command
}
void node_write(int nodeid, int rssi, float lat, float lng, int soil){

  clearandhome();
  
  Serial.write("NodeId:");
  Serial.print(nodeid, HEX);
  Serial.write("#");
  Serial.write("SoilMoisture:");
  Serial.print(soil);
  Serial.write("#");
  Serial.write("Latitude:");
  Serial.write("40.011234");
  Serial.write("#");
  Serial.write("Longitude:");
  Serial.write("-105.261234");
  Serial.write("#");
  Serial.write("RSSI:");
  Serial.print(rssi);
  Serial.println('\n');
  
  delay(490);
}

void node0(){
 nodeid = 0x10; // node id
 rssi = random(-150, 0);  // rssi can be from noise floor to 0
 lat = -105.271234; // DLC building
 lng = 40.011234; // DLC building
 soil = analogRead(analogPin); // percentage from 0 to 4095
 node_write(nodeid, rssi, lat, lng, soil);
}

void node1(){
 nodeid = 0x11; // node id
 rssi = random(-150, 0);  // rssi can be from noise floor to 0
 lat = -105.261234; // DLC building
 lng = 40.011234; // DLC building
 soil = analogRead(analogPin); // percentage from 0 to 100
 node_write(nodeid, rssi, lat, lng, soil);
}

void node2(){
 nodeid = 0x12; // node id
 rssi = random(-150, 0);  // rssi can be from noise floor to 0
 lat = -105.261234; // DLC building
 lng = 40.011234; // DLC building
 soil = analogRead(analogPin); // percentage from 0 to 100
 node_write(nodeid, rssi, lat, lng, soil);
}

void node3(){
 nodeid = 0x13; // node id
 rssi = random(-150, 0);  // rssi can be from noise floor to 0
 lat = -105.261234; // DLC building
 lng = 40.011234; // DLC building
 soil = analogRead(analogPin); // percentage from 0 to 100
 node_write(nodeid, rssi, lat, lng, soil);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while(!Serial){
    ;
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  node0();
  delay(5000);
  node1();
  delay(5000);
  node2();
  delay(5000);
  node3();
  delay(5000);
}







