from os import *
from PIL import Image
import glob
import pathlib
from pathlib import Path

if __name__ == '__main__':

    jpg_path_name = r''
    # print(type(path.join(jpg_path_name.replace('[', '[[]').replace(']', '[]]') + 'webp/', '*.webp')))
    p = pathlib.Path(Path(jpg_path_name).joinpath("webp"))
    for idx, f in enumerate(p.glob("*.webp"), start=1):
        # print(f"正在转码第 {idx} 张图片")
        img = Image.open(f)
        file_name = str(f)[0:-5].split("\\").pop()
        # img.load(), img.save(f[0:-5] + ".jpg")
        img.load(), img.save(Path(jpg_path_name).joinpath(file_name + ".jpg"))

    # for idx, f in enumerate(glob.glob(path.join(jpg_path_name + 'webp/', '*.webp')), start=1):
    #     img = Image.open(f)
    #     print(f[0:-5])
    #     file_name = f[0:-5].split("\\").pop()
    #     # img.load(), img.save(f[0:-5] + ".jpg")
    #     img.load(), img.save(jpg_path_name + file_name + ".jpg")
    #     # remove(f)
