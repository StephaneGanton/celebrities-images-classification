from unittest import result
import cv2
import joblib
import json
import numpy as np
import base64
from wavelet import w2d

__class_name_to_number = {}
__class_number_to_name = {}
__model = None

def classify_image(image_base64_data, file_path=None):
    images = get_cropped_image_if_two_eyes(file_path, image_base64_data)

    result = []

    for img in images:
        scalled_raw_img = cv2.resize(img,(32,32))
        img_har = w2d(img, 'db1',5)
        scalled_har_img = cv2.resize(img_har,(32,32))
        
        combined_img = np.vstack((scalled_raw_img.reshape(32*32*3,1), scalled_har_img.reshape(32*32,1)))#the secont image doesn't has third dimension(rgb value) as it is a gray image (no color)

        len_image_array = 32*32*3 + 32*32

        final_image = combined_img.reshape(1, len_image_array).astype(float) #float because some APIs we're going to use expect float datatype

        # Now, we need our model
        #return the class as number (based on the class_dictionary..)
        #we can now convert number to string class name using class_number_to_name function we defined below

        predicted_class_number = __model.predict(final_image)[0]
        predicted_class_name = class_number_to_name(predicted_class_number)

        result.append({
            'class': predicted_class_name,
            'class_probabilty': np.round(__model.predict_proba(final_image)*100 , 2).tolist()[0],
            'class_dictionary': __class_number_to_name # as we need it on the UI
        })

    
    return result 

#### check on web, scikit-learn issue : API Inconsistency of predict and predict_proba in SVC


def load_saved_artifacts():
    file_path = './artifacts/'
    print("Loading saved artifacts... start")
    global __class_name_to_number
    global __class_number_to_name

    with open(file_path + "class_dictionary.json", 'r') as f:
        __class_name_to_number = json.load(f)
        __class_number_to_name = {v:k for k,v in __class_name_to_number.items()}

    
    global __model
    with open(file_path + "saved_model.pkl", 'rb') as f:
        __model = joblib.load(f)
    print("Loading saved artifacts...done")


#convert number to string class name :
def class_number_to_name(class_num):
    return __class_number_to_name[class_num]

def get_cv2_image_from_base64_string(base64_str): #take a base64 string and return a cv2 image
    '''
    from stackoverflow
    :Param: uri
    :return: cv2 image
    '''
    encode_data = base64_str.split(',')[1]
    np_array = np.frombuffer(base64.b64decode(encode_data), np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    return img


def get_cropped_image_if_two_eyes(image_path, image_base64_data):
        
    haar_path = '../model/opencv/haarcascades/'
    face_cascade = cv2.CascadeClassifier(haar_path +'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier( haar_path + 'haarcascade_eye.xml' )

    if image_path:
        img = cv2.imread(image_path)
    else:
        img = get_cv2_image_from_base64_string(image_base64_data)

    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    cropped_faces = []

    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >=2:
            cropped_faces.append(roi_color)
            
    return cropped_faces

#read a base64 Image format
def get_b64_test_image_for_virat():
    with open("b64.txt") as f:
        return f.read()

if __name__ == '__main__':
    load_saved_artifacts()
    #print(classify_image(get_b64_test_image_for_virat(), None))

    #Tests using images path
    """print(classify_image(None, "./test_images/federer1.jpg"))
    print(classify_image(None, "./test_images/federer2.jpg"))
    print(classify_image(None, "./test_images/virat1.jpg"))"""
    #print(classify_image(None, "./test_images/virat2.jpg"))

    print(classify_image(None, "./test_images/virat3.jpg"))

