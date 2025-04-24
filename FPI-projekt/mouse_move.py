# Importing Libraries 
import serial 
import time 
import keyboard
import mouse 
import random as rand
import threading


arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1) 
time.sleep(2)  # wait for Arduino to reset

# Initial values
CPR_threshold = 0
mouse_death = -1
x = y = z = piezo = 0
accel = 100
animation_speed = 1
  
# Reading serial data and assigning values
def read_serial_data():
    global x, y, z, piezo

    while True:
        data = arduino.readline().decode().strip()
        if ':' in data:
            print(f'Data: {data}')
            try:
                label, value = data.split(':')
                value = float(value)  # Or int(), if you're sending integers
                if label == "x":
                    x = value
                elif label == "y":
                    y = value
                elif label == "z":
                    z = value
            except ValueError:
                print(f"Could not convert value: {data}")

# Initializing background thread
b_thread = threading.Thread(target=read_serial_data, daemon=True)
b_thread.start()


while True: 
    time.sleep(1)

    # Stop program
    if keyboard.is_pressed("ctrl"):
        break

    # Check if mouse is dead
    if mouse_death == 2:
        mouse.move(1000, 1000, True, 1)
        if piezo >= CPR_threshold:
            print("Bla")
            
    # Calculate new random number to check if mouse is dead
    mouse_death = rand.randint(1,10)
    print(f'Mouse death int:{mouse_death}')

    # Moving mouse
    mouse.move(x*accel, y*accel, absolute=False, duration=animation_speed)

    # Printing gyro data
    print(f'x: {x}, y: {y}, z: {z}, piezo {piezo}')


print("Stopped")

'''
    if data == "x":
        while data == "x":
            data = get_direction() 
        
        try:
            data = int(data)
            mouse.move(data, 0, False, 1)

        except ValueError:
            continue
    
    if data == "y":
        while data == "y":
            data = get_direction() 

        try:
            data = int(data)
            mouse.move(0, data, False, 1)
        except ValueError:
            continue
'''