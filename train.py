from ultralytics import YOLO

# Load a pretrained YOLOv8 model
model = YOLO('yolov8n.pt')  # Replace 'yolov8n.pt' with the correct model file

# Train the model with more epochs
model.train(data='/Users/vaneezafatima/Desktop/CDIO_GolfBot/CDIO.v8i.yolov8/data.yaml', epochs=30, task='detect')
