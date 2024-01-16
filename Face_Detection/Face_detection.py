import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# this Initialize global variables
video_capture = None
#image = None

#This Function is to perform face detection on images
def detect_faces_image():
    global image
    global canvas


    # Load the pre-trained face detection classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Open a file dialog to select an image file
    file_path = filedialog.askopenfilename()

    if file_path:
        # Load the selected image
        image = cv2.imread(file_path)
        image = cv2.resize(image, (340, 380))

        # Convert the image to grayscale (face detection works on grayscale images)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Perform face detection
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Count the number of faces detected
        num_faces = len(faces)

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Convert the OpenCV image to a format that tkinter can display
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)

        # Update the tkinter canvas with the detected image
        canvas.config(image=image_tk)
        canvas.image = image_tk

        # Display the image size

        # Display the result
        result_label.config(text=f'Faces Detected: {num_faces}',fg="#000",bg="#d6cadd")

# This Function is to perform face detection from the camera 
# def detect_faces_camera():
#     global video_capture

#     if video_capture is not None:
#         # Release the video capture when switching to camera input
#         video_capture.release()

#     # Initialize video capture from the default camera (0)
#     video_capture = cv2.VideoCapture(0)

#     # Reduce the size of the camera feed
#     video_capture.set(3, 320)  # Width
#     video_capture.set(4, 240)  # Height

#     detect_faces()




# Function to continuously capture frames and perform face detection
def detect_faces():
    global image
    global canvas
    global original_image_label
    global video_capture
    global root

    if video_capture is not None:
        ret, frame = video_capture.read()

        if ret:
            # Load the pre-trained face detection classifier
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            if face_cascade.empty():
                result_label.config(text='Error: Haar Cascade Classifier XML file not found.')
                return

            # Convert the frame to grayscale (face detection works on grayscale images)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Perform face detection
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Count the number of faces detected
            num_faces = len(faces)

            # Draw rectangles around the detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Convert the OpenCV image to a format that tkinter can display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            frame_tk = ImageTk.PhotoImage(frame_pil)

            # Update the tkinter canvas with the detected image
            canvas.config(image=frame_tk)
            canvas.image = frame_tk

            # Display the original frame size

            # Display the result
            result_label.config(text=f' Faces Detected =  {num_faces}',fg="#990000",bg="#d6cadd")

            # Schedule the next frame capture and detection
            root.after(10, detect_faces)

# Create the main tkinter window
root = tk.Tk()
root.title("Face Detection GUI")
root.geometry("800x700")
root.configure(bg="#f0f0f0")  # Background color of the main window

# Create and configure title label
title_label = tk.Label(root, text="     Face Detection tool by sanket_ss    ", font=("Arial", 25), fg="#333333", bg="red")
title_label.pack(pady=20)

# Create buttons with custom styles
button_style = tk.Button(root, text="Open Image", command=detect_faces_image, font=("Arial", 16), fg="white", bg="#007acc", padx=10, pady=5)
button_style.pack(pady=10)



# camera_button = tk.Button(root, text="Camera ", command=detect_faces_camera, font=("Arial", 16), fg="white", bg="#007acc", padx=10, pady=5)
# camera_button.pack(pady=10)



# Create a canvas to display the image with detected faces
canvas = tk.Label(root, bg="#f0f0f0")
canvas.pack()

# Create a label to display the detection result
result_label = tk.Label(root, text='', font=('Arial', 22), fg="#333333", bg="#f0f0f0" ,padx=10, pady=5 )
result_label.pack()

# Run the tkinter main loop
root.mainloop()
