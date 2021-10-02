import cv2
import numpy as np
from gpiozero import Motor
from time import sleep

def move_forward(speed):
    back_motor.forward(speed)
    
def move_backward(speed):
    back_motor.backward(speed)

def move_right(speed):
    front_motor.forward(speed)

def move_left(speed):
    front_motor.backward(speed)
    
def stop_motors(speed):
    back_motor.stop()
    front_motor.stop()

back_motor = Motor(16,19)
front_motor = Motor(26,20)
cap = cv2.VideoCapture(0)

depth = [0,0,0,0,0,0]



cap.set(3, 480)
cap.set(4, 320)


_, frame = cap.read()

_, width, _ = frame.shape

#x_medium = int(cols / 2)
center = int(width / 2)
while True:
    contour = int(2)
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame = cv2.flip(frame,-1)
    # red color
    low_red = np.array([160, 100, 20])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    
    
    _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    
    for cnt in contours:
        contour = int(1)
        x,y,w,h = cv2.boundingRect(cnt)
        
        #x_medium = int((x + x + w) / 2)
        cv2.rectangle(frame, (x, y), (x+w,y+h), (0, 255, 0), 2)
#         object_center = int ((x+x+w) / 2)
#         cv2.line(frame,(object_center,0),(object_center,480),(0,255,0),2)
        
        break
   
    
    cv2.line(frame, (x, y), (x+w,y+h), (0, 255, 0), 2)
    cv2.imshow("Frame", frame)
    cv2.imshow("mask", red_mask)
    key = cv2.waitKey(1) #we need to wait otherwise it will not show up
    
    move_right(0.8)
    move_forward(1)
    
   
    if key == 115:
        break
cap.release()
cv2.destroyAllWindows()
