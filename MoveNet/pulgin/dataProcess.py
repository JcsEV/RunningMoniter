import os
import random
import shutil
from PIL import Image


def train_test_split():
    # 设置需要划分的文件夹路径和训练集、验证集、测试集的比例
    data_dir = '../data/running_pic'
    out_dir = '../data/run_data'
    train_ratio = 0.7
    test_ratio = 0.2

    # 创建新的文件夹
    train_dir = os.path.join(out_dir, 'train')
    test_dir = os.path.join(out_dir, 'test')
    val_dir = os.path.join(out_dir, 'val')
    for dir in [out_dir, train_dir, test_dir, val_dir]:
        os.makedirs(dir, exist_ok=True)

    # 获取路径下的所有文件夹名称列表
    class_dirs = [name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name))]

    # 遍历每个文件夹中的图片并按比例分配到不同的数据集中
    for class_dir in class_dirs:
        images = [img for img in os.listdir(os.path.join(data_dir, class_dir)) if
                  os.path.isfile(os.path.join(data_dir, class_dir, img))]
        # 打乱图片路径列表
        random.shuffle(images)
        # 计算训练集、验证集、测试集的分割点
        train_split = int(len(images) * train_ratio)
        test_split = int(len(images) * (train_ratio + test_ratio))
        # 分配到不同的数据集中
        for i, image in enumerate(images):
            if i < train_split:
                output_dir = os.path.join(train_dir, class_dir)
            elif i < test_split:
                output_dir = os.path.join(test_dir, class_dir)
            else:
                output_dir = os.path.join(val_dir, class_dir)

            os.makedirs(output_dir, exist_ok=True)
            shutil.copy(os.path.join(data_dir, class_dir, image), os.path.join(output_dir, image))


def val_copy():
    # 设置需要划分的文件夹路径和训练集、验证集、测试集的比例
    data_dir = '../data/run_data/val'
    out_dir = '../data/run_predict/running_pic'
    out_path = "../data/labels.txt"
    os.makedirs(out_dir, exist_ok=True)

    # 获取路径下的所有文件夹名称列表
    dirs = [name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name))]

    # 遍历每个文件夹中的图片并按比例分配到不同的数据集中
    for dir in dirs:
        class_dir = os.path.join(data_dir, dir)
        # 获取该文件夹下所有图片的完整路径
        images = [os.path.join(class_dir, img) for img in os.listdir(class_dir)
                  if os.path.isfile(os.path.join(class_dir, img))]
        # 打乱图片路径列表
        random.shuffle(images)
        # 分配到不同的数据集中
        for i, img in enumerate(images):
            shutil.copy(img, os.path.join(out_dir, dir + '_' + str(i) + '.jpg'))

    with open(out_path, "w") as f:
        for dir in dirs:
            f.write(dir + "\n")


def video_copy():
    # 设置需要划分的文件夹路径和训练集、验证集、测试集的比例
    data_dir = '../data/running_vid'
    out_dir = '../data/run_predict/running_vid'
    os.makedirs(out_dir, exist_ok=True)

    # 获取路径下的所有文件夹名称列表
    dirs = [name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name))]

    # 遍历每个文件夹中的图片并按比例分配到不同的数据集中
    for dir in dirs:
        class_dir = os.path.join(data_dir, dir)
        # 获取该文件夹下所有图片的完整路径
        images = [os.path.join(class_dir, vid) for vid in os.listdir(class_dir)
                  if os.path.isfile(os.path.join(class_dir, vid))]
        # 打乱图片路径列表
        random.shuffle(images)
        # 分配到不同的数据集中
        for i, img in enumerate(images):
            shutil.copy(img, os.path.join(out_dir, dir + '_' + str(i) + '.mp4'))


def preSelect():
    source_folder = '../data/running_pic/'
    destination_folder = '../data/running_pic/'
    # 遍历源文件夹
    for root, folders, files in os.walk(source_folder):
        # 获取源文件夹路径
        source_folder_path = os.path.abspath(root)

        # 获取源文件夹下的子文件夹列表
        sub_folders = [folder for folder in folders]

        for sub_folder in sub_folders:
            # 当前子文件夹路径
            sub_folder_path = os.path.join(source_folder_path, sub_folder)

            # 获取当前子文件夹下的图片文件列表
            image_files = [file for file in os.listdir(sub_folder_path) if
                           file.endswith('.jpg') or file.endswith('.png')]

            for image_file in image_files:
                # 当前图片文件路径
                image_file_path = os.path.join(sub_folder_path, image_file)

                # 执行水平转换操作
                flipped_image = Image.open(image_file_path).transpose(Image.FLIP_LEFT_RIGHT)

                # 获取目标文件夹路径
                destination_sub_folder_path = os.path.join(destination_folder, sub_folder)

                # 创建目标文件夹
                os.makedirs(destination_sub_folder_path, exist_ok=True)

                # 目标文件路径
                destination_file_path = os.path.join(destination_sub_folder_path, "_" + image_file)

                # 保存转换后的图片到目标文件路径
                flipped_image.save(destination_file_path)

train_test_split()
val_copy()
# video_copy()
# preSelect()