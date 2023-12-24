import json
import time
import requests
import paho.mqtt.client as mqtt

# MQTT Configuration
mqtt_broker = "10.10.10.243"
mqtt_topics = ["83db35f", "839af2e", "e3c52f", "139cfc10"]

# JSON Server Configuration
json_server_url_base = "http://localhost:3000/"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))
    for topic in mqtt_topics:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print("Received message on topic {}: {}".format(msg.topic, payload))
    timeToDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    urlcheck = json_server_url_base + msg.topic
    response = requests.get(urlcheck)
    if response.status_code == 200:
        data = response.json()

    # Check if data is a non-empty list
    if isinstance(data, list) and len(data) > 0:
        status = data[-1].get("status")
        if status == "out":
            data[0]["status"] = "in"
            data[0]["timestamp"] = timeToDate
            data[0].pop("id")
            send_to_json_server(data[0])
        elif status == "in":
            data[0]["status"] = "out"
            data[0]["timestamp"] = timeToDate
            data[0].pop("id")
            send_to_json_server(data[0])
    else:
        print("Invalid data format received from the server.")

def send_to_json_server(data):
    headers = {"Content-Type": "application/json"}
    json_server_url = json_server_url_base + data["topic"]
    response = requests.post(json_server_url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        print("Data sent to JSON server successfully.")
    else:
        print("Failed to send data to JSON server. Status code:", response.status_code)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_broker, 1883, 60)


    client.loop_start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting...")
        client.disconnect()
        client.loop_stop()

if __name__ == "__main__":
    main()
