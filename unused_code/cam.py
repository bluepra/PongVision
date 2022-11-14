import cv2
import mediapipe as mp
import time
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils


cur_time = None
prev_time = 0
def show_fps(frame):
    global cur_time
    global prev_time

    cur_time = time.time()
    fps = int(1/(cur_time - prev_time))
    prev_time = cur_time
    
    # print('FPS:', fps)
    return cv2.putText(frame, 'FPS:' + str(fps), (70,80), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

# For webcam input:
cap = cv2.VideoCapture(0)

def get_nose_coords(image):
    h,w,c = image.shape
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    results = face_detection.process(image)

    # Draw the face detection annotations on the image
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    nose_coords = []
    if results.detections:
        for detection in results.detections:
            nose = nose = mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.NOSE_TIP)
            nose_y = int(nose.y * h)
            nose_x = int(nose.x * w)
            nose_coords.append((nose_x, nose_y))
            # mp_drawing.draw_detection(image, detection)
    
    return nose_coords

def draw_nose_lines(frame, coords, side):
    if len(coords) > 0:
        for x,y in coords:
            color = (0,0,255)
            frame = cv2.line(frame, pt1 = (x-20, y), pt2=(x+20, y), color=color, thickness=5)
    return frame

# Context Manager

while True:
    success, image = cap.read()
    if not success: continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False

    # Flip the image horizontally for a selfie-view display.
    image = show_fps(image)
    nose_coords = get_nose_coords(image)
    
    image = draw_nose_lines(image, nose_coords[:2], side = 'left')
    cv2.imshow('MediaPipe Face Detection', image)

    if cv2.waitKey(5) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()