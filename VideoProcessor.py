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
        self.mp_pose = mp.solutions.pose
        self.mp_draw = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose()

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

    def split_frame_into_2(self, frame):
        height, width, channels = frame.shape

        # Right Half - left side is blacked out
        r = copy.deepcopy(frame)
        r[:, 0:width//2] = np.zeros(shape=(height, width//2, channels))

        # Left Half - right side is blacked out
        frame[:, width//2:] = np.zeros(shape=(height, width//2, channels))
        
        return frame, r

    def break_frame_into_2(self, frame):
        h,w,c = frame.shape
        left = frame[:,0:w//2]
        right = frame[:,w//2:]
        return left, right
    
    def stitch_left_and_right(self, left, right):
        h,w,c = left.shape
        left[:, w//2:] = right[:, w//2:]
        cv.line(left, pt1=(w//2,0), pt2=(w//2,h), color=(255,255,255), thickness=100)
        return left
    
    def draw_nose_line(self, frame, coord, side):
        if coord:
            x,y = coord
            if side == 'left':
                color = (255,0,0)
            else:
                color = (0,0,255)
            frame = cv.line(frame, pt1 = (x-20, y), pt2=(x+20, y), color=color, thickness=4)
        return frame
    
    def get_nose_coord(self, frame):
        frame_width = frame.shape[1]
        frame_height = frame.shape[0]
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        # Get the Pose Landmarks
        results = self.pose.process(frame)
        if results.pose_landmarks:
            self.mp_draw.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

            # Nose Y is the Y coordinate of your nose in the frame
            nose_y = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.NOSE].y * frame_height)
            nose_x = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.NOSE].x * frame_width)
        else:
            return None

        return (nose_x, nose_y)
    
    def get_Y_coords(self, show_video = False):
        ret, frame = vp.cam.read()
        if not ret: return None
        
        h,w,c = frame.shape
        frame = cv.flip(frame, 1)

        frame = vp.show_fps(frame)

        # Break frame into 2 halves
        left, right = vp.break_frame_into_2(frame)

        # Get poses for both halves
        left_nose_coord = vp.get_nose_coord(left)
        right_nose_coord = vp.get_nose_coord(right)

        left = vp.draw_nose_line(left, left_nose_coord, 'left')
        right = vp.draw_nose_line(right, right_nose_coord, 'right')

        frame = np.concatenate((left,right),axis=1)

        self.cur_frame = frame

        # EXTRA: Modify right coord to so that its in the right place in the bigger frame
        right_nose_coord[0] += w//2

        if show_video:
            cv.imshow("Video Feed", frame)

        return (left_nose_coord[1], right_nose_coord[1])

        



if __name__ == '__main__':
    vp = VideoProcessor()

    while True:
        ret, frame = vp.cam.read()
        
        if not ret: continue

        h,w,c = frame.shape
        frame = cv.flip(frame, 1)

        frame = vp.show_fps(frame)

        # Split frame into 2 halves
        # left, right = vp.split_frame_into_2(frame)
        
        left, right = vp.break_frame_into_2(frame)

        # # # Get poses for both halves
        left_nose_coord = vp.get_nose_coord(left)
        right_nose_coord = vp.get_nose_coord(right)

        # # if left_nose_coord:
        # #     print('Left Nose', left_nose_coord[1], ' ------ ', end='')
        # # if right_nose_coord:
        # #     print('Right Nose', right_nose_coord[1], end='')
        # # print()

        left = vp.draw_nose_line(left, left_nose_coord, 'left')
        right = vp.draw_nose_line(right, right_nose_coord, 'right')

        frame = np.concatenate((left,right),axis=1)

        cv.imshow("Video Feed", frame)

        if cv.waitKey(33) == ord('q'):
            break

    vp.close()