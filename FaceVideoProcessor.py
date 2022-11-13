import cv2 as cv
import mediapipe as mp
import time
import copy
import numpy as np

class VideoProcessor():

    def __init__(self) -> None:
        # Camera and frame
        self.cam = cv.VideoCapture(0)
        self.cur_frame = None

        # Pose detection
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils

        # FPS Information
        self.cur_time = None
        self.prev_time = 0   
    
    def show_fps(self, frame):
        self.cur_time = time.time()
        fps = int(1/(self.cur_time - self.prev_time))
        self.prev_time = self.cur_time
        return cv.putText(frame, 'FPS:' + str(fps), (70,80), cv.FONT_HERSHEY_PLAIN, 3, (255,0,0), thickness=10)

    def close(self):
        self.cam.release()
        cv.destroyAllWindows()

    # def break_frame_into_2(self, frame):
    #     h,w,c = frame.shape
    #     left = frame[:,0:w//2]
    #     right = frame[:,w//2:]
    #     return left, right
    
    def draw_nose_lines(self, frame, coords):
        if len(coords) > 0:
            for x,y in coords:
                color = (0,0,255)
                frame = cv.line(frame, pt1 = (x-20, y), pt2=(x+20, y), color=color, thickness=5)
        return frame
    
    def get_nose_coords(self, image):
        h,w,c = image.shape
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        
        results = self.face_detection.process(image)

        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        nose_coords = []
        if results.detections:
            for detection in results.detections:
                nose = self.mp_face_detection.get_key_point(detection, self.mp_face_detection.FaceKeyPoint.NOSE_TIP)
                nose_y = int(nose.y * h)
                nose_x = int(nose.x * w)
                nose_coords.append((nose_x, nose_y))
        
        return nose_coords
    
    def get_Y_coords(self, show_video = False):
        ret, frame = self.cam.read()
        if not ret: return None
        
        h,w,c = frame.shape
        frame = cv.flip(frame, 1)

        frame = vp.show_fps(frame)

        y_vals = None
        nose_coords = self.get_nose_coords(frame)
        if len(nose_coords) >= 2:
            nose_coords = nose_coords[:2]

            if nose_coords[0][0] < nose_coords[1][0]:
                left_nose = nose_coords[0]
                right_nose = nose_coords[1]
            else:
                left_nose = nose_coords[1]
                right_nose = nose_coords[0]
    
            frame = self.draw_nose_lines(frame, nose_coords)
            
            y_vals = (left_nose[1], right_nose[1])
        
        self.cur_frame = frame
        
        if show_video:
            cv.imshow('Face Detection', frame)

        return y_vals if y_vals else (0,0) 



if __name__ == '__main__':
    vp = VideoProcessor()
    
    while True:
        left, right = vp.get_Y_coords(show_video=True)       
        if cv.waitKey(5) == ord('q'):
            break
    vp.close()