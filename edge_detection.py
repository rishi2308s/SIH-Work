### This code will provide real time edge detection using Canny edge Detection

import cv2
import numpy as np

# custom canny edge detection code
def canny_edge_detection(frame): 
	# Convert the frame to grayscale for edge detection 
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
	
	# Apply Gaussian blur to reduce noise and smoothen edges 
	blurred = cv2.GaussianBlur(src=gray, ksize=(3, 5), sigmaX=0.5) 
	
	# Perform Canny edge detection 
	edges = cv2.Canny(blurred, 70, 135) 
	
	return blurred, edges


	# Open the default webcam 
cap = cv2.VideoCapture(0) 

    ## now we need to remove all the horizonatal edges and keep only vertical edge 

def extract_vertical_edges(edges):
    # Use Hough Line Transform to detect lines
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    # Create a binary mask to extract vertical lines
    vertical_mask = np.zeros_like(edges)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
            if np.abs(angle) < 45:  # Consider lines with an angle less than 45 degrees as vertical
                cv2.line(vertical_mask, (x1, y1), (x2, y2), 255, 2)

    # Bitwise AND operation to extract vertical edges
    horizontal_edges = cv2.bitwise_and(edges, vertical_mask)

    return horizontal_edges

# check if the dislodgement is there or not, the principle is that all the edges should lie between the upper and lower bound
def dislodgement(horizontal_edges, upper_bound, lower_bound):
    # Calculate the sum of pixel values along the vertical axis
    vertical_projection = np.sum(horizontal_edges, axis=0)

    # Check if any value in the vertical projection is outside the specified bounds
    dislodged = any(value < lower_bound or value > upper_bound for value in vertical_projection)

    return dislodged

while True: 
    # Read a frame from the webcam 
    ret, frame = cap.read() 
    if not ret: 
        print('Image not captured') 
        break
    
    # Perform Canny edge detection on the frame 
    blurred, edges = canny_edge_detection(frame) 
    vertical_edges=extract_vertical_edges(edges)


    # Display the original frame and the edge-detected frame 
    #cv2.imshow("Original", frame) 
    cv2.imshow("Blurred", blurred) 
    cv2.imshow("Edges", edges) 
    # Display the veritcal edges
    cv2.imshow("Vertical Edges",vertical_edges)


    # Exit the loop when 'q' key is pressed 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break


# Release the webcam and close the windows 
cap.release() 
cv2.destroyAllWindows()


