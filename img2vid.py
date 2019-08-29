import argparse
from pathlib import Path
from tqdm import tqdm
import cv2


class Img2Vid:

    def __init__(self, path, outdir, fps, ext):
        self.path = path
        self.outdir = outdir
        self.ext = ext
        self.make_outdir()
        self.read_imgs()
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.video = cv2.VideoWriter(f"{self.outdir}/{self.path.stem}.mp4", fourcc, fps, (self.w, self.h))

    def make_outdir(self):
        if not self.outdir:
            self.outdir = Path("merged")
        if not self.outdir.exists():
            self.outdir.mkdir(exist_ok=True, parents=True)

    def read_imgs(self):
        self.paths = sorted(list(self.path.glob(f"*.{self.ext}")))
        self.h, self.w, _ = cv2.imread(str(self.paths[0])).shape

    def save_images(self):
        for path in tqdm(self.paths):
            img = cv2.imread(str(path))
            self.video.write(img)
        self.video.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path,
                        help="Path to the input video.")
    parser.add_argument("-o", "--outdir", type=Path,
                        help="Directory to save the frames.")
    parser.add_argument("-f", "--fps", type=float, default=29.5,
                        help="Interval between the frames to save.")
    parser.add_argument("-e", "--extention", type=str, default="png",
                        help="Extension to glob images as.")
    args = parser.parse_args()

    vi = Img2Vid(args.path, args.outdir, args.fps, args.extention)
    vi.save_images()
