import RPi.GPIO as GPIO
import os
from time import sleep
import mysql.connector
from http.server import BaseHTTPRequestHandler, HTTPServer
import drivers

coi = 26  # coi canh bao
auto0 = 23  # on/off auto
maybom = 24  # on/off may bom
automay = 22  # auto may bom
wsoil = 25  # den canh bao soil
rem = 27  # mai che

import Adafruit_DHT
sensor = Adafruit_DHT.DHT11

pin = 6  # pin sig dht11

import serial

display = drivers.Lcd()

db = mysql.connector.connect(
    host="127.0.0.1",  # Thay thế bằng thông tin kết nối của bạn
    user="root",
    password="654321",
    database="dht_data"
)
cursor = db.cursor()

host_name = '172.20.10.2'  # IP Address of Raspberry Pi
host_port = 8555


def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(pin, GPIO.IN)
    GPIO.setup(coi, GPIO.OUT)
    GPIO.setup(auto0, GPIO.OUT)
    GPIO.setup(maybom, GPIO.OUT)
    GPIO.setup(automay, GPIO.OUT)
    GPIO.setup(wsoil, GPIO.OUT)
    GPIO.setup(rem, GPIO.OUT)


def getTemperature():
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
    return temp


def getDHT11Data():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return humidity, temperature


class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        html = '''
  <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
<style>
    .container {{
        width: 100%;
        height: 100vh;
    }}
    .minhngu {{
        /* position: absolute; */
        background-color: #1fb1aa;
        width: 100%;
        height: 200px;
        display: flex;
        align-items: center;
        flex-direction: column;
    }}
    .minhngu1 {{
        position: relative;
        margin-top: 30px;
        display: flex;
        justify-content: center;
        margin-bottom: 15px;

    }}
    .minhngu1 span {{
        color: white;
        font-size: 30px;
        font-style: normal;
    }}
    .minhngu2 span {{
        display: flex;
        justify-content: center;
        color: white;
        font-style: normal;
    }}
    .dungngu {{
        position: relative;
        margin-top: 30px;
        width: 100%;
        display: flex;
        background-color: white;
        font-style: normal;
        bottom: 20px;
    }}
    .dungngu ul {{
        width: 100%;
        display: flex;
        justify-content: start;
    }}
    .dungngu li {{
        height: 25px;
        padding: 10px;
    }}
    .soangnu {{
        height: 60%;
        display: flex;
        width: 100%;
        margin-top: 50px;
    }}
    img {{
        width: 200px;
    }}
    .tuoicay {{
        flex: 33%;
        flex-direction: column;

    }}
    .keorem {{
        flex: 33%;
        flex-direction: column;

    }}
    .img1 {{
        display: flex;
        justify-content: center;
    }}
    .keorem1 {{
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }}
    .hienthithongso {{
        flex: 34%;
    }}
    .onn {{
        width: 50px;
        background-color: rgb(0, 255, 0);
    }}
    .off {{
        width: 50px;
        background-color: red;
    }}
    .text {{
        display: flex;
        justify-content: center;
        margin-bottom: 30px;
        font-size: 30px;
    }}
    .footer {{
        width: 100%;
        margin-top: 20px;
        color: white;
        background-color: #1fb1aa;
        height: 10%;
        display: flex;
        align-items: center;
    }}
    .footer span {{
        margin-left: 50px;
    }}
</style>
</head>
<body>
<div class="container">
    <div class="minhngu">
        <div class="minhngu1">
            <span>WELCOME</span>
        </div>
        <div class="minhngu2">
            <span>
                This is a simple example with embedded CSS.
            </span>
        </div>
        <div class="dungngu">
            <ul type="none">
                <li>Trang Chủ</li>
                <li>Trang Chủ</li>
                <li>Trang Chủ</li>
            </ul>
        </div>
    </div>
    <form action="/" method="POST">
        <div class="soangnu">
            <div class="tuoicay">
                <div class="text">
                    <span>Máy Bơm Tự Động</span>
                </div>
                <div class="img1">
                    <img src="https://i.pinimg.com/736x/34/f7/44/34f7447cf32cc155bc3d479c4cffa49d.jpg" alt="">
                </div>
                <div class="keorem1">
                    <input class="onn" type="submit" name="submit" value="on">
                    <input class="off" type="submit" name="submit" value="off">
                </div>
            </div>
            <div class="keorem">
                <div class="text">
                    <span>Bật Tắt Máy bơm</span>
                </div>
                <div class="img1">
                    <img src="https://i.pinimg.com/originals/3c/da/db/3cdadba7d18b913f39fc5b49d55447e4.png"
                        alt="">
                </div>
                <div class="keorem1">
                    <span>
                        <input class="onn" type="submit" name="submit" value="ON">
                        <input class="off" type="submit" name="submit" value="OFF">
                    </span>
                </div>
            </div>
            <div class="hienthithongso">
                <p>Current GPU temperature is {}</p>
                <p>Current DHT11 data - Humidity: {}%, Temperature: {}°C</p>
                <input type="submit" name="submit" value="SHOW">
            </div>
        </div>
    </form>
    <div class="footer">
        <span>
            Good Morning@@
        </span>
    </div>
</div>
</body>
</html>
        '''
        temp = getTemperature()
        humidity, temperature = getDHT11Data()
        self.do_HEAD()
        self.wfile.write(html.format(temp[5:], humidity, temperature).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = post_data.split("=")[1]

        setupGPIO()
        humidity, temperature = getDHT11Data()
        # 1 on may bom tu dong
        if post_data == 'on':
            GPIO.output(auto0, GPIO.LOW)
            print("Bat auto may bom")

            self._redirect('/')  # Redirect back to the root url
        # 2 off may bom tu dong
        if post_data == 'off':
            GPIO.output(auto0, GPIO.HIGH)
            print("Tat auto may bom")
            self._redirect('/')  # Redirect back to the root url
        # 3 on may bom
        if post_data == 'ON':
            GPIO.output(maybom, GPIO.HIGH)
            print("ON may bom")
            self._redirect('/')  # Redirect back to the root url
        # 4 off may bom
        if post_data == 'OFF':
            GPIO.output(maybom, GPIO.LOW)

            print("OFF may bom")
            self._redirect('/')  # Redirect back to the root url
        if post_data == 'SHOW':
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
            self._redirect('/')  # Redirect back to the root url
        if humidity < 65 and temperature > 30 and temperature < 32:  # temp > 40 C ( mô phỏng > 30 )
            GPIO.output(rem, GPIO.HIGH)
        elif temperature > 32:  # temp > 50 C ( mô phỏng > 35)
            GPIO.output(rem, GPIO.HIGH)
            GPIO.output(coi, GPIO.HIGH)
        else:
            GPIO.output(coi, GPIO.LOW)
            GPIO.output(rem, GPIO.LOW)

        # save Mysql
        # Lưu giá trị từ cảm biến DHT11 vào cơ sở dữ liệu
        cursor.execute("INSERT INTO dht_data (humidity, temperature) VALUES (%s, %s)", (humidity, temperature))
        db.commit()
        self._redirect('/')  # Redirect back to the root URL


if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        # http_server.server_close()
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.flush()
        display.lcd_clear()
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()

                # print((int(line))/10)
                mois = int(line)
                print(mois, "%")
                humidity, temperature = getDHT11Data()
                display.lcd_display_string(f"Tem={temperature}C_Hum={humidity}%", 1)
                display.lcd_display_string(f"Soil = {mois} %", 2)
                if mois < 60:
                    GPIO.output(automay, GPIO.HIGH)
                    GPIO.output(wsoil, GPIO.HIGH)
                else:
                    GPIO.output(automay, GPIO.LOW)
                    GPIO.output(wsoil, GPIO.LOW)
#xxsd
