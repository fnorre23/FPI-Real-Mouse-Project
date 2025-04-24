# Importing Libraries 
import serial 
import time 
import keyboard
import mouse 
import random as rand
import threading
from playsound import playsound

arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1) 
time.sleep(2)  # wait for Arduino to reset

# Initial values

# Mouse death and revival
CPR_threshold = 1
mouse_death = -1
revival_threshold = 2
cpr_counter = 0
mouse_death_cap = 10

# Sound

death_sound_has_played = False
death_sound = 'C:\\Users\\frede\\source\\repos\\MED4\\FPI\\FPI-projekt\\mouse-squeak.wav'
revival_sound = 'C:\\Users\\frede\\source\\repos\\MED4\\FPI\\FPI-projekt\\nice-mouse-cartoon.wav'


# Mouse movement
x = y = z = piezo = 0
animation_speed = 1
mult = 100

  
# Reading serial data and assigning values
def read_serial_data():
    global x, y, z, piezo

    while True:
        data = arduino.readline().decode().strip()
        if ':' in data:
            #print(f'Data: {data}')
            try:
                label, value = data.split(':')
                value = float(value) * mult  # Or int(), if you're sending integers
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

    piezo = rand.randint(0,10)

    # Check if mouse is dead
    if mouse_death == 2:

        if death_sound_has_played == False:
            
            # Playing death sound
            playsound(death_sound)

            # Making sure it can't play again until it has revived
            death_sound_has_played = True

        # Moving mouse to bottom of screen
        mouse.move(1000, 1000, True, 1)

        # If hit is good enough, add to revival counter    
        if piezo >= CPR_threshold:
            cpr_counter += 1
            print("Added +1 to CPR counter!")

        # If counter is sufficient, revive and continue, else, stay in mouse is dead loop
        if cpr_counter >= revival_threshold:
            
            print('Revived!')
            playsound(revival_sound)

            # Resetting death sound
            death_sound_has_played = False

            # Resetting counter
            cpr_counter = 0
        else:
            continue    
        
    # Calculate new random number to check if mouse is dead
    mouse_death = rand.randint(1,mouse_death_cap)
    print(f'Mouse death int:{mouse_death}')

    # Moving mouse
    mouse.move(x, y, absolute=False, duration=animation_speed)

    # Printing gyro data
    #print(f'x: {x}, y: {y}, z: {z}, piezo {piezo}')


print("Stopped")