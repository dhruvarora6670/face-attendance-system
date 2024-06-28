import pickle
import cv2
import os
import cvzone
import face_recognition
from firebase_admin import credentials
import firebase_admin
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime

cred = credentials.Certificate("/Users/dhruvarora/Documents/Projects/AttendanceSystem/faceattendance-e74b5-firebase-adminsdk-ea67x-9d868ee225.json")
firebase_admin.initialize_app(cred,{
                                  'storageBucket': 'faceattendance-e74b5.appspot.com',
                                  'databaseURL': 'https://faceattendance-e74b5-default-rtdb.firebaseio.com/'
                              })

bucket = storage.bucket()

folderPath = '/Users/dhruvarora/Documents/Projects/AttendanceSystem/Images'
imageList = []
studentIds = []


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')
folderModePath = 'Resources/Modes/'
imageModeList = []
for path in os.listdir(folderModePath):
    imageModeList.append(cv2.imread(folderModePath + path))

file = open("EncodeFile.p", "rb")
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print(studentIds)

modeType = 3
counter = 0
id = -1

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imageModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            # print(matches)
            # print(faceDis)

            matchInd = np.argmin(faceDis)
            if matches[matchInd]:
                # print(studentIds[matchInd])
                # print("Known Face Detected")
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55+x1, 162+y1, x2-x1, y2-y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt = 0, colorC= [255,255,255])
                id = studentIds[matchInd]
                if counter == 0:
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                # Get Student Info
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)

                # Get Image
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.int8)
                img_student = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                # Update data
                datetimeObject = datetime.strptime(studentInfo['last_att_time'], "%Y-%m-%d %H:%M:%S")

                seconds_lapsed = (datetime.now() - datetimeObject).total_seconds()
                if seconds_lapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_att_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 0
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imageModeList[modeType]

            imgBackground[44:44 + 633, 808:808 + 414] = imageModeList[modeType]

            if modeType != 0:

                if 20 < counter < 30:
                    modeType = 2

                if counter <= 20:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861,125),
                                cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)

                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w,h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset = (414 - w)//2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808+offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175:175+216,909:909+216] = img_student
                counter+=1

                if counter >= 30:
                    counter = 0
                    modeType = 3
                    studentInfo = []
                    img_student = []

    else:
        modeType = 3
        counter = 0

    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
