import serial
import csv
import time

arduino_port = 'COM9'
baud_rate = 9600

# Open the serial port
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

# Create CSV file and write header
csv_file = open('USS.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Sound travel time', 'Thickness', 'Tension', 'Timestamp'])

# Set the duration for data collection (in seconds)
collection_duration = 60
start_time = time.time()

try:
    while time.time() - start_time < collection_duration:
        # Read data from Arduino
        data = ser.readline().decode('utf-8').strip()

        # Check if data is not empty
        if data:
            try:
                if data.strip() == "9":
                    duration = 0
                    thickness = 0
                    tension = 0
                else:
                    # Extract sensor values from the data
                    duration, thickness, tension = map(float, data.split(" "))

                # Get the current time in seconds
                current_time = time.time() - start_time

                # Write data to CSV file
                csv_writer.writerow([duration, thickness, tension, int(current_time)])
                print(f"Sound travel time: {duration}, Thickness: {thickness}, Tension: {tension} at {int(current_time)} seconds")

            except (ValueError, IndexError) as e:
                print(f"Error processing data: {e}. Raw data: {data}")

except KeyboardInterrupt:
    pass

finally:
    ser.close()
    csv_file.close()
    print("Data collection completed. CSV file saved.")




