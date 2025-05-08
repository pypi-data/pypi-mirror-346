from typing import Generator

import cv2


class Extractor:
    def __init__(self, video_path):
        self.video_path = video_path

        cap = cv2.VideoCapture(self.video_path)
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        seconds = round(frames / fps)
        self.duration = seconds

    def get_codec(self)->str:
        cap = cv2.VideoCapture(self.video_path)
        h = int(cap.get(cv2.CAP_PROP_FOURCC))
        codec = chr(h & 0xff) + chr((h >> 8) & 0xff) + chr((h >> 16) & 0xff) + chr((h >> 24) & 0xff)
        return codec

    def get_duration(self):
        return self.duration


    def extract_frames(self, start_at: int=0, end_at:int|None=None) -> Generator[tuple[int, float,cv2.typing.MatLike], None, None]:
        cam = cv2.VideoCapture(self.video_path)
        # cam.set(cv2.CAP_PROP_POS_MSEC, start_at*1000)

        if end_at is None:
            end_at = self.duration

        currentframe = 0
        cond = True
        while cond:
            ret, frame = cam.read()

            if ret:
                t_in_ms=cam.get(cv2.CAP_PROP_POS_MSEC)
                t_in_s=int(t_in_ms/1000)
                if t_in_s < start_at:
                    currentframe += 1
                    continue
                elif start_at <= t_in_s <= end_at:
                    yield currentframe, t_in_ms, frame
                    currentframe += 1
                elif t_in_s > end_at:
                    break
            else:
                break

        cam.release()
        cv2.destroyAllWindows()