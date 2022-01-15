import serial
import pynmea2

ser = serial.Serial("/dev/ttyS0", 9600)

while True:
	try:
		data = ser.readline()
		msg = pynmea2.parse(data.decode())
		try:
			print(msg)
		except:
			pass
	except:
		pass
