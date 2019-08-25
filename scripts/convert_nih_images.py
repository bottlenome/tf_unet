import csv
import os
import numpy as np
import png
from PIL import Image


def intensity_windowing(img, a, b):
    assert(a < b)
    img = img.astype("float")
    img = np.minimum(255, np.maximum(0, (img - a) / (b - a) * 255))
    return img.astype("uint8")


def normalize(img):
    return img - 32768


def convert(search_path, file_hint, output_path, func):
    # 000001_01_01_109.png to 000001_01_01/109.png
    file_name = file_hint[:-8] + os.sep + file_hint[-7:]
    print(file_name)
    reader = png.Reader(search_path + os.sep + file_name)
    pngdata = reader.read()
    return func(np.array(map(np.int32, pngdata[2])))


def main(csv_path, search_path, output_path):
    with open(csv_path) as f:
        f = csv.DictReader(f)
        for row in f:
            window = row["DICOM_windows"]
            low, high = window.split(",")
            low = float(low)
            high = float(high)
            file_name = row["File_name"]
            print(file_name, low, high)
            output_filename = output_path + os.sep + file_name
            if os.path.exists(output_filename):
                print("alredy exists")
                continue

            def func(img):
                return intensity_windowing(normalize(img), low, high)

            converted = convert(search_path, file_name, output_path, func)
            pilImg = Image.fromarray(converted.astype('uint8'))
            pilImg.save(output_filename)


if __name__ == '__main__':
    main("/mnt/collect/ct_images/DL_info.csv",
         "/mnt/collect/ct_images/Images_png",
         "/mnt/collect/ct_images/windowed_png")
