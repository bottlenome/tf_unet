import os
import sys

num_images = 28463
project_num = int(sys.argv[1])
start = int(sys.argv[2])
data_folder = "/home/urota/git/fab/data_folder/fab/train_datas/{}/"
dst_folder = "/home/urota/git/tf_unet/data_folder/fab_link/{}/"
pre_file = "{}_pre.npy"
fbped_file = "{}_{}_fbped.npy"

for i in range(start, num_images):
    print(i)
    if i >= 28000:
        folder_num = num_images
    else:
        folder_num = (int(i / 1000) + 1) * 1000
    src = (data_folder + pre_file).format(folder_num, i)
    dst = (dst_folder + pre_file).format(project_num, i)
    if not os.path.exists(dst):
        os.symlink(src, dst)
    src = (data_folder + fbped_file).format(folder_num, i, project_num)
    dst = (dst_folder + fbped_file).format(project_num, i, project_num)
    if not os.path.exists(dst):
        os.symlink(src, dst)
