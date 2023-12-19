import numpy as np
import torch
import pandas as pd
import cv2
import csv 

# load the custom YOLOv5 model 
model=torch.hub.load('ultralytic/yolov5','custom',path='best.pt',force_reload=True)
while True:
    #Initialize the video capture object to use the default camera
    cap=cv2.VideoCapture(0)
    base_path="cbcd_results" # the base path will be the folder in which you want all your .csv files  
    new_csv_file = latest_csv(base_path)

    #check if the camera opened succesfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Couldn't read frame.")
            break
        
        results=model.predict(frame)
        boxes=results.boxes

        left,right=numbers_boxes(boxes)
        left_marking=marking(left)
        right_marking=marking(right)
        crack=crack_boxes(boxes)

        if left_marking == 100 # the starting number 
            break 
        cracks_between , num_cracks =crack_in_between(left,right,crack)
        crack_size=calculate_crack_size(cracks_between)

        ## now we will append the data in .csv file which will have marking ranges ,number of cracks, their sizes 
        
        

        #latest_exp_directory is basically the path to the newly created .csv file
        append_in_csv(left_marking,right_marking,num_cracks,crack_size,latest_exp_directory)

cap.release()