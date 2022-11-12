import cv2 as cv
import mediapipe as mp
import time
import copy
import numpy as np


cam = cv.VideoCapture(0)
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

cur_time = None
prev_time = 0
def show_fps(frame):
    global cur_time
    global prev_time

    cur_time = time.time()
    fps = int(1/(cur_time - prev_time))
    prev_time = cur_time
    
    # print('FPS:', fps)
    return cv.putText(frame, 'FPS:' + str(fps), (70,80), cv.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

def face_detection(input_frame):
    face_cascade=cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_alt2.xml")
    ds_factor=0.6
    frame = cv.resize(input_frame,None,fx=ds_factor,fy=ds_factor, interpolation=cv.INTER_AREA)
    
    # Face dectection
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    face_rects = face_cascade.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in face_rects:
        cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        break
    return frame

def split_frame_into_2(frame):
    height, width, channels = frame.shape

    # Right Half - left side is blacked out
    r = copy.deepcopy(frame)
    r[:, 0:width//2] = np.zeros(shape=(height, width//2, channels))

    # Left Half - right side is blacked out
    frame[:, width//2:] = np.zeros(shape=(height, width//2, channels))
    
    return frame, r

def get_nose_coord(frame):
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # Get the Pose Landmarks
    results = pose.process(frame)
    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Nose Y is the Y coordinate of your nose in the frame
        nose_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * frame_height)
        nose_x = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * frame_width)
    else:
        return None

    return (nose_x, nose_y)

def draw_nose_line(frame, coord, side):
    if coord:
        x,y = coord
        if side == 'left':
            color = (255,0,0)
        else:
            color = (0,0,255)
        frame = cv.line(frame, pt1 = (x-20, y), pt2=(x+20, y), color=color, thickness=4)
    return frame

def stitch_left_and_right(left, right):
    h,w,c = left.shape
    left[:, w//2:] = right[:, w//2:]
    cv.line(left, pt1=(w//2,0), pt2=(w//2,h), color=(255,255,255), thickness=100)
    return left

while True:
    ret, frame = cam.read()
    if not ret: continue

    h,w,c = frame.shape
    frame = cv.flip(frame, 1)

    # frame = show_fps(frame)

    # Split frame into 2 halves
    left, right = split_frame_into_2(frame)

    # # Get poses for both halves
    left_nose_coord = get_nose_coord(left)
    right_nose_coord = get_nose_coord(right)

    # if left_nose_coord:
    #     print('Left Nose', left_nose_coord[1], ' ------ ', end='')
    # if right_nose_coord:
    #     print('Right Nose', right_nose_coord[1], end='')
    # print()


    left = draw_nose_line(left, left_nose_coord, 'left')
    right = draw_nose_line(right, right_nose_coord, 'right')

    frame = stitch_left_and_right(left, right)

    cv.imshow("Video Feed", frame)

    if cv.waitKey(33) == ord('q'):
        break

cam.release()
cv.destroyAllWindows() 