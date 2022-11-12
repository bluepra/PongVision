# Import the pygame library and initialise the game engine
import pygame
from paddle import Paddle
from ball import Ball
import cv2 as cv
import time
import mediapipe as mp


# function to start camera for face detection
def cam_set_up(width, height):
    # start webcam
    cam = cv.VideoCapture(0)
    cam.set(3, width)  # Width
    cam.set(4, height)  # Height

    return cam



def face_detection(input_frame):
    frame = cv.resize(input_frame,None,fx=ds_factor,fy=ds_factor, interpolation=cv.INTER_AREA)
    
    # Face dectection
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    face_rects = face_cascade.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in face_rects:
        cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        break
    return frame


mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()
def pose_estimation(frame):
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = pose.process(frame)
    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        frame_width = frame.shape[1]
        frame_height = frame.shape[0]
        print('Frame Height', frame_height)
        print('Frame Width', frame_width)
        nose_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * frame_height)
        frame = cv.putText(frame, 'Nose: ' + str(nose_y), (70,130), cv.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)
        # for i, pt in enumerate(results.pose_landmarks.landmark):
        #     print(i, pt)
        frame = cv.line(frame,pt1 = (0, nose_y), pt2=(frame_width, nose_y), color=(255,0,0), thickness=4)

    return cv.cvtColor(frame, cv.COLOR_RGB2BGR), nose_y


