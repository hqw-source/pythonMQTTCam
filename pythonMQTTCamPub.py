# server_mqtt.py （运行在主机）
import cv2
import paho.mqtt.client as mqtt
import numpy as np
import time

# MQTT 连接参数（替换为你的参数）
CLIENT_ID = "k12vvXWjR3e.mytest|securemode=2,signmethod=hmacsha256,timestamp=1744271990317|"
USERNAME = "mytest&k12vvXWjR3e"
PASSWORD = "aa6f7146815e9a6aabbdb6f962db812a1b3c712f043d08f126dc5ecd5c794bf1"
MQTT_HOST = "iot-06z00iu8stlk7l4.mqtt.iothub.aliyuncs.com"
PORT = 1883

# 发布和订阅的 Topic（需在阿里云平台提前创建并授权）
PUB_TOPIC = "/broadcast/k12vvXWjR3e/test"


# 初始化摄像头
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 降低分辨率
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# MQTT 连接回调
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("成功连接到阿里云 MQTT！")
    else:
        print(f"连接失败，错误码: {rc}")

# 创建 MQTT 客户端
client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect

# 连接到服务器
client.connect(MQTT_HOST, PORT, 60)
client.loop_start()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 压缩图像为 JPEG（调整质量控制大小）
        _, img_encoded = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        data = img_encoded.tobytes()

        # 检查数据大小（阿里云限制 256KB）
        if len(data) > 256 * 1024:
            print("警告：图像超过 256KB，跳过此帧")
            continue

        # 发布到 Topic
        client.publish(PUB_TOPIC, payload=data, qos=1)
        print(f"已发送一帧，大小: {len(data)/1024:.2f} KB")
        time.sleep(0.3)  # 控制帧率

except KeyboardInterrupt:
    cap.release()
    client.disconnect()
    print("已断开连接")