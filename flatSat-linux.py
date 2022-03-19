#complete CAPITALIZD SECTIONS

#ARUTHOR: Rachel Fernandez
#DATE: 3/18/2022

#import libraries
from numpy import sqrt
import math
import time
from time import sleep
import os
import board
import busio
import adafruit_bno055
from git import Repo
from picamera import PiCamera

#setup imu and camera
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)
camera = PiCamera()

#bonus: function for uplodaing image to Github
def git_push():
    try:
        #halps
        repo = Repo('/home/pi/Home/MIT-CubeSat')  # PATH TO YOUR GITHUB REPO
        #halps
        repo.git.add('Images')  # PATH TO YOUR IMAGES FOLDER WITHIN YOUR GITHUB REPO
        repo.index.commit('New Photo')
        print('made the commit')
        origin = repo.remote('origin')
        print('added remote')
        origin.push()
        print('pushed changes')
    except:
        print('Couldnt upload to git')

#SET THRESHOLD
threshold = 5.62901
photoPauseTime=5
loopPauseTime = 5

#read acceleration
while True:
        accelX, accelY, accelZ = sensor.acceleration

        #CHECK IF READINGS ARE ABOVE THRESHOLD
        accel = sqrt(accelX**2 + accelY**2 + accelZ**2)

        #TAKE/SAVE/UPLOAD A PICTURE
        if accel>threshold:
            print("Taking picture in 5 seconds")
            sleep(photoPauseTime)
            name = "Lady Lion Stemmers" #Last Name, First Initial

            if name:
                t=time.strftime("_%H%M%S") #current time string
                imgname = ('home/pi/Home/MIT-CubeSat/Images/%s%s') #chagne didrectory to your folder
                img = camera.capture(imgname+ ".jpg")
                git_push()

        sleep(loopPauseTime)
