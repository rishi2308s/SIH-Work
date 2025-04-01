import serial
import csv
import time
arduino_port = 'COM6'  
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

csv_file = open('temperature_data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Temperature (°C)', 'Time (s)'])
collection_duration = 60
start_time = time.time()
end_time = time.time() + collection_duration

try:
    while time.time() < end_time:
        data = ser.readline().decode('latin-1').strip()

        if data:
            try:
                ambient_temp = float(data.replace(' Â°C', ''))
                current_time = time.time() - start_time
                csv_writer.writerow([ambient_temp, int(current_time)])
                print(f"Temperature: {ambient_temp}°C at {int(current_time)} seconds")
            except ValueError as e:
                print(f"Error processing data: {e}. Raw data: {data}")

except KeyboardInterrupt:
    pass

finally:
    ser.close()
    csv_file.close()
    print("Data collection completed. CSV file saved.")
