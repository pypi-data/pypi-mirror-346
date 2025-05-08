from typing import Generator

import cv2
import os

class Extractor:
    def __init__(self, video_path):
        self.video_path = video_path

    def extract_frames(self) -> Generator[tuple[int, float,cv2.typing.MatLike], None, None]:
        cam = cv2.VideoCapture(self.video_path)
        cam.set(cv2.CAP_PROP_POS_MSEC, 40000)

        if not os.path.exists('data'):
            os.makedirs('data')

        currentframe = 0
        while True:
            print('read file')
            ret, frame = cam.read()
            t_in_ms=cam.get(cv2.CAP_PROP_POS_MSEC)
            if ret:
                yield currentframe, t_in_ms, frame
            else:
                break
            currentframe += 1

        cam.release()
        cv2.destroyAllWindows()
