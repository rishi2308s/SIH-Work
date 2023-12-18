import cv2
import torch

# Load the custom YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)

# Initialize the video capture object to use the default camera
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read frame.")
        break

    # Perform inference
    results = model(frame)

    # Annotate image
    annotated_frame = results.render()[0]

    for detection in results.pred[0]:
        # Each detection is a tensor containing [x1, y1, x2, y2, confidence, class]
        *xyxy, conf, cls = detection
        label = f'{results.names[int(cls)]} {conf:.2f}'
        c1, c2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))

        # Draw rectangle to frame
        annotated_frame = cv2.rectangle(frame, c1, c2, (0,255,0), 2)

        # If the detected object is a crack, calculate and display its size
        if results.names[int(cls)] == 'crack':
            crack_width = c2[0] - c1[0]
            crack_height = c2[1] - c1[1]
            crack_area = crack_width*crack_height
            crack_size_label = f'Area: {crack_area}px'
            annotated_frame = cv2.putText(frame, crack_size_label, (c1[0], c1[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

    # Display the resulting frame
    cv2.imshow('YOLOv5n Live Detection', annotated_frame)

    # Press 'q' to quit the video stream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
