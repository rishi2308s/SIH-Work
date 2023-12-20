import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt

# Function to update the graph from CSV
def update_graph(figure, ax, canvas):
    # Read the latest data from CSV file
    data = pd.read_csv('Test.csv')  # Update this path
    x = data['Day']  # Replace with your actual column name
    y = data['Temp']  # Replace with your actual column name

    # Clear the current plot and plot the new data
    ax.clear()
    ax.plot(x, y, 'r-')  # Adjust plot style as needed

    # Redraw the graph
    canvas.draw()

    # Schedule the next update (adjust the interval as needed)
    window.after(1000, update_graph, figure, ax, canvas)

# Initialize the main window
window = tk.Tk()
window.title("MineSense Display")
window.configure(bg='black')

# Header frame
header_frame = tk.Frame(window, bg='darkslategray')
header_frame.pack(side='top', fill='x')

# Header content
logo_label = tk.Label(header_frame, text="MineSense Display", font=('Arial', 24), fg='white', bg='darkslategray')
logo_label.pack(side='left', padx=10)

date_label = tk.Label(header_frame, text="Monday,14 December,2023", font=('Arial', 16), fg='white', bg='darkslategray')
date_label.pack(side='right', padx=10)

# Main content frame
content_frame = tk.Frame(window, bg='darkslategray')
content_frame.pack(expand=True, fill='both', padx=20, pady=20)

# Left sidebar for navigation
nav_frame = tk.Frame(content_frame, bg='darkslategray')
nav_frame.pack(side='left', fill='y')

# Navigation buttons
nav_button1 = tk.Button(nav_frame, text="Dashboard", bg='lightgray')
nav_button1.pack(pady=10, padx=10, fill='x')

nav_button2 = tk.Button(nav_frame, text="Sensor Data", bg='lightgray')
nav_button2.pack(pady=10, padx=10, fill='x')

# Right side content
right_frame = tk.Frame(content_frame, bg='darkslategray')
right_frame.pack(side='right', expand=True, fill='both')

# Create a figure for the plot
fig, ax = plt.subplots()

# Create the matplotlib canvas
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# Initial call to start the graph update
update_graph(fig, ax, canvas)

# Footer frame
footer_frame = tk.Frame(window, bg='darkslategray')
footer_frame.pack(side='bottom', fill='x')

# Footer content
maintenance_label = tk.Label(footer_frame, text="Next Predicted Maintenance : 20 January, 2024", font=('Arial', 16), fg='white', bg='darkslategray')
maintenance_label.pack(pady=10)

# Start the Tkinter loop
window.mainloop()
