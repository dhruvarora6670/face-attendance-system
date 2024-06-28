import cv2
import os
import face_recognition
import pickle
from firebase_admin import credentials
import firebase_admin
from firebase_admin import storage

cred = credentials.Certificate("/Users/dhruvarora/Documents/Projects/AttendanceSystem/faceattendance-e74b5-firebase-adminsdk-ea67x-9d868ee225.json")
firebase_admin.initialize_app(cred,{
                                  'storageBucket': 'faceattendance-e74b5.appspot.com'
                              })

folderPath = '/Users/dhruvarora/Documents/Projects/AttendanceSystem/Images'
imageList = []
studentIds = []

# Ensure folderPath ends with a separator
if not folderPath.endswith('/'):
    folderPath += '/'

# Load images and student IDs
for path in os.listdir(folderPath):
    full_path = os.path.join(folderPath, path)
    if os.path.isfile(full_path):
        img = cv2.imread(full_path)
        imageList.append(img)
        studentIds.append(os.path.splitext(path)[0])

        # Sending Images to storage bucket in firebase
        fileName = os.path.basename(full_path)
        bucket = storage.bucket()
        blob = bucket.blob('Images/' + fileName)
        blob.upload_from_filename(full_path)

print(studentIds)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        encodeList.append(encode[0])


    return encodeList

print("Encoding Started")
encodeListKnown = findEncodings(imageList)
print("Encoding Complete")
encodeListKnownWithIds = [encodeListKnown, studentIds]
file = open("EncodeFile.p", "wb")
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")


