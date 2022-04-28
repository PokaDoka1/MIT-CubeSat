from mpu6050 import mpu6050
import time
from git import Repo
from picamera import PiCamera
mpu = mpu6050(0x28)

#make sure you can git clone
#git pull 
#generate data
#append data to the file.
#git add the file
#git commit

git_pull()

while True:
    
    print("Temp : "+str(mpu.get_temp()))
    print()
   
    originalDataFile = open("/home/pi/Home/MIT-CubeSat/IMU data/gryo_data.txt", "a")
    
                    
    accel_data = mpu.get_accel_data()
    """print("Acc X : "+str(accel_data['x']))
    print("Acc Y : "+str(accel_data['y']))
    print("Acc Z : "+str(accel_data['z']))
    print()"""
    
    originalDataFile.write("Acc X : "+str(accel_data['x'])
    originalDataFile.write("Acc Y : "+str(accel_data['y']))
    originalDataFile.write("Acc Z : "+str(accel_data['z'])) 

    gyro_data = mpu.get_gyro_data()
    """print("Gyro X : "+str(gyro_data['x']))
    print("Gyro Y : "+str(gyro_data['y']))
    print("Gyro Z : "+str(gyro_data['z']))
    print()
    print("-------------------------------")"""
    time.sleep(5)
    
    originalDataFile.write("Gyro X : "+str(gyro_data['x']))
    originalDataFile.write("Gyro Y : "+str(gyro_data['y']))
    originalDataFile.write("Gyro Z : "+str(gyro_data['z']))
    git_push()

def git_push():
    try:

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
                           
def git_pull():
      repo = Repo('/home/pi/Home/MIT-CubeSat')  # PATH TO YOUR GITHUB REPO
        origin = repo.remote('origin')
        print('pulled repository')
        origin.pull()
