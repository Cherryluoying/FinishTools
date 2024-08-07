import cv2
import time

class VideoRecorder:
    def __init__(self, config):
        self.config = config
        self.is_recording = False
        self.cap = cv2.VideoCapture(0)
        self.video_writer = None

    def start_recording(self):
        self.is_recording = True
        self.video_writer = cv2.VideoWriter(f"data/videos/{time.strftime('%Y%m%d_%H%M%S')}.avi",
                                            cv2.VideoWriter_fourcc(*"XVID"), 20.0, (640, 480))

    def stop_recording(self):
        self.is_recording = False
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None

    def get_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return ret, frame
        return False, None

    def add_timestamp(self, frame):
        timestamp = time.strftime("%Y-%m-%d %M:%S.%f",time.localtime())
        cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return frame

    def release(self):
        self.cap.release()