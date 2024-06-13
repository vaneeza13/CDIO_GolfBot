from flask import Flask, request, jsonify
import cv2
from ultralytics import YOLO
import socket
import threading
import os
import json

app = Flask(__name__)

# Load the trained YOLOv8 model
model = YOLO('/Users/vaneezafatima/Desktop/CDIO_GolfBot/train4/weights/best.pt')  # Update this path to your model
class_names = ['big-goal', 'blue-golf-balls', 'green-golf-balls', 'obstacle', 'orange-golf-balls', 'purple-pink-golf-balls', 'red-golf-balls', 'robot', 'small-goal', 'white-golf-balls', 'yellow-golf-balls']

# Initialize the webcam
cap = cv2.VideoCapture(0)  # Use 0 for the default webcam. Change if you have multiple cameras.

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

ball_position = None
robot_position = None

def webcam_processing():
    global ball_position, robot_position
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform inference on the frame with a lower confidence threshold
        results = model(frame, conf=0.25)

        # Initialize variables to store positions
        ball_position = None
        robot_position = None

        # Visualize the results on the frame
        annotated_frame = frame.copy()  # Make a copy of the frame to annotate
        for result in results:
            for box in result.boxes:
                # Get the class name
                class_name = class_names[int(box.cls[0])]
                if class_name == 'orange-golf-balls':
                    # Get the bounding box
                    x1, y1, x2, y2 = box.xyxy[0].int().tolist()
                    ball_position = ((x1 + x2) // 2, (y1 + y2) // 2)  # Calculate the center of the bounding box
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    # Get the class name and confidence
                    confidence = box.conf[0]
                    # Draw the label
                    label = f'{class_name}: {confidence:.2f}'
                    cv2.putText(annotated_frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                elif class_name == 'robot':
                    # Get the bounding box
                    x1, y1, x2, y2 = box.xyxy[0].int().tolist()
                    robot_position = ((x1 + x2) // 2, (y1 + y2) // 2)  # Calculate the center of the bounding box
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    # Get the class name and confidence
                    confidence = box.conf[0]
                    # Draw the label
                    label = f'{class_name}: {confidence:.2f}'
                    cv2.putText(annotated_frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                elif class_name == 'white-golf-balls':
                    # Get the bounding box
                    x1, y1, x2, y2 = box.xyxy[0].int().tolist()
                    robot_position = ((x1 + x2) // 2, (y1 + y2) // 2)  # Calculate the center of the bounding box
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    # Get the class name and confidence
                    confidence = box.conf[0]
                    # Draw the label
                    label = f'{class_name}: {confidence:.2f}'
                    cv2.putText(annotated_frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Display the frame with detections
        cv2.imshow('YOLOv8 Inference', annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

def socket_server():
    global ball_position, robot_position
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9090))
    server_socket.listen(1)

    print("Socket server listening on port 9090")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                if ball_position and robot_position:
                    client_socket.sendall(json.dumps({
                        "ball_position": ball_position,
                        "robot_position": robot_position
                    }).encode())
                else:
                    client_socket.sendall(json.dumps({
                        "ball_position": None,
                        "robot_position": None
                    }).encode())
            except ConnectionResetError:
                break
        
        client_socket.close()
        print(f"Connection from {addr} closed")

# Start the socket server in a separate thread
socket_thread = threading.Thread(target=socket_server)
socket_thread.start()

# Run webcam processing in the main thread
webcam_processing()
