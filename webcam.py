#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import os,sys, os.path
import numpy as np
import math

def nothing(x):
    pass

#cv2.namedWindow('Trackbars')
#cv2.resizeWindow('Trackbars', 300, 300)
#cv2.createTrackbar('L - H', 'Trackbars', 0, 179, nothing)
#cv2.createTrackbar('L - S', 'Trackbars', 0, 255, nothing)
#cv2.createTrackbar('L - V', 'Trackbars', 0, 255, nothing)
#cv2.createTrackbar('U - H', 'Trackbars', 179, 179, nothing)
#cv2.createTrackbar('U - S', 'Trackbars', 255, 255, nothing)
#cv2.createTrackbar('U - V', 'Trackbars', 255, 255, nothing)


def webcam_img(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    # Trackbars
    #l_h = cv2.getTrackbarPos('L - H', 'Trackbars')
    #l_s = cv2.getTrackbarPos('L - S', 'Trackbars')
    #l_v = cv2.getTrackbarPos('L - V', 'Trackbars')
    #u_h = cv2.getTrackbarPos('U - H', 'Trackbars')
    #u_s = cv2.getTrackbarPos('U - S', 'Trackbars')
    #u_v = cv2.getTrackbarPos('U - V', 'Trackbars')
    #lower = np.array([l_h, l_s, l_v])  
    #upper = np.array([u_h, u_s, u_v])
    #track = cv2.inRange(img, lower, upper)

    # Mask Circuferência Esquerda
    left_lower = np.array([34, 32, 93])  
    left_upper = np.array([95, 184, 217])
    left_mask = cv2.inRange(img, left_lower, left_upper)

    # Mask Circuferência Direita
    right_lower = np.array([105, 139, 30])  
    right_upper = np.array([179, 255, 255])
    right_mask = cv2.inRange(img, right_lower, right_upper)

    mask = cv2.bitwise_or(left_mask, right_mask)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)

    # Contorno
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    center_list = []
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 2000:
            cv2.drawContours(frame, [cnt], 0, (0, 0, 0), 3)
            M = cv2.moments(cnt)
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                center_list.append((cx, cy))
                cv2.circle(frame, (cx, cy), 1, (255, 255, 0), 3)
            else:
                cx, cy = 0, 0
        
        # Reta
        if center_list:
            #print(center_list)
            cv2.line(frame, center_list[len(center_list)-1], center_list[len(center_list)-2], (255, 0, 0), 2)
            cv2.line(frame, center_list[len(center_list)-2], (center_list[len(center_list)-1][0], center_list[len(center_list)-2][1]), (255, 0, 0), 2)

            # Angulo
            if len(center_list) >= 2:
                h = int(center_list[len(center_list)-2][0]) - int(center_list[len(center_list)-1][0])
                x = int(center_list[len(center_list)-2][1]) - int(center_list[len(center_list)-1][1])

                y = np.degrees(math.atan(h/x))
                angle = 180 - y - 90
                cv2.putText(frame, str('{:.2f}'.format(angle)), (center_list[len(center_list)-2][0]-50, center_list[len(center_list)-2][1]-50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
        else:
            pass
    return mask

cv2.namedWindow('raw', cv2.WND_PROP_FULLSCREEN)
#cv2.setWindowProperty('raw', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

vc = cv2.VideoCapture(1)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    img = webcam_img(frame)
    
    cv2.imshow('mask', img)
    cv2.imshow('raw', frame)

    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow('raw')
vc.release()