import cv2
import math
import imutils
import numpy as np
import data.colors as color

def alignedFaceHorizontal(image, landmark_list):
    height, width, _ = image.shape
    PointA = landmark_list.landmark[10].x * \
        width, landmark_list.landmark[10].y * height
    PointB = landmark_list.landmark[152].x * \
        width, landmark_list.landmark[152].y * height
    angle = get_angle(PointA, PointB)
    image = imutils.rotate(image, angle)
    print('angle rotation:', angle)
    add_text_img(image, str(angle)+' grades')
    return image


def mask_face(image, landmark_list):
    height, width, _ = image.shape
    points = []
    for idx, landmark in enumerate(landmark_list.landmark):
        point = int(landmark.x * width), int(landmark.y * height)
        points.append(point)
    points = np.array(points, np.int32)
    convexhull = cv2.convexHull(points)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_gray_mask = np.zeros_like(image_gray)
    image_gray_mask = cv2.fillConvexPoly(image_gray_mask, convexhull, 255)
    result = cv2.bitwise_and(image, image, mask=image_gray_mask)

    return result


def get_distance(PointA, PointB):
    """


    Parameters
    ----------
    PointA : tuple
        x and y of startpoint.
    PointB : tuple
        x and y of endpoint.

    Returns
    -------
    distance : int


    """
    distance = int(
        math.sqrt((PointB[0] - PointA[0])**2 + (PointB[1] - PointA[1])**2))
    return distance


def get_angle(PointA, PointB):
    """


    Parameters
    ----------
    PointA : tuple
        x and y of startpoint.
    PointB : tuple
        x and y of endpoint.

    Returns
    -------
    degrees : int


    """
    myradians = math.atan2(PointA[1]-PointB[1], PointA[0]-PointB[0])
    degrees = round(math.degrees(myradians) + 90, 4)
    return degrees


def drawLandmarkPoints(image, face_landmarks, radious=1, color=(0, 255, 0)):
    height, width, _ = image.shape
    for idx, landmark in enumerate(face_landmarks.landmark):
        Point = int(landmark.x * width), int(landmark.y * height)
        cv2.circle(image, Point, radious, color)


def drawTesselation(image, face_landmarks, connections, color=(0, 255, 0), thickness=1):
    height, width, _ = image.shape
    for idx, connect in enumerate(connections):
        PointA = int(face_landmarks.landmark[connect[0]].x * width), int(
            face_landmarks.landmark[connect[0]].y * height)
        PointB = int(face_landmarks.landmark[connect[1]].x * width), int(
            face_landmarks.landmark[connect[1]].y * height)
        cv2.line(image, PointA, PointB, color, thickness)


def drawContourFace(image, face_landmarks, connections, color=(0, 255, 0), thickness=1):
    height, width, _ = image.shape
    for idx, connect in enumerate(connections):
        PointA = int(face_landmarks.landmark[connect[0]].x * width), int(
            face_landmarks.landmark[connect[0]].y * height)
        PointB = int(face_landmarks.landmark[connect[1]].x * width), int(
            face_landmarks.landmark[connect[1]].y * height)
        cv2.line(image, PointA, PointB, color, thickness)


def draw_fill_contour(image, face_landmarks, connections):
    height, width, _ = image.shape
    landmark_points_face = []
    for idx, connect in enumerate(connections):
        PointA = int(face_landmarks.landmark[connect].x * width), int(
            face_landmarks.landmark[connect].y * height)
        landmark_points_face.append(PointA)
    points = np.array(landmark_points_face, np.int32)
    convexhull = cv2.convexHull(points)
    img2_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img2_face_mask = np.zeros_like(img2_gray)
    red = np.full_like(image, (0, 0, 255))
    blend = 0.5
    img_red = cv2.addWeighted(image, blend, red, 1-blend, 0)
    img2_head_mask = cv2.fillConvexPoly(img2_face_mask, convexhull, 255)
    img2_head_noface = cv2.bitwise_and(img_red, img_red, mask=img2_head_mask)
    img2_face_mask = cv2.bitwise_not(img2_head_mask)
    img2_head_noface2 = cv2.bitwise_and(image, image, mask=img2_face_mask)
    image = cv2.add(img2_head_noface, img2_head_noface2)
    return image


def detect_side_face(image, face_landmarks, connections, color=(0, 255, 0), thickness=1):
    height, width, _ = image.shape
    PointA = int(face_landmarks.landmark[123].x *
                 width), int(face_landmarks.landmark[123].y * height)
    PointB = int(
        face_landmarks.landmark[4].x * width), int(face_landmarks.landmark[4].y * height)
    PointC = int(face_landmarks.landmark[352].x *
                 width), int(face_landmarks.landmark[352].y * height)
    dist_left = get_distance(PointA, PointB)
    dist_right = get_distance(PointC, PointB)

    with np.load('connections_face_side.npz') as data:
        centred_set = data['arr_0']
        left_set = data['arr_1']
        right_set = data['arr_2']
        left_points = data['arr_3']
        right_points = data['arr_4']

    if dist_left > dist_right:

        for idx, connect in enumerate(left_set):
            PointA = int(face_landmarks.landmark[connect[0]].x * width), int(
                face_landmarks.landmark[connect[0]].y * height)
            PointB = int(face_landmarks.landmark[connect[1]].x * width), int(
                face_landmarks.landmark[connect[1]].y * height)
            cv2.line(image, PointA, PointB, color, thickness)

        add_text_img(image, 'Left', (0, 255, 0))

        image = draw_fill_contour(image, face_landmarks, left_points)

    elif dist_left < dist_right:

        for idx, connect in enumerate(right_set):
            PointA = int(face_landmarks.landmark[connect[0]].x * width), int(
                face_landmarks.landmark[connect[0]].y * height)
            PointB = int(face_landmarks.landmark[connect[1]].x * width), int(
                face_landmarks.landmark[connect[1]].y * height)
            cv2.line(image, PointA, PointB, color, thickness)

        add_text_img(image, 'Right', (0, 255, 0))
        image = draw_fill_contour(image, face_landmarks, right_points)

    else:

        for idx, connect in enumerate(centred_set):
            PointA = int(face_landmarks.landmark[connect[0]].x * width), int(
                face_landmarks.landmark[connect[0]].y * height)
            PointB = int(face_landmarks.landmark[connect[1]].x * width), int(
                face_landmarks.landmark[connect[1]].y * height)
            cv2.line(image, PointA, PointB, color, thickness)

        add_text_img(image, 'Centred', (255, 0, 0))

    return image


def add_text_img(img, text, color=(0, 255, 0), position=(50, 50)):

    if type(text) != str:
        text = str(text)

    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = position
    fontScale = 1
    fontColor = color
    lineType = 2
    cv2.putText(img, text, bottomLeftCornerOfText,
                font, fontScale, fontColor, lineType)
    return img


def detect_side_face_minimal(image, face_landmarks):
    height, width, _ = image.shape
    PointA = int(face_landmarks.landmark[123].x *
                 width), int(face_landmarks.landmark[123].y * height)
    PointB = int(
        face_landmarks.landmark[4].x * width), int(face_landmarks.landmark[4].y * height)
    PointC = int(face_landmarks.landmark[352].x *
                 width), int(face_landmarks.landmark[352].y * height)
    dist_left = get_distance(PointA, PointB)
    dist_right = get_distance(PointC, PointB)

    if dist_left > dist_right:
        return 'left'
    else:
        return 'right'
