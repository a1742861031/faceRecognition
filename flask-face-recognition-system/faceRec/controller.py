# -*- coding: utf-8 -*-
# @Time    : 2021/4/18 14:11
# @Author  : bobo
# @Email   : 2460417845@qq.com
# @File    : api.py
import os

import cv2
import numpy as np

from . import utils
from . import net


class face_rec():
    def __init__(self):
        # -------------------------#
        #   创建mtcnn的模型
        #   用于检测人脸
        # -------------------------#
        self.mtcnn_model = net.mtcnn.mtcnn()
        self.threshold = [0.5, 0.6, 0.8]

        # -----------------------------------#
        #   载入facenet
        #   将检测到的人脸转化为128维的向量
        # -----------------------------------#
        self.facenet_model = net.inception.InceptionResNetV1()
        model_path = './model_data/facenet_keras.h5'
        self.facenet_model.load_weights(model_path)

        # -----------------------------------------------#
        #   对数据库中的人脸进行编码
        #   known_face_encodings中存储的是编码后的人脸
        #   known_face_names为人脸的名字
        # -----------------------------------------------#
        face_list = os.listdir("face_dataset")
        self.known_face_encodings = []
        self.known_face_names = []
        print(face_list)
        # 遍历人脸数据库中的每张人脸
        for face in face_list:
            name = face.split(".")[0]
            # img = cv2.imdecode("./face_dataset/" + face, dtype=np.uint8), cv2.IMREAD_COLOR)
            img = cv2.imdecode(np.fromfile("./face_dataset/" + face, dtype=np.uint8),
                               cv2.IMREAD_COLOR)  # 从内存数据读入图片

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # ---------------------#
            #   检测人脸
            # ---------------------#
            rectangles = self.mtcnn_model.detectFace(img, self.threshold)
            # ---------------------#
            #   转化成正方形
            # ---------------------#
            rectangles = utils.utils.rect2square(np.array(rectangles))
            # -----------------------------------------------#
            #   facenet要传入一个160x160的图片
            #   利用landmark对人脸对齐
            # -----------------------------------------------#
            rectangle = rectangles[0]
            landmark = np.reshape(rectangle[5:15], (5, 2)) - np.array([int(rectangle[0]), int(rectangle[1])])
            crop_img = img[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
            crop_img, _ = utils.utils.Alignment_1(crop_img, landmark)
            crop_img = np.expand_dims(cv2.resize(crop_img, (160, 160)), 0)
            # --------------------------------------------------------------------#
            #   将检测到的人脸传入到facenet的模型中，实现128维特征向量的提取
            # --------------------------------------------------------------------#
            face_encoding = utils.utils.calc_128_vec(self.facenet_model, crop_img)

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(name)

    def face_encodeing_recognize(self, img):
        # -----------------------------------------------#
        #   人脸识别
        #   先定位，再进行数据库匹配
        # -----------------------------------------------#
        height, width, _ = np.shape(img)
        draw_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # --------------------------------#
        #   检测人脸
        # --------------------------------#
        rectangles = self.mtcnn_model.detectFace(draw_rgb, self.threshold)

        if len(rectangles) == 0:
            return

        # 转化成正方形
        rectangles = utils.utils.rect2square(np.array(rectangles, dtype=np.int32))
        rectangles[:, [0, 2]] = np.clip(rectangles[:, [0, 2]], 0, width)
        rectangles[:, [1, 3]] = np.clip(rectangles[:, [1, 3]], 0, height)

        # -----------------------------------------------#
        #   对检测到的人脸进行编码
        # -----------------------------------------------#

        face_encodings = []
        for rectangle in rectangles:
            # ---------------#
            #   截取图像
            # ---------------#
            landmark = np.reshape(rectangle[5:15], (5, 2)) - np.array([int(rectangle[0]), int(rectangle[1])])
            crop_img = draw_rgb[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
            # -----------------------------------------------#
            #   利用人脸关键点进行人脸对齐
            # -----------------------------------------------#
            crop_img, _ = utils.utils.Alignment_1(crop_img, landmark)
            crop_img = np.expand_dims(cv2.resize(crop_img, (160, 160)), 0)

            face_encoding = utils.utils.calc_128_vec(self.facenet_model, crop_img)
            face_encodings.append(face_encoding)
        face_names = []
        for face_encoding in face_encodings:
            # -------------------------------------------------------#
            #   取出一张脸并与数据库中所有的人脸进行对比，计算得分
            # -------------------------------------------------------#
            matches = utils.utils.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"
            # -------------------------------------------------------#
            #   找出距离最近的人脸
            # -------------------------------------------------------#
            face_distances = utils.utils.face_distance(self.known_face_encodings, face_encoding)
            # -------------------------------------------------------#
            #   取出这个最近人脸的评分
            # -------------------------------------------------------#
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)
        result = ','.join(face_names)
        return result
