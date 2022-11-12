import cv2 as cv
import mediapipe as mp
import time

cam = cv.VideoCapture(0)

face_cascade=cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_alt2.xml")
ds_factor=0.6

cur_time = None
prev_time = 0
def show_fps(frame):
    global cur_time
    global prev_time

    cur_time = time.time()
    fps = int(1/(cur_time-prev_time))
    prev_time = cur_time
    
    # print('FPS:', fps)
    return cv.putText(frame, str(fps), (70,80), cv.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)


def face_detection(input_frame):
    frame = cv.resize(input_frame,None,fx=ds_factor,fy=ds_factor, interpolation=cv.INTER_AREA)
    
    # Face dectection
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    face_rects = face_cascade.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in face_rects:
        cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        break
    return frame

while True:
    ret, frame = cam.read()

    frame = face_detection(frame)   

    frame = show_fps(frame)

    if ret:
        cv.imshow("Hello", frame)

        if cv.waitKey(33) == ord('q'):
            break

cam.release()
cv.destroyAllWindows() 