# Real-Time Face Attendance System

This project is a Real-Time Face Attendance System built using Python. It leverages computer vision and cloud technologies to automate and streamline attendance tracking. 

## Features

- 📹 **Real-Time Video Capture**: Uses OpenCV to capture live video.
- 🧑‍🤝‍🧑 **Face Detection and Recognition**: Utilizes the `face_recognition` library for accurate face detection and recognition.
- 🌐 **Firebase Integration**: Employs Firebase Admin SDK for real-time database management and storage.
- 📊 **User-Friendly Interface**: Displays attendance information with an intuitive interface.

## Libraries and Technologies

- **Python**: The programming language used for development.
- **OpenCV**: For video capturing and image processing.
- **face_recognition**: For face detection and recognition.
- **Firebase Admin SDK**: For database and storage management.
- **NumPy**: For numerical operations and data management.
- **Pickle**: For saving and loading encoded face data.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/face-attendance-system.git
    cd face-attendance-system
    ```

2. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up Firebase:
    - Create a Firebase project and download the service account key.
    - Save the JSON file to your project directory and update the path in the code.

## Usage

1. **Initialize Firebase**:
    ```python
    from firebase_admin import credentials, initialize_app

    cred = credentials.Certificate("path/to/your/firebase-key.json")
    initialize_app(cred, {
        'storageBucket': 'your-project-id.appspot.com',
        'databaseURL': 'https://your-database-name.firebaseio.com/'
    })
    ```

2. **Encode Faces**:
    - Store images in the specified directory.
    - Run the script to encode faces and save the data.
    ```python
    python encode_faces.py
    ```

3. **Run the Attendance System**:
    ```python
    python attendance_system.py
    ```

## Project Structure

- `attendance_system.py`: Main script for running the real-time attendance system.
- `encode_faces.py`: Script for encoding faces and saving the data.
- `requirements.txt`: List of required libraries.
- `Resources/`: Directory containing background images and other resources.
- `Images/`: Directory for storing face images.

## Contributing

Feel free to fork this repository, create a feature branch, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments

- Inspired by various computer vision and machine learning projects.
- Special thanks to the creators of the libraries used in this project.

Feel free to connect if you have any questions or suggestions!

![Real-Time Face Attendance System](https://share.icloud.com/photos/002G8eUjns7L14g4wVc1IQOaw)