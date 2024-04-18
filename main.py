import tkinter as tk
from tkinter import filedialog
import os


def clean_file(input_file, output_file):
    try:
        # Open the input file in read mode and output file in write mode
        with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
            # Flag to track whether to skip lines
            skip_lines = False
            # Counter for lines within each entry
            line_counter = 0
            # Flag to track the start of a new entry
            start_of_entry = True
            # Read each line in the input file
            for line in f_in:
                # Check for REGION, COUNTY, ASSIGNED, and ERROR patterns
                if "REGION" in line:
                    f_out.write("REGION LINE: " + line)
                    start_of_entry = False
                    continue
                if "COUNTY" in line:
                    f_out.write("COUNTY LINE: " + line)
                    start_of_entry = False
                    continue
                if "ASSIGNED" in line:
                    f_out.write("Assigned Worker LINE: " + line)
                    start_of_entry = False
                    continue
                if "ERROR" in line:
                    line_counter = 0  # Reset line counter for new entry
                    f_out.write(f"Entry Line {line_counter + 1}: {line}")
                    start_of_entry = False
                    continue

                # Check if the line contains the unwanted pattern to start skipping lines
                if "STATE OF MONTANA" in line:
                    skip_lines = True
                    start_of_entry = False
                    continue  # Skip this line

                # Check if we are in the middle of the unwanted section
                if skip_lines:
                    # Check if we've reached the end of the unwanted section
                    if "RUN DATE" in line:
                        skip_lines = False
                    start_of_entry = False
                    continue  # Skip this line

                # Check if the line is empty (contains only whitespace characters)
                if line.strip():  # If the line is not empty
                    # Write the line to the output file
                    if start_of_entry:
                        line_counter = 0  # Start counting lines within entry from 0
                        f_out.write(f"Entry Line {line_counter + 1}: {line}")
                        start_of_entry = False
                    else:
                        line_counter += 1
                        f_out.write(f"Entry Line {line_counter + 1}: {line}")
                    start_of_entry = False

        return True
    except Exception as e:
        print(e)
        return False


def browse_input_file():
    filename = filedialog.askopenfilename()
    if filename:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, filename)


def browse_output_file():
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    if filename:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, filename)


def process_file():
    input_file = entry_input.get()
    output_file = entry_output.get()
    if not input_file:
        status_label.config(text="Please select an input file.")
        return
    if not output_file:
        status_label.config(text="Please select an output file.")
        return
    success = clean_file(input_file, output_file)
    if success:
        status_label.config(text="File processed successfully!")
        output_label.config(text=f"Output file: {output_file}")
    else:
        status_label.config(text="Error processing the file.")


# Create the main window
window = tk.Tk()
window.title("File Cleaner App")

# Create widgets
label_input = tk.Label(window, text="Select input file:")
label_input.pack()

entry_input = tk.Entry(window, width=50)
entry_input.pack()

browse_input_button = tk.Button(window, text="Browse", command=browse_input_file)
browse_input_button.pack()

label_output = tk.Label(window, text="Select output file:")
label_output.pack()

entry_output = tk.Entry(window, width=50)
entry_output.pack()

browse_output_button = tk.Button(window, text="Browse", command=browse_output_file)
browse_output_button.pack()

process_button = tk.Button(window, text="Process File", command=process_file)
process_button.pack()

status_label = tk.Label(window, text="")
status_label.pack()

output_label = tk.Label(window, text="")
output_label.pack()

# Run the GUI
window.mainloop()