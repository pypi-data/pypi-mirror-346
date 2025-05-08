import argparse
import os

import cv2

from movie_frame_extractor_xethhung12 import Extractor


def cmd():
    parser = argparse.ArgumentParser(description="Extract movie frames")
    parser.add_argument("--path", help="Path to movie file")
    parser.add_argument("--start",type=int, help="Start at second")
    parser.add_argument("--end",type=int, help="End at second")
    args = parser.parse_args()

    path=args.path
    if path is None:
        raise Exception("argument --path is required")
    if not os.path.exists(path):
        raise Exception("File doesn't exist")

    start = args.start
    end = args.end

    ex = Extractor(path)
    duration = ex.get_duration()

    if start is None:
        start = 0

    if start > duration:
        raise Exception(f"start must be smaller than duration[{duration} second]")

    if end is None:
        end = duration

    if end > duration:
        end = duration

    out_path='.movie_frame_extractor_data'
    if not os.path.exists(out_path):
        os.makedirs(out_path)


    print(f"Extracting movie frames from {start} to {end} in `{path}` to `{out_path}`")

    for frame_number, ms, image in ex.extract_frames(start, end):
        in_s = ms / 1000
        f = os.path.join(out_path, f"frame-{frame_number:06d}-at-{int(in_s/60):02d}m-{int(in_s%60):02d}s.jpg")
        print(f"Writing {f}", end=' ')
        cv2.imwrite(f, image)
        print(f" <=== [Done]")

    print("Extraction Complete")
