#include <ESP8266WiFi.h>
#include <MFRC522.h>
#include <Servo.h>
#include <PubSubClient.h>

// กำหนดพิน
#define RST_PIN D1       // พิน Reset สำหรับโมดูล RFID MFRC522
#define SS_PIN D2        // พิน Slave Select สำหรับโมดูล RFID MFRC522
#define SERVO_PIN D3     // พินที่ต่อ Servo

// ข้อมูลการเชื่อมต่อ WiFi
const char* ssid = "pinsudaa";
const char* password = "123456zx";

// การกำหนดค่า MQTT broker
const char* mqttServer = "10.10.10.243";  // ที่อยู่ IP ของ MQTT broker

// สร้างอ็อบเจ็กต์สำหรับไลบรารีที่จำเป็น
WiFiClient wifiClient;
PubSubClient client(wifiClient);
MFRC522 mfrc522(SS_PIN, RST_PIN);
Servo myServo;

void setup() {
  Serial.begin(115200);
  delay(10);

  Serial.println();
  Serial.println("กำลังเชื่อมต่อ WiFi...");

  // เชื่อมต่อ WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("เชื่อมต่อ WiFi สำเร็จ");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // กำหนดค่าการสื่อสาร SPI และโมดูล RFID MFRC522
  SPI.begin();
  mfrc522.PCD_Init();
  myServo.attach(SERVO_PIN);

  // หมุน Servo ไปที่ตำแหน่งเริ่มต้น (160 องศา)
  myServo.write(160);

  // กำหนดค่า MQTT client เพื่อเชื่อมต่อกับ broker
  client.setServer(mqttServer, 1883);
}

void loop() {
  // ตรวจสอบว่ามีการ์ด RFID ใหม่หรือไม่
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    delay(50);
    return;
  }

  Serial.println("ตรวจพบ RFID!");

  // อ่าน UID ของการ์ด RFID
  String readUID = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    readUID += String(mfrc522.uid.uidByte[i], HEX);
  }
  readUID.trim();

  Serial.print("UID: ");
  Serial.println(readUID);

  // หมุน Servo ไปที่ 0 องศา
  myServo.write(0);

  // ส่ง UID ไปยัง MQTT broker เป็นข้อความ
  String mqttUidTopic = readUID;
  client.connect("ESP8266Client");
  client.publish(mqttUidTopic.c_str(), "Detect");

  delay(3000);  // หน่วงเวลาเพื่อป้องกันการอ่านซ้ำ

  // หมุน Servo กลับไปที่ตำแหน่งเริ่มต้น (160 องศา)
  myServo.write(160);
}
