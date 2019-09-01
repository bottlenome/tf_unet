import sys
import os
import subprocess


def make_link(file_name, link_name):
    cmd = "ln -s {} {}".format(file_name, link_name)
    print(cmd)
    os.system(cmd)


def is_size(size, target):
    cmd = "identify -format %w {}".format(target).split(" ")
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    p.wait()
    image_size, _ = p.communicate()
    if int(image_size) == size:
        return True
    else:
        print("ignore {} {}".format(target, image_size))
        return False


def main(input_data_folder, output_data_folder, output_path, limit=475):
    input_path = input_data_folder
    count = 1

    for curDir, dirs, files in os.walk(input_path):
        files = sorted(files)
        for name in files:
            file_name = input_data_folder + os.sep + name
            if not is_size(512, file_name):
                continue
            count += 1
            if count > limit:
                break
            link_name = output_path + os.sep + name
            make_link(file_name, link_name)
            file_name = output_data_folder + os.sep + name
            link_name = output_path + os.sep + name
            link_name = link_name.replace(".png", "_reconst.png")
            make_link(file_name, link_name)


if __name__ == '__main__':
    input_data_folder = sys.argv[1]
    output_data_folder = sys.argv[2]
    output_path = sys.argv[3]
    main(input_data_folder, output_data_folder, output_path)
