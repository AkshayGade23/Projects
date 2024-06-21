# import pyfirmata 
# from time import sleep

# DHTTYPE = 

# board = pyfirmata.Arduino('COM4')

# dht = adafruit_dht.DHT11(board.D8)
# smokeA0 = 'A0'
# buzzer = 11
# sensorValue
# led = 7
# ldrPin = A1
# threshold = 40

#  # Change to your port
# print("Start blinking D13")
# while True:
#     board.digital[9].write(1)
#     sleep(1)
#     board.digital[9].write(0)
#     sleep(1)


import serial

ser = serial.Serial('COM4', 9600)  # open serial connection
while True:
    if ser.in_waiting > 0:  # check if there is data in the serial buffer
        message = ser.readline().decode().strip()  # read the data and decode it
        print(message)




# 68 Mayuresh Chavan

