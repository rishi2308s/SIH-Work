import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load and Analyze Data
uss_data = pd.read_csv('USS.csv')
fsr_data = pd.read_csv('FSR.csv', header=[0, 1])
temp_data = pd.read_csv('temperature_data.csv', encoding='latin1')
sound_travel_time_data = uss_data['Sound travel time']
thickness_data = uss_data['Thickness']
tension_data = uss_data['Tension']
ambient_temp_data = temp_data['Temperature (°C)']
pressure_1 = fsr_data['Sensor1']
pressure_2 = fsr_data['Sensor2']

speed_of_sound = 34300  # cm/s, assuming speed of sound in air in cm
distance_data = [(sound_travel_time / 2) * speed_of_sound for sound_travel_time in sound_travel_time_data]

thickness_threshold = (-6, 6)
tension_threshold = (2.5, 8)
distance_threshold = (min(distance_data), max(distance_data))
ambient_temp_threshold = (-15, 120)
pressure_1_threshold = pressure_2_threshold = (70, 120)

def calculate_health(thickness, tension, distance, ambient_temp, pressure_1, pressure_2):
    pressure_1_numeric = pd.to_numeric(pressure_1, errors='coerce')
    pressure_2_numeric = pd.to_numeric(pressure_2, errors='coerce')
    normalized_thickness = (thickness - thickness_threshold[0]) / (thickness_threshold[1] - thickness_threshold[0])
    normalized_tension = (tension - tension_threshold[0]) / (tension_threshold[1] - tension_threshold[0])
    normalized_distance = (distance - distance_threshold[0]) / (distance_threshold[1] - distance_threshold[0])
    normalized_ambient_temp = (ambient_temp - ambient_temp_threshold[0]) / (ambient_temp_threshold[1] - ambient_temp_threshold[0])
    normalized_pressure1 = (pressure_1_numeric - pressure_1_threshold[0]) / (pressure_1_threshold[1] - pressure_1_threshold[0])
    normalized_pressure2 = (pressure_2_numeric - pressure_2_threshold[0]) / (pressure_2_threshold[1] - pressure_2_threshold[0])
    health = 0.3 * normalized_thickness + 0.2 * normalized_tension + 0.1 * normalized_distance + 0.1 * normalized_ambient_temp + 0.15 * normalized_pressure1 + 0.15 * normalized_pressure2
    return pd.Series([health])  # Return as a pandas Series

current_health = calculate_health(thickness_data.iloc[-1], tension_data.iloc[-1], distance_data[-1], ambient_temp_data.iloc[-1], pressure_1.iloc[-1], pressure_2.iloc[-1])

print(current_health)

# Plotting the health graph over time
health_data = []
for i in range(len(thickness_data)):
    health = calculate_health(thickness_data[i], tension_data[i], distance_data[i], ambient_temp_data[i], pressure_1[i], pressure_2[i])
    health_data.append(health)

# Converting health data to a pandas Series for easy plotting
health_series = pd.concat(health_data, ignore_index=True)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(health_series, label='Health over Time')
plt.xlabel('Time')
plt.ylabel('Health')
plt.title('Health Graph over Time')
plt.legend()
plt.show()
