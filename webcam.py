import cv2
from ultralytics import YOLO

# Load the trained YOLOv8 model
model = YOLO('/Users/vaneezafatima/Desktop/CDIO_GolfBot/train4/weights/best.pt')

# Class names corresponding to your dataset
class_names = ['big-goal', 'blue-golf-balls', 'green-golf-balls', 'obstacle', 'orange-golf-balls', 'purple-pink-golf-balls', 'red-golf-balls', 'robot', 'small-goal', 'white-golf-balls', 'yellow-golf-balls']

# Initialize the webcam
cap = cv2.VideoCapture(0)  # Use 0 for the default webcam. Change if you have multiple cameras.

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform inference on the frame with a lower confidence threshold
    results = model(frame, conf=0.25)

    # Visualize the results on the frame
    annotated_frame = frame.copy()  # Make a copy of the frame to annotate
    for result in results:
        for box in result.boxes:
            # Draw the bounding box
            x1, y1, x2, y2 = box.xyxy[0].int().tolist()
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Get the class name and confidence
            class_name = class_names[int(box.cls[0])]
            confidence = box.conf[0]
            # Draw the label
            label = f'{class_name}: {confidence:.2f}'
            cv2.putText(annotated_frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame with detections
    cv2.imshow('YOLOv8 Inference', annotated_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
