import serial
import pynmea2

ser = serial.Serial("/dev/ttyS0", 9600)

lat = 0
lng = 0
sats = 0
speed = 0
course = 0

while True:
    try:
        data = ser.readline()
        data = data.decode()
#        print(data)

        if data.split(",")[0] == "$GNGGA":
            lat = float(data.split(",")[2])/100 + 0.193328
            lng = float(data.split(",")[4])/100 + 0.12404
            sats = float(data.split(",")[7])
            
        elif "VTG" in data.split(",")[0][1:]:
            speed = data.split(",")[5]
            course = float(data.split(",")[1])

        print(lat, lng, sats, speed, course)
    except:
       pass
