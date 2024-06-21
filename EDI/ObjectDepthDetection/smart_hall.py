import time
import serial
from pyfirmata import Arduino, util
from dht11 import DHT11

board = Arduino('COM3')
it = util.Iterator(board)
it.start()

dht = DHT11(pin=8)
smokeA0 = 1
buzzer = 11
sensorValue = 0
ldrPin = 0
led = 7
threshold = 100
pwm = 9

degree = [  [0b00011],
  [0b00011],
  [0b00000],
  [0b00000],
  [0b00000],
  [0b00000],
  [0b00000],
  [0b00000]
]

board.analog[pwm].write(10)
board.digital[buzzer].mode = board.OUTPUT
board.digital[smokeA0].mode = board.INPUT
board.digital[led].mode = board.OUTPUT

ser = serial.Serial('COM4', 9600)
time.sleep(2)

def get_proper_regions(data):
  regions = data.split(',')
  proper_regions = [0, 0, 0]

  for i in range(len(regions)):
    region = int(regions[i])
    if region > 0 and region < 3:
      proper_regions[region] = 1

  return proper_regions

while True:
  if ser.in_waiting > 0:
    incoming = ser.readline().decode().strip()
    print(incoming)
    proper_regions = get_proper_regions(incoming)

  temperature = dht.read_temperature()
  humidity = dht.read_humidity()

  if proper_regions[1]:
    if temperature < 20:
      board.analog[pwm].write(0)
      time.sleep(1)
    elif temperature > 20 and temperature < 25:
      board.analog[pwm].write(0.2)
      time.sleep(1)
    elif temperature > 25 and temperature < 30:
      board.analog[pwm].write(0.4)
      time.sleep(1)
    elif temperature > 30 and temperature < 32:
      board.analog[pwm].write(0.6)
      time.sleep(1)
    elif temperature > 32 and temperature < 40:
      board.analog[pwm].write(0.8)
      time.sleep(1)
    elif temperature > 40:
      board.analog[pwm].write(1.0)
      time.sleep(1)

  sensorValue = board.analog[smokeA0].read()
  if sensorValue > 350:
    print("Smoke detected!!!, Value:", sensorValue)
    board.digital[buzzer].write(1)
  else:
    print("Smoke not detected!, Value:", sensorValue)
    board.digital[buzzer].write(0)

  time.sleep(1)

  ldrdata = board.analog[ldrPin].read()
  print("Light intensity =", ldrdata)
  if ldrdata <= threshold:
    board.digital[led].write(1)
  else:
    board.digital[led].write(0)

  time.sleep(1)