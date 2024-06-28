import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("faceattendance-e74b5-firebase-adminsdk-ea67x-9d868ee225.json")
firebase_admin.initialize_app(cred,{
                                  'databaseURL': 'https://faceattendance-e74b5-default-rtdb.firebaseio.com/'
                              })

ref = db.reference('Students')

data = {
    "Dhruv-54321266":
        {
            "name": "Dhruv Arora",
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 6,
            "standing": "G",
            "year": 4,
            "last_att_time": "2024-06-27 10:00:00"
        },
    "Elon_Musk":
        {
            "name": "Elon Musk",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 2,
            "standing": "G",
            "year": 3,
            "last_att_time": "2024-06-27 12:00:00"
        },
    "tim-cook_image":
        {
            "name": "Tim Cook",
            "major": "CSE",
            "starting_year": 2020,
            "total_attendance": 10,
            "standing": "G",
            "year": 5,
            "last_att_time": "2024-06-27 10:00:00"
        }
}

for key, value in data.items():
    ref.child(key).set(value)
