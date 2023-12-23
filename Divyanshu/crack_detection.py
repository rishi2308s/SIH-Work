import cv2
import torch
import csv
import time

# Function to compare two cracks based on area and coordinates
def is_different_crack(crack1, crack2, threshold=0.1):
    area1, (x1, y1) = crack1
    area2, (x2, y2) = crack2

    area_diff = abs(area1 - area2) / float(max(area1, area2))
    coord_diff = max(abs(x1 - x2), abs(y1 - y2)) / max(frame_width, frame_height)

    return area_diff > threshold or coord_diff > threshold

# Load the custom YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
speed = 1
# Initialize the video capture object to use the default camera
cap = cv2.VideoCapture(0)
csv_file = open('cracks.csv', 'a+', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['S.No', 'Area', 'Time', 'Location'])
s_no = 1
start_time = time.time()
last_logged_crack = None  # Store the last logged crack details

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Read the first frame to get the dimensions
ret, frame = cap.read()
if not ret:
    print("Error: Couldn't read frame.")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Define the dimensions of the frame
frame_height, frame_width = frame.shape[:2]

# Define the ROI as a small vertical strip in the center
strip_width = 20
roi_x1 = frame_width // 2 - strip_width // 2
roi_y1 = 0
roi_width = strip_width
roi_height = frame_height

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read frame.")
        break

    cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x1 + roi_width, roi_y1 + roi_height), (255, 0, 0), 2)
    results = model(frame)

    for detection in results.pred[0]:
        *xyxy, conf, cls = detection
        if results.names[int(cls)] == 'crack':
            x1, y1, x2, y2 = map(int, xyxy)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, "Crack", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if (x1 >= roi_x1 and x2 <= roi_x1 + roi_width) and (y1 >= roi_y1 and y2 <= roi_y1 + roi_height):
                crack_area = (x2 - x1) * (y2 - y1)
                crack_center = ((x1 + x2) // 2, (y1 + y2) // 2)
                current_crack = (crack_area, crack_center)
                if last_logged_crack is None or is_different_crack(last_logged_crack, current_crack):
                    current_time = time.time() - start_time
                    csv_writer.writerow([s_no, crack_area, int(current_time), int(current_time*speed)])
                    last_logged_crack = current_crack
                    s_no += 1
                    print("New crack found and logged")

    cv2.imshow('YOLOv5n Live Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
csv_file.close()
