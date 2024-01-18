import cv2
import os
from retinaface import RetinaFace
import math

def faceapp(images, filename, output):
    images = cv2.imread(images)
    faces = RetinaFace.detect_faces(images)
    faces_list = []
    if isinstance(faces, dict):
        print("RF Decoder Accepted the file", filename)
        for key, inner_dict in faces.items():
            inner_dict["id"] = key
            faces_list.append(inner_dict)
        faces_data = faces_list[0]
        x1, y1, x2, y2 = faces_data["facial_area"]
        landmarks = faces_data["landmarks"]
        point_right_eye = list(landmarks["right_eye"])
        a1 = int(point_right_eye[0])
        b1 = int(point_right_eye[1])
        point_mouth_left = list(landmarks["mouth_left"])
        a2 = int(point_mouth_left[0])
        b2 = int(point_mouth_left[1])
        half_d1 = int(int(math.sqrt((a1 - x1) ** 2 + (b1 - y1) ** 2) / 3) + int(
            math.sqrt((a1 - x1) ** 2 + (b1 - y1) ** 2) / 5))
        q_d1 = int(half_d1 / 2)
        x1n = x1 - half_d1
        y1n = y1 - half_d1 - q_d1
        half_d2 = int(math.sqrt((a2 - x2) ** 2 + (b2 - y2) ** 2) / 2)
        q_d2 = int(int(math.sqrt((a2 - x2) ** 2 + (b2 - y2) ** 2) / 3) + int(
            math.sqrt((a2 - x2) ** 2 + (b2 - y2) ** 2) / 5))
        x2n = x2 + half_d2 + q_d2
        y2n = y2 + half_d2 + q_d2

        if x1n and y1n and x2n and y2n:
            if x1n < 0:
                x1n = 0
            if y1n < 0:
                y1n = 0

        cropped_img = images[y1n:y2n, x1n:x2n]
        cv2.rectangle(images,(x1n,y1n),(x2n,y2n),(0,225,255),3)
        import matplotlib.pyplot as plt
        plt.imshow(images)
        plt.show()
        print(cropped_img)

        finalimage_height = cropped_img.shape[0]
        finalimage_width = cropped_img.shape[1]
        if cropped_img:
            cv2.imwrite(output + filename, cropped_img)
        else:

        # if finalimage_width > finalimage_height:
        #     workimgwidth = int(finalimage_width / float(finalimage_height / 241))
        #     workimgheight = int(finalimage_height / float(finalimage_width / 189))
        #     final_work_img = cv2.resize(cropped_img, (workimgwidth, workimgheight))
        #     cv2.imwrite(output + filename, final_work_img)
        # else:
        #     workimgwidth = int(finalimage_width / (float(finalimage_height / 241)))
        #     workimgheight = int(finalimage_height / (float(finalimage_width / 189)))
        #     final_work_img = cv2.resize(cropped_img, (workimgwidth, workimgheight))
        #     cv2.imwrite(output + filename, final_work_img)

if __name__ == "__main__":
    try:
        image = 'input/'
        output = 'output/'
        detached = 'detached/'
        filename = [f for f in os.listdir(image) if f.endswith('.jpg') or f.endswith('.JPG')]
        for filename in filename:
            path = os.path.join(image, filename)
            faceapp(path,filename,output)

    except RuntimeError as e:
        # Code to handle the exception
        print("An exception occurred", e)
