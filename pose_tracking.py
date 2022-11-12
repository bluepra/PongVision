import cv2 as cv
import mediapipe as mp
import time
import copy


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
    fps = int(1/(cur_time-prev_time))
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
    height, width = frame.shape
    l = copy.deepcopy(frame)
    r = frame
    return


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

    return cv.cvtColor(frame, cv.COLOR_RGB2BGR)


while True:
    ret, frame = cam.read()
    
    # frame = face_detection(frame)   

    frame = show_fps(frame)
    frame = pose_estimation(frame)

    cv.imshow("Video Feed", frame)

    if cv.waitKey(33) == ord('q'):
        break

cam.release()
cv.destroyAllWindows() 