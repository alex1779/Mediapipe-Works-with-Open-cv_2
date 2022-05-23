# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 19:15:23 2022

@author: Ale
"""

import argparse
import cv2
import mediapipe as mp
import imutils
from data.drawing import alignedFaceHorizontal, mask_face
from data.utils import getBaseName


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--img_path', type=str, default='input/test.jpg',
                    help='Please specify path for image', required=True)
opt = parser.parse_args()

path_out = 'output/' + getBaseName(opt.img_path) + '_Aligned Face Horizontal.jpg'

# # For static images:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5) as face_mesh:

    image = cv2.imread(opt.img_path)
    image = imutils.resize(image, height=1200)
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    annotated_image = image.copy()
    for face_landmarks in results.multi_face_landmarks:
        annotated_image = mask_face(annotated_image, face_landmarks)
        annotated_image = alignedFaceHorizontal(annotated_image, face_landmarks)

    cv2.imwrite(path_out, annotated_image)
    
    image = imutils.resize(image, height=500)
    annotated_image = imutils.resize(annotated_image, height=500)
    cv2.imshow('Original', image)
    cv2.imshow('Face Aligned Without Background', annotated_image)

    if cv2.waitKey(0) & 0xFF == 27:
        cv2.destroyAllWindows()
