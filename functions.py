# this function will return boxes for numbers 
def numbers_boxes(boxes_from_model): # assuming in a frame two numbers will appear together

    boxes_for_numbers=np.copy(boxes_from_model)

    
    non_crack_rows = boxes_for_numbers[:, 5] != 'crack' # non_crack_rows will be a boolean array
    boxes_for_numbers = boxes_for_numbers[non_crack_rows, :]

    if boxes_for_numbers.shape != (6, 6):
        print("Input array must have shape (6, 6).")
        return None, None
    
    # Calculate the mean of the first column (array[0])
    mean_value = np.mean(boxes_for_numbers[:, 0])
    
    # Use boolean masks to split the array into two based on the mean
    left_marking = boxes_for_numbers[boxes_for_numbers[:, 0] < mean_value]
    right_marking = boxes_for_numbers[boxes_for_numbers[:, 0] >= mean_value]
    
    return left_marking, right_marking   # it will return both left and right markings, they will be of size (3,6)


#this function will return rows boxes for crack
def crack_boxes(boxes_from_model):
    boxes_for_cracks=np.copy(boxes_from_model)

    non_numbers_rows=boxes_for_cracks[:,5] == 'crack' # non_numbers_rows will be a boolean array
    boxes_for_cracks= boxes_for_cracks[non_numbers_rows,:]
    return boxes_for_cracks 

# marking() will give us the Y_coordinates of numbers in the frame 

def crack_in_between(left_coordinates,right_coordinates,crack_coordinates):
    # this function will check if any crack is present between left and right numbers.
    # we will check if the x coordinates of all the cracks are lying between leftcoordinates of rightcoordinates
    if len(left_coordinates) == 0 or len(right_coordinates) == 0 or len(crack_coordinates) == 0:
        print("Input arrays cannot be empty.")
        return None

    # Extract the first elements (X values) from the arrays
    left_x = left_coordinates[:, 0]
    right_x = right_coordinates[:, 0]
    crack_x = crack_coordinates[:, 0]

    # Check if there are any cracks between the left and right coordinates
    mask = np.logical_and(left_x < crack_x, crack_x < right_x)
    cracks_between = crack_coordinates[mask]
    num_cracks=cracks_between.shape[0]


    return cracks_between , num_cracks


def calculate_crack_size(crack_coordinates):

 # since each row in this 2d numpy array is of 6 collumns

    # Sort the crack_coordinates based on y1
    sorted_crack_coordinates = crack_coordinates[crack_coordinates[:, 1].argsort()]

    # Extract x1, y1, x2, y2 from sorted crack_coordinates
    x1, y1, x2, y2 = sorted_crack_coordinates[:, :4].T # here x1 y1 will be the 1d arrays containing all the top left points 

    # Calculate height and width for each crack
    height = y2 - y1
    width = x2 - x1

    # Combine height and width into a 2D array
    size_array = np.column_stack((height, width))

    return size_array



def marking(Numbers):  # here but leftNumber and rightNumbers one by one is basically is basically the array returned by numbers_box() , see numbers_box()
      # Your implementation here to combine the detected numbers

    Y_coordinates=np.copy(Numbers[:,1]).astype(float) # we will create Y_coordinates function and it will collect the y coords of all the numbers
    # the job of this function is to use the boxes and find the number markings

    # sorted the Y_coordinates
    numbers_Y= np.sort(Y_coordinates)

    # select the first column of the array

    combined_number = ''.join(map(str, numbers_Y))
    return combined_number 

# marking will give us the final number like 415 

# marking(rightNumbers) , marking(leftNumbers)


## basically we will pass an array which hold all the info about crack location , if this array is empty which means no crack is found
def crack_found(crack_coordinates): # crack_coordinates will be the array from crack_boxes
    
    if crack_coordinates.size == 0:
        return False
    else:
        return True

def number_found(number_coordinates): # number_coordinates will be the array from number_boxes
    if number_coordinates.size==0:
        return False
    else:
        return True 
    
import csv
import numpy as np


## append_in_csv function will append the data into the new rows in the existing file_path
def append_in_csv(left_marking, right_marking, num_cracks, crack_sizes, csv_path):
    # Check if the CSV file already exists
    file_exists = False
    try:
        with open(csv_path, 'r') as file:
            file_exists = True
    except FileNotFoundError:
        pass

    # Open the CSV file in append mode
    with open(csv_path, 'a', newline='') as file:
        writer = csv.writer(file)

        # If the file doesn't exist, write the header
        if not file_exists:
            writer.writerow(['Left Marking', 'Right Marking', 'Number of Cracks', 'Height', 'Width', 'Area'])

        # Iterate over cracks and append a row for each
        for i in range(num_cracks):
            # Calculate area from height and width
            area = crack_sizes[i, 0] * crack_sizes[i, 1]

            # Append a row to the CSV file
            writer.writerow([left_marking, right_marking, num_cracks, crack_sizes[i, 0], crack_sizes[i, 1], area])

## Example usage:
# left_marking = 110
# right_marking = 111
# num_cracks = 2
# crack_sizes = np.array([[5, 10], [7, 15]])  # Example crack sizes
# csv_path = 'output.csv'

# make_csv(left_marking, right_marking, num_cracks, crack_sizes, csv_path)

def latest_csv(base_path):
    # Join the base path with the 'exp' prefix and '.csv' extension
    search_path = os.path.join(base_path, 'exp*.csv')

    # Get a list of CSV files matching the pattern
    csv_files = [f for f in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, f)) and f.startswith('exp') and f.endswith('.csv')]

    # Sort the CSV files by their numerical part and get the latest one
    latest_csv_file = max(csv_files, key=lambda x: int(x[3:-4]) if x[3:-4].isdigit() else 0, default=None)

    # Return the address of the latest CSV file
    if latest_csv_file:
        return os.path.join(base_path, latest_csv_file)
    else:
        return None
    