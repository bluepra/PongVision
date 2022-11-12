import cv2 as cv
import mediapipe as mp
import time
import copy
import numpy as np

class Camera():

    def __init__(self) -> None:
        self.cam = cv.VideoCapture(0)
        self.mp_pose = mp.solutions.pose
        self.mp_draw = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose()
        

if __name__ == '__main__':
    pass