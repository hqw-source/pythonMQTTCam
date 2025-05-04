# client_mqtt.py （运行在虚拟机）
import paho.mqtt.client as mqtt
import cv2
import numpy as np

# MQTT 连接参数（与服务端相同或另一设备的三元组）
CLIENT_ID = "k12vvXWjR3e.mytest1|securemode=2,signmethod=hmacsha256,timestamp=1744272650748|"
USERNAME = "mytest1&k12vvXWjR3e"
PASSWORD = "7bb1116d64d473726f25cdef548e3fbfcb70616907c635ced6e3e95ceff412bf"
MQTT_HOST = "iot-06z00iu8stlk7l4.mqtt.iothub.aliyuncs.com"
PORT = 1883

SUB_TOPIC = "/broadcast/k12vvXWjR3e/test"  # 需与服务端 PUB_TOPIC 一致

# MQTT 消息回调
def on_message(client, userdata, msg):
    try:
        # 解码图像
        img = cv2.imdecode(np.frombuffer(msg.payload, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is not None:
            cv2.imshow("MQTT Camera Stream", img)
            cv2.waitKey(1)
    except Exception as e:
        print(f"解码错误: {e}")

# 初始化 MQTT
client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)
client.username_pw_set(USERNAME, PASSWORD)
client.on_message = on_message

# 连接并订阅
client.connect(MQTT_HOST, PORT, 60)
client.subscribe(SUB_TOPIC, qos=1)
print("等待接收图像...")

try:
    client.loop_forever()
except KeyboardInterrupt:
    client.disconnect()
    cv2.destroyAllWindows()