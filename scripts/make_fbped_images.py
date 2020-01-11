import numpy as np
from skimage.transform import radon, iradon
import os
import sys


def make_image(src_path, num_project, dst_path):
    image = np.load(src_path)
    theta = np.linspace(0., 360., num_project, endpoint=False)
    sinogram = radon(image, theta=theta, circle=True)
    reconstruction_fbp = iradon(sinogram, theta=theta, circle=True)
    np.save(dst_path, reconstruction_fbp)


num_images = 28463
project_num = 64
start = int(sys.argv[1])
data_folder = "/home/urota/git/fab/data_folder/fab/train_datas/"
src_file = data_folder + "{}/{}_pre.npy"
dst_file = data_folder + "{}/{}_{}_fbped.npy"

for i in range(start, num_images):
    print(i)
    if i >= 28000:
        folder_num = num_images
    else:
        folder_num = (int(i / 1000) + 1) * 1000
    for p_num in [64, 128, 256, 512]:
        src = src_file.format(folder_num, i)
        dst = dst_file.format(folder_num, i, p_num)
        if not os.path.exists(dst):
            make_image(src, p_num, dst)
