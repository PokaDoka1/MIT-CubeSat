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
import numpy as np
import cv2
from mpu6050 import mpu6050
import time
from git import Repo
from picamera import PiCamera
mpu = mpu6050(0x28)

green = [227,115,223]
dog = []
diff = 100



# ur mom

#setup imu and camera
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)
camera = PiCamera()

#bonus: function for uplodaing image to Github
def git_push_image():
    try:
        repo = Repo('/home/cubesat/Home/MIT-CubeSat')
        repo.git.add('Images')  # PATH TO YOUR IMAGES FOLDER WITHIN YOUR GITHUB REPO
        repo.index.commit('New Photo')
        origin = repo.remote('origin')
        origin.push()
        print('pushed image with plastic to github' + "\n")
    except:
        print('Couldnt upload to git')
        
def git_push_data():
    try:
        repo = Repo('/home/cubesat/Home/MIT-CubeSat')
        repo.git.add('IMU_Data')
        repo.index.commit('Gyro Data')
        origin = repo.remote('origin')
        print("push imu data" + "\n")
        origin.push()
    except:
        print('Couldnt upload to git')
        
def git_pull():
      repo = Repo('/home/cubesat/Home/MIT-CubeSat')  # PATH TO YOUR GITHUB REPO
      origin = repo.remote('origin')
      print('pulled repository')
      origin.pull()
    
git_pull()

loopCount = 0

#SET THRESHOLD
threshold = 5.62901
photoPauseTime=1
loopPauseTime = 1

#read acceleration
while True:
        print("Temp : "+str(mpu.get_temp()))
        print()

        originalDataFile = open("/home/cubesat/Home/MIT-CubeSat/IMU_Data/gyro_data.txt", "a")


        accel_data = mpu.get_accel_data()
        print("Acc X : "+str(accel_data['x']))
        print("Acc Y : "+str(accel_data['y']))
        print("Acc Z : "+str(accel_data['z']))
        print()

        originalDataFile.write("Acc X : "+str(accel_data['x']) + "\n")
        originalDataFile.write("Acc Y : "+str(accel_data['y'])+ "\n")
        originalDataFile.write("Acc Z : "+str(accel_data['z'])+ "\n")

        gyro_data = mpu.get_gyro_data()
        print("Gyro X : "+str(gyro_data['x']))
        print("Gyro Y : "+str(gyro_data['y']))
        print("Gyro Z : "+str(gyro_data['z']))
        print()
        print("-------------------------------")


        originalDataFile.write("Gyro X : "+str(gyro_data['x'])+ "\n")
        originalDataFile.write("Gyro Y : "+str(gyro_data['y'])+ "\n")
        originalDataFile.write("Gyro Z : "+str(gyro_data['z'])+ "\n")
        loopCount+=1
        if (loopCount % 30 == 0):
            git_push_data()    


        
        accelX, accelY, accelZ = sensor.acceleration

        #CHECK IF READINGS ARE ABOVE THRESHOLD
        accel = sqrt(accelX**2 + accelY**2 + accelZ**2)

        #TAKE/SAVE/UPLOAD A PICTURE
        if accel>threshold:
            print("Taking picture in 3 seconds")
            sleep(photoPauseTime)
            name = "Lady Lion Stemmers" #Last Name, First Initial

            if name:
                t=time.strftime("_%H%M%S") #current time string
                imgname = ('/home/cubesat/Home/MIT-CubeSat/Images/blah') #chagne didrectory to your folder
                cat = camera.capture(imgname + ".jpg")
                img = cv2.imread('/home/cubesat/Home/MIT-CubeSat/Images/blah.jpg')
                for color in green:
                    if diff + color > 255:
                         dog.append(255)
                    else:
                        dog.append(diff + color)

                # Be aware that opencv loads image in BGR format,
                # that's why the color values have been adjusted here:
                boundaries = [([green[2], green[1], green[0]], [dog[2],dog[1], dog[0]])]

                # Scale your BIG image into a small one:
                scalePercent = 0.3

                # Calculate the new dimensions
                width = int(img.shape[1] * scalePercent)
                height = int(img.shape[0] * scalePercent)
                newSize = (width, height)
                img = cv2.resize(img, newSize, None, None, None, cv2.INTER_AREA)
                for (lower, upper) in boundaries:
                    # You get the lower and upper part of the interval:
                    lower = np.array(lower, dtype=np.uint8)
                    upper = np.array(upper, dtype=np.uint8)

                    # cv2.inRange is used to binarize (i.e., render in white/black) an image
                    # All the pixels that fall inside your interval [lower, uipper] will be white
                    # All the pixels that do not fall inside this interval will
                    # be rendered in black, for all three channels:
                    mask = cv2.inRange(img, lower, upper)

                    # Now, you AND the mask and the input image
                    # All the pixels that are white in the mask will
                    # survive the AND operation, all the black pixels
                    # will remain black
                    output = cv2.bitwise_and(img, img, mask=mask)

                    # You can use the mask to count the number of white pixels.
                    # Remember that the white pixels in the mask are those that
                    # fall in your defined range, that is, every white pixel corresponds
                    # to a green pixel. Divide by the image size and you got the
                    # percentage of green pixels in the original image:
                    ratio_green = cv2.countNonZero(mask)/(img.size/3)

                    # This is the color percent calculation, considering the resize I did earlier.
                    colorPercent = (ratio_green * 100)

                    # Print the color percent, use 2 figures past the decimal point

                    #print('blue pixel percentage:', np.round(colorPercent, 2))

                    if colorPercent > 98:
                        print(f"Water most likely detected with {colorPercent:.2f}% ")
                        git_push_image()
                    else:
                        print(f"plastic detected with {100 - colorPercent:.2f}%")
                        git_push_image()

        sleep(loopPauseTime)

