import time
import bluetooth
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
POWER_STRIP = 23

GPIO.setup(POWER_STRIP, GPIO.OUT)

while(True):
    PORT = 22
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    print("connect...")

    server_socket.bind(("",PORT ))
    server_socket.listen(1)

    client_socket,address = server_socket.accept()

    print("connection success!!")

    while 1:
        try:
            data = client_socket.recv(1024)
            data = data.decode()
            print(data)
            print('\n')
        except KeyboardInterrupt:
            client_socket.close()
            server_socket.close()
            break
        if data == "on":
            GPIO.output(POWER_STRIP, GPIO.HIGH)
        elif data == "off":
            GPIO.output(POWER_STRIP, GPIO.LOW)