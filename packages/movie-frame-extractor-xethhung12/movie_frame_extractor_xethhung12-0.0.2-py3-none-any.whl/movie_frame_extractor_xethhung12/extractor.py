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

    def get_duration(self):
        return self.duration


    def extract_frames(self, start_at: int=0, end_at:int|None=None) -> Generator[tuple[int, float,cv2.typing.MatLike], None, None]:
        cam = cv2.VideoCapture(self.video_path)
        # cam.set(cv2.CAP_PROP_POS_MSEC, start_at*1000)

        if end_at is None:
            end_at = self.duration

        currentframe = 0
        while True:
            ret, frame = cam.read()
            t_in_ms=cam.get(cv2.CAP_PROP_POS_MSEC)
            t_in_s=int(t_in_ms/1000)

            if t_in_s < start_at:
                currentframe += 1
                continue

            elif start_at <= int(t_in_ms/1000) <= end_at:
                if ret:
                    yield currentframe, t_in_ms, frame
                    currentframe += 1
                else:
                    break
            elif t_in_s > end_at:
                break

        cam.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    for i in Extractor("/home/xeth/Downloads/REC_2025_04_30_21_47_02_F.MP4").extract_frames(10,12):
        print(i)