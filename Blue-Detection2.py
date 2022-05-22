import cv2
import numpy as np

lower = np.array([90,150,20])
upper = np.array([105,255,255])

video = cv2.VideoCapture(0)

while True:
    success, img = video.read()
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image, lower, upper)

    countours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(countours) != 0:
        for countor in countours:
            if cv2.contourArea(countor)>1500:
                x,y,w,h = cv2.boundingRect(countor)
                cv2.rectangle(img, (x,y), (x + w, y+h), (0,0,255), 3)

    pixels = cv2.countNonZero(mask)
    if pixels > 3:
        print("blue exists")
    else:
        print("not found")




    cv2.imshow("mask", mask)
    cv2.imshow("webcam", img)


    cv2.waitKey(1)
