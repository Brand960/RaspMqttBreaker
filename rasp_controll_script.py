import subprocess

import serial
import paho.mqtt.client as mqtt
import serial.tools.list_ports
import time
# proc = subprocess.Popen(["pgrep", "-f", __file__], stdout=subprocess.PIPE)
# std = proc.communicate()
# if len(std[0].decode().split()) > 1:
#     exit('Already running')
OPEN_PREFIX_HEX = '550112000000'
CLOSE_PREFIX_HEX = '550111000000'
OPEN_END_HEX = ['0', '69', '6a', '6b', '6c', '6d', '6e', '6f', '70', '71', '72', '73', '74', '75', '76', '77', '78',
                '79', '7a', '7b', '7c', '7d']
CLOSE_END_HEX = ['0', '68', '69', '6a', '6b', '6c', '6d', '6e', '6f', '70', '71', '72', '73', '74', '75', '76', '77',
                 '78', '79', '7a', '7b', '7c']


# port_list = list(serial.tools.list_ports.comports())
#
# if len(port_list) <= 0:
#     print("The Serial port can't find!")
#
# else:
#     port_list_0 = list(port_list[0])
#     port_serial = port_list_0[0]
#     ser = serial.Serial(port_serial, 9500, timeout=60)
#     print("check which port was really used >", ser.name)


def send_COM(data):
    try:
        # 端口，GNU / Linux上的/ dev / ttyUSB0 等 或 Windows上的 COM3 等
        portx = "/dev/ttyUSB0"
        # 波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
        bps = 9500
        # 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
        timex = 5
        # 打开串口，并得到串口对象
        ser = serial.Serial(portx, bps, timeout=timex)
        # 写数据
        # if int(data) == 0:
        #     print(OPEN_PREFIX_HEX + "ffff")
        #     b = int("5501130000000069", 16).to_bytes(8, 'big')
        #     ser.write(b)
        b = int("5501130000000069", 16).to_bytes(8, 'big')
        ser.write(b)
        # else:
        if int(data) < 16:
            data_str = '0' + str(hex(int(data))).replace("0x", "")
        else:
            data_str = str(hex(int(data))).replace("0x", "")
        print(OPEN_PREFIX_HEX + data_str + OPEN_END_HEX[int(data)])
        b = int(OPEN_PREFIX_HEX + data_str + OPEN_END_HEX[int(data)], 16).to_bytes(8, 'big')
        time.sleep(0.2)
        ser.write(b)
        # for i in range(1, 21):
        #     if i == int(data):
        #         pass
        #       #  if i < 16:
        #        #     data_str = '0' + str(hex(int(data))).replace("0x", "")
        #        # else:
        #         #    data_str = str(hex(int(data))).replace("0x", "")
        #         #print(OPEN_PREFIX_HEX + data_str + OPEN_END_HEX[i])
        #         #b = int(OPEN_PREFIX_HEX + data_str + OPEN_END_HEX[i], 16).to_bytes(8, 'big')
        #         #ser.write(b)
        #     else:
        #         if i < 16:
        #             # print(CLOSE_PREFIX_HEX + '0' + str(hex(i)).replace("0x", "") + CLOSE_END_HEX[i])
        #             b = int(CLOSE_PREFIX_HEX + '0' + str(hex(i)).replace("0x", "") + CLOSE_END_HEX[i], 16).to_bytes(
        #                 8, 'big')
        #             # ser.write(b)
        #         else:
        #             # print(CLOSE_PREFIX_HEX + str(hex(i)).replace("0x", "") + CLOSE_END_HEX[i])
        #             b = int(CLOSE_PREFIX_HEX + str(hex(i)).replace("0x", "") + CLOSE_END_HEX[i], 16).to_bytes(8,
        #                                                                                                       'big')
        #         ser.write(b)
        #         # ser.write(bin(int(PREFIX_HEX + data + CLOSE_END_HEX[i], 16)))
        #     time.sleep(0.16)
        ser.close()  # 关闭串口
    except Exception as e:
        print("---异常---：", e)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))


def on_message(client, userdata, msg):
    send_COM(msg.payload)
    print(msg.topic + " " + str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("test", password="test")
client.connect('localhost', 1883, 60)  # 60为keepalive的时间间隔
client.subscribe('BytePayload/test9', qos=0)
client.loop_forever()  # 保持连接
