# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 01:04:44 2020

@author: hp
"""
import time
import random
from datetime import datetime
import cv2
from face_detector import get_face_detector, find_faces
from face_landmarks import get_landmark_model, detect_marks, draw_marks
from save_image_to_log import save_image_log



# WAIT = random.randint(3,10)
WAIT = 5

font = cv2.FONT_HERSHEY_SIMPLEX

class MouthOpenDetector:
    def __init__(self):
        self.face_model = get_face_detector()
        self.landmark_model = get_landmark_model()
        self.outer_points = [[49, 59], [50, 58], [51, 57], [52, 56], [53, 55]]
        self.d_outer = [0]*5
        self.inner_points = [[61, 67], [62, 66], [63, 65]]
        self.d_inner = [0]*3
    
    
    def get_mask(self,cap):
        while(True):
            ret, img = cap.read()
            rects = find_faces(img, self.face_model)
            for rect in rects:
                shape = detect_marks(img, self.landmark_model, rect)
                draw_marks(img, shape)
                cv2.putText(img, 'Press r to record Mouth distances', (30, 30), font,
                            1, (0, 255, 255), 2)
                cv2.imshow("Output", img)
            if cv2.waitKey(1) & 0xFF == ord('r'):
                for i in range(100):
                    for i, (p1, p2) in enumerate(self.outer_points):
                        self.d_outer[i] += shape[p2][1] - shape[p1][1]
                    for i, (p1, p2) in enumerate(self.inner_points):
                        self.d_inner[i] += shape[p2][1] - shape[p1][1]
                break
        cv2.destroyWindow("Output")
        self.d_outer[:] = [x / 100 for x in self.d_outer]
        self.d_inner[:] = [x / 100 for x in self.d_inner]
        # return d_outer, d_inner


    def detect_mouth(self,cap):
        while (True):
            ret, img = cap.read()
            rects = find_faces(img, self.face_model)
            for rect in rects:
                shape = detect_marks(img, self.landmark_model, rect)
                cnt_outer = 0
                cnt_inner = 0
                draw_marks(img, shape[48:])
                for i, (p1, p2) in enumerate(self.outer_points):
                    if self.d_outer[i] + 3 < shape[p2][1] - shape[p1][1]:
                        cnt_outer += 1 
                for i, (p1, p2) in enumerate(self.inner_points):
                    if self.d_inner[i] + 2 <  shape[p2][1] - shape[p1][1]:
                        cnt_inner += 1
                if cnt_outer > 3 and cnt_inner > 2:
                    print('Mouth open')
                    cv2.putText(img, 'Mouth open', (30, 30), font,
                            1, (0, 255, 255), 2)
                    cheatingtype = "MOUTH_OPEN"
                    save_image_log(img,datetime.now(), cheatingtype)
                # show the output image with the face detections + facial landmarks
            cv2.imshow("Output", img)
            # time.sleep(WAIT)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
