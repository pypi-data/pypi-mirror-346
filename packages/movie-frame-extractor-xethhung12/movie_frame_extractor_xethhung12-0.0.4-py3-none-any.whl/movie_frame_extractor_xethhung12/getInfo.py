import argparse
import os
from pyFileSizeUtils import BinarySize, SizeUnit

from movie_frame_extractor_xethhung12 import Extractor


def cmd():
    parser = argparse.ArgumentParser(description="Extract movie info")
    parser.add_argument("--path", help="Path to movie file")
    args = parser.parse_args()

    path=args.path
    if path is None:
        raise Exception("argument --path is required")
    if not os.path.exists(path):
        raise Exception("File doesn't exist")

    ex = Extractor(path)
    duration = ex.get_duration()

    sizeUnit=BinarySize(SizeUnit.Byte,os.path.getsize(path))

    print("File: ", path)
    print("File size: ", f"{sizeUnit.inMB()}m")
    print("Codec: ", ex.get_codec())
    print("Duration: ", f"{duration//60:02d}m{int(duration%60)}s")
