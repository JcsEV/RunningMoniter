import io
import os
import sys

import numpy as np
import pandas as pd
import tqdm

import tensorflow as tf

import cv2
from PIL import Image

from .script.data import BodyPart
from .script.movenet import Movenet


class MoveNetPoseMark(object):
    def __init__(self, model_path="'./model/movenet_singlepose_thunder_int8'", detection=0.3):
        self.move_net = Movenet(model_name=model_path)
        self.header = ['file_name']
        list_name = [[p.name + '_x', p.name + '_y', p.name + '_score'] for p in BodyPart]
        for columns_name in list_name:
            self.header += columns_name
        self.detection = detection

    def detect(self, input_tensor, inference_count=3, per=None):
        self.move_net.detect(input_tensor.numpy(), reset_crop_region=True)
        for _ in range(inference_count - 1):
            per = self.move_net.detect(input_tensor.numpy(), reset_crop_region=False)
        return per

    def pic_mark(self, folder, header, detection=0.1, index=None, classes="temp"):
        messages, valid_image_count, df = [], 0, pd.DataFrame([], columns=header)
        image_names = sorted([n for n in os.listdir(folder) if not n.startswith('.')])
        for image_name in tqdm.tqdm(image_names):
            image_path = os.path.join(folder, image_name)
            try:
                image = tf.io.decode_jpeg(tf.io.read_file(image_path))
                _, _, channel = image.shape
            except:
                messages.append('Skipped ' + image_path + '. Invalid image.')
                continue
            if channel != 3:
                messages.append('Skipped ' + image_path + '. Image isn\'t in RGB format.')
                continue
            person = self.detect(image)
            if not (min([p.score for p in person.keypoints]) >= detection):
                messages.append('Skipped ' + image_path + '. No pose was confidentlly detected.')
                continue
            landmarks = np.array([[p.coordinate.x, p.coordinate.y, p.score] for p in person.keypoints],
                                 dtype=str).flatten()
            df = pd.concat([df, pd.DataFrame([[image_name] + list(landmarks)], columns=header)], axis=0)
            valid_image_count += 1
        if not valid_image_count:
            raise RuntimeError('No valid images found for the "{}" class.'.format(classes))
        df['class_no'], df['class_name'] = [str(index)] * len(df), [classes] * len(df)
        return messages, df

    def vid_mark(self, vid_pic, header, detection=0.1, index=None, classes="temp"):
        messages, valid_image_count, df = [], 0, pd.DataFrame([], columns=header)
        for pic in tqdm.tqdm(vid_pic):
            try:
                pillow_image, buffer = Image.fromarray(np.uint8(pic)), io.BytesIO()
                pillow_image.save(buffer, format='JPEG')
                decoded_image = tf.io.decode_jpeg(buffer.getvalue(), channels=3)
                _, _, channel = decoded_image.shape
            except:
                messages.append(f'Skipped {valid_image_count + 1}. Invalid image.')
                continue
            if channel != 3:
                messages.append(f'Skipped {valid_image_count + 1}. Image isn\'t in RGB format.')
                continue
            person = self.detect(decoded_image)
            if not (min([p.score for p in person.keypoints]) >= detection):
                messages.append(f'Skipped {valid_image_count + 1}. No pose was confidentlly detected.')
                continue
            landmarks = np.array([[p.coordinate.x, p.coordinate.y, p.score] for p in person.keypoints],
                                 dtype=str).flatten()
            df = pd.concat([df, pd.DataFrame([[valid_image_count + 1] + list(landmarks)], columns=header)], axis=0)
            valid_image_count += 1
        if not valid_image_count:
            raise RuntimeError('No valid images found for the "{}" class.'.format("predict"))
        df['class_no'], df['class_name'] = [str(0)] * len(df), ["predict"] * len(df)
        return messages, df

    def process(self, folder, csvs_path):
        messages, df = [], pd.DataFrame([], columns=self.header)
        class_names = sorted([n for n in os.listdir(folder) if not n.startswith('.')])
        for index, pose_class in enumerate(class_names):
            print('Preprocessing', pose_class, file=sys.stderr)
            _folder = os.path.join(folder, pose_class)
            message, per_df = self.pic_mark(_folder, self.header, detection=self.detection, index=index,
                                            classes=pose_class)
            messages.extend(message)
            df = pd.concat([df, per_df], axis=0)
        # print('\n'.join(messages))
        df.to_csv(csvs_path, index=False)
        return messages, df

    def img_predict(self, folder, csvs_path):
        print('Preprocessing', "pic_predict", file=sys.stderr)
        messages, df = [], pd.DataFrame([], columns=self.header)
        message, per_df = self.pic_mark(folder, self.header, detection=self.detection, index=0, classes="temp")
        messages.extend(message)
        df = pd.concat([df, per_df], axis=0)
        # print('\n'.join(messages))
        df.to_csv(csvs_path, index=False)
        return messages, df

    def vid_predict(self, vid_path, csvs_path):
        print('Preprocessing', "vid_predict", file=sys.stderr)
        cap = cv2.VideoCapture(vid_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        vid_pic = [frame for ret, frame in (cap.read() for _ in range(frame_count)) if ret]
        cap.release()
        messages, df = [], pd.DataFrame([], columns=self.header)
        message, per_df = self.vid_mark(vid_pic, self.header, detection=self.detection, index=0, classes="temp")
        messages.extend(message)
        df = pd.concat([df, per_df], axis=0)
        # print('\n'.join(messages))
        df.to_csv(csvs_path, index=False)
        return messages, df
