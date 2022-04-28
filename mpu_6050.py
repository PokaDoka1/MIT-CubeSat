from mpu6050 import mpu6050
import time
from git import Repo
from picamera import PiCamera
mpu = mpu6050(0x28)

while True:
    print("Temp : "+str(mpu.get_temp()))
    print()

    accel_data = mpu.get_accel_data()
    """print("Acc X : "+str(accel_data['x']))
    print("Acc Y : "+str(accel_data['y']))
    print("Acc Z : "+str(accel_data['z']))
    print()"""

    gyro_data = mpu.get_gyro_data()
    """print("Gyro X : "+str(gyro_data['x']))
    print("Gyro Y : "+str(gyro_data['y']))
    print("Gyro Z : "+str(gyro_data['z']))
    print()
    print("-------------------------------")"""
    time.sleep(1
    git_push()

def git_push():
    try:
        #halps
        repo = Repo('/home/pi/Home/MIT-CubeSat')  # PATH TO YOUR GITHUB REPO
        #halps
        repo.git.add('IMU Data')  # PATH TO YOUR IMAGES FOLDER WITHIN YOUR GITHUB REPO
        repo.index.commit('Gyro Data')
        print('made the commit')
        origin = repo.remote('origin')
        print('added remote')
        origin.push()
        print('pushed changes')
    except:
        print('Couldnt upload to git')
