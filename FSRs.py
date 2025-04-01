import serial
import csv
import time

# Set the COM port and baud rate according to your Arduino configuration
arduino_port = 'COM6'  
baud_rate = 9600

# Open the serial port
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

# Create CSV file and write header
csv_file = open('FSR.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Sensor1', 'Sensor2', 'Time (s)'])

# Set the duration for data collection (in seconds)
collection_duration = 60
start_time = time.time()
end_time = time.time() + collection_duration

try:
    while time.time() < end_time:
        # Read data from Arduino
        data = ser.readline().decode('utf-8').strip()

        # Check if data is not empty
        if data:
            try:
                # Extract sensor values from the data
                pressure1, pressure2 = map(int, data.split(" "))

                # Get the current time in seconds
                current_time = time.time() - start_time

                # Write data to CSV file
                csv_writer.writerow([pressure1, pressure2, int(current_time)])
                print(f"Sensor1: {pressure1}, Sensor2: {pressure2} at {int(current_time)} seconds")

            except (ValueError, IndexError) as e:
                print(f"Error processing data: {e}. Raw data: {data}")

except KeyboardInterrupt:
    pass

finally:
    ser.close()
    csv_file.close()
    print("Data collection completed. CSV file saved.")
