import os
from PIL import Image
from skimage.transform import radon, iradon
import numpy as np
import sys
import time
import psutil


def make_fbped(img, size):
    img = np.array(img)
    theta = np.linspace(0., 360., size, endpoint=False)
    sino = radon(img, theta=theta, circle=True)
    return iradon(sino, theta=theta, circle=True)


def check_cpu_temperature():
    temp = psutil.sensors_temperatures()['coretemp'][0].current
    while temp > 60:
        print("temperature high", )
        time.sleep(1)
        temp = psutil.sensors_temperatures()['coretemp'][0].current


def main(input_path, output_path, size):
    save_path = output_path + os.sep + str(size)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    for curDir, dirs, files in os.walk(input_path):
        for name in files:
            check_cpu_temperature()
            file_path = curDir + os.sep + name
            output_file = save_path + os.sep + name
            if os.path.exists(output_file):
                print("ignore", output_file)
                continue
            print(file_path, output_file)
            fbped_image = make_fbped(Image.open(file_path), size)
            Image.fromarray(fbped_image.astype('uint8')).save(output_file)


if __name__ == '__main__':
    input_path = sys.argv[1]
    size = int(sys.argv[2])
    output_path = "/mnt/collect/ct_images/fbped_images"
    main(input_path, output_path, size)
