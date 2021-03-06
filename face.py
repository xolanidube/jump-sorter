# coding=utf-8
"""Face Detection and Recognition"""
# MIT License
#
# Copyright (c) 2017 François Gervais
#
# This is the work of David Sandberg and shanren7 remodelled into a
# high level container. It's an attempt to simplify the use of such
# technology and provide an easy to use facial recognition package.
#
# https://github.com/davidsandberg/facenet
# https://github.com/shanren7/real_time_face_recognition
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pickle
import os

import cv2
import numpy as np
import tensorflow as tf
from scipy import misc
import random
import  detect_face
import  facenet
from sklearn.svm.libsvm import predict


gpu_memory_fraction = 0.3
facenet_model_checkpoint = os.path.dirname(__file__) + f"\\20180402-114759.pb"
classifier_model = os.path.dirname(__file__) + f"\\faces.pkl" 
debug = False


class Face:
    def __init__(self):
        self.name = None
        self.bounding_box = None
        self.image = None
        self.container_image = None
        self.embedding = None
        self.threshold = 0;


class Recognition:
    def __init__(self):
        self.detect = Detection()
        self.encoder = Encoder()
        self.identifier = Identifier()

    def add_identity(self, image, person_name):
        faces = self.detect.find_faces(image)

        if len(faces) == 1:
            face = faces[0]
            face.name = person_name
            face.embedding = self.encoder.generate_embedding(face)
            return faces

    def identify(self, image):
        
        
        faces, points = self.detect.find_faces(image)
    
        if len(faces) > 0:
            for i, face in enumerate(faces):
                if debug:
                    cv2.imshow("Face: " + str(i), face.image)
                face.embedding = self.encoder.generate_embedding(face)
                face.name = self.identifier.identify(face)
                face.threshold = self.identifier.Threshold(face)
            return faces, points
        
        if len(faces) < 0:
            return None
        
    def detection(self, face):
        faces, points = self.detect.find_faces(face)
        
        if len(faces) > 0:
            for i, face in enumerate(faces):
                if debug:
                    cv2.imshow("Face: " + str(i), face.image)

            return faces, points
        
        if len(faces) < 0:
            return None
class Identifier:
    def __init__(self):
        with open(classifier_model, 'rb') as infile:
            self.model, self.class_names = pickle.load(infile)

    def identify(self, face):
        if face.embedding is not None:
            predictions = self.model.predict_proba([face.embedding])
            best_class_indices = np.argmax(predictions, axis=1)
            best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]
            
            if best_class_probabilities >= .95:
                
                return self.class_names[best_class_indices[0]]
            else:
                return "Unrecognized"
            
    def Threshold(self, face):
        if face.embedding is not None:
            predictions = self.model.predict_proba([face.embedding])
            best_class_indices = np.argmax(predictions, axis=1)
            best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]
            self.threshold = best_class_probabilities
       
            if best_class_probabilities >= .95:
                
                return  best_class_probabilities
            else:
                return 0
           
            
        


class Encoder:
    def __init__(self):
        self.sess = tf.compat.v1.Session()
        with self.sess.as_default():
            facenet.load_model(facenet_model_checkpoint)

    def generate_embedding(self, face):
        # Get input and output tensors
        images_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("input:0")
        embeddings = tf.compat.v1.get_default_graph().get_tensor_by_name("embeddings:0")
        phase_train_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("phase_train:0")

        prewhiten_face = facenet.prewhiten(face.image)

        # Run forward pass to calculate embeddings
        feed_dict = {images_placeholder: [prewhiten_face], phase_train_placeholder: False}
        return self.sess.run(embeddings, feed_dict=feed_dict)[0]


class Detection:
    # face detection parameters
    minsize = 20  # minimum size of face
    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    factor = 0.709  # scale factor

    def __init__(self, face_crop_size=160, face_crop_margin=32):
        self.pnet, self.rnet, self.onet = self._setup_mtcnn()
        self.face_crop_size = face_crop_size
        self.face_crop_margin = face_crop_margin

    def _setup_mtcnn(self):
        with tf.Graph().as_default():
            gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
            sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
            with sess.as_default():
                return detect_face.create_mtcnn(sess, None)

    def find_faces(self, image):
        faces = []

        bounding_boxes, _ = detect_face.detect_face(image, self.minsize,
                                                          self.pnet, self.rnet, self.onet,
                                                          self.threshold, self.factor)
        for bb in bounding_boxes:
            face = Face()
            face.container_image = image
            face.bounding_box = np.zeros(4, dtype=np.int32)

            img_size = np.asarray(image.shape)[0:2]
            face.bounding_box[0] = np.maximum(bb[0] - self.face_crop_margin / 2, 0)
            face.bounding_box[1] = np.maximum(bb[1] - self.face_crop_margin / 2, 0)
            face.bounding_box[2] = np.minimum(bb[2] + self.face_crop_margin / 2, img_size[1])
            face.bounding_box[3] = np.minimum(bb[3] + self.face_crop_margin / 2, img_size[0])
            cropped = image[face.bounding_box[1]:face.bounding_box[3], face.bounding_box[0]:face.bounding_box[2], :]
            face.image = misc.imresize(cropped, (self.face_crop_size, self.face_crop_size), interp='bilinear')

            faces.append(face)
            
        
        return faces, _
        
     
    
class Verification:
    
    def __init__(self):
        
            
        self.threshold = 0.7
        self.encoder = Encoder()
        self.detect = Detection()

        
    def distance(self, emb1, emb2):
        diff = np.subtract(emb1, emb2)
        return np.sum(np.square(diff))
            
            
    def getEmbbeding(self, image):
        faces, points = self.detect.find_faces(image)
        
        if len(faces) > 0:
            for i, face in enumerate(faces):
                
                face.embedding = self.encoder.generate_embedding(face)
                
                return face.embedding
        else:
            
            return None
        
    def getRandomImage(self, path):
        """function loads a random images from a random folder in our test path """
        random_filename = random.choice([x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))])
        
        return random_filename        
        
        
    def verify(self, recognized, comparisen):
        
        face1 = cv2.imread(recognized, cv2.IMREAD_COLOR)
        face2 = cv2.imread(comparisen, cv2.IMREAD_COLOR)
        
        
                
        
        
        
        emb1 = self.getEmbbeding(face1)
        emb2 = self.getEmbbeding(face2)
        
        if emb1 is None:
            name = recognized.split('.')[0]
            path = "C://Users//SELINA//Project Clock-in//Clock_In//employee_data//train_aligned//" + name + "//"
            rd = path + self.getRandomImage(path)
            
            face1 = cv2.imread(rd, cv2.IMREAD_COLOR)
            emb1 = self.getEmbbeding(face1)
            
            if emb1 is None:
                name = recognized.split('.')[0]
                path = "C://Users//SELINA//Project Clock-in//Clock_In//employee_data//train_aligned//" + name + "//"
                rd = path + self.getRandomImage(path)
                
                face1 = cv2.imread(rd, cv2.IMREAD_COLOR)
                emb1 = self.getEmbbeding(face1)
                
        if emb2 is None:
            
            name = recognized.split('.')[0]
            path = "C://Users//SELINA//Project Clock-in//Clock_In//employee_data//train_aligned//" + name + "//"
            rd = path + self.getRandomImage(path)
            
            face2 = cv2.imread(rd, cv2.IMREAD_COLOR)
            
            emb2 = self.getEmbbeding(face2)
            if emb2 is None:
                name = recognized.split('.')[0]
                path = "C://Users//SELINA//Project Clock-in//Clock_In//employee_data//train_aligned//" + name + "//"
                rd = path + self.getRandomImage(path)
                
                face2 = cv2.imread(rd, cv2.IMREAD_COLOR)
                emb2 = self.getEmbbeding(face1)
            
        
        
        distance = self.distance(emb1, emb2)
        
        print("Verification distance : ", distance)
        
        distance = (2 - distance) * 50
        
        print("Normalized Verification distance : ", distance)
        
        return distance
        
            

        
        
            
