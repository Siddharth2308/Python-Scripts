import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import messagebox

def upload_binary_file(port, file_path):
    try:
        # Open the serial port
        ser = serial.Serial(port, 115200)  # Adjust the baud rate if necessary

        with open(file_path, 'rb') as file:
            # Read the binary data from the file
            binary_data = file.read()

            # Upload the binary data to the microcontroller
            ser.write(binary_data)

        ser.close()
        print("Binary file uploaded successfully.")
    except Exception as e:
        print(f"Error uploading binary file: {e}")

def get_microcontroller_details():
    microcontrollers = []
    
    # Get a list of all available serial ports
    available_ports = list(serial.tools.list_ports.comports())

    for port, desc, hwid in available_ports:
        # Check if it's an Arduino Uno
        if 'arduino' in desc.lower() or 'arduino' in hwid.lower():
            microcontroller = {
                'port': port,
                'name': 'Arduino Uno',
                'architecture': 'ATmega328P',  # You may want to double-check this for your specific board
                'required_drivers': 'CH340 driver (Windows), no drivers required for macOS and Linux.'
            }
            microcontrollers.append(microcontroller)

        # Check if it's an ESP32 (you can add more checks for different ESP32 boards)
        elif 'cp210' in hwid.lower():  # Example: ESP32 DEVKIT V1 (CP210x)
            microcontroller = {
                'port': port,
                'name': 'ESP32',
                'architecture': 'XTensa LX6',
                'required_drivers': 'CP210x USB to UART Bridge VCP driver (Windows), ' \
                                    'CP210x driver (macOS), no drivers required for Linux.'
            }
            microcontrollers.append(microcontroller)

    return microcontrollers

def send_numeric_input(port, value_entry):
    try:
        ser = serial.Serial(port, 115200)  # Open the serial port

        try:
            value = int(value_entry.get())
            ser.write(str(value).encode())  # Convert int to string and send it as bytes
            print(str(value).encode())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter the Pin Number you want to test.")
            return

        ser.close()
        messagebox.showinfo("Success", "Numeric value sent via serial communication.")
    except Exception as e:
        messagebox.showerror("Error", f"Error during serial communication: {e}")

def show_selected_microcontroller_details(selected_var, details_text, connected_microcontrollers):
    selected_port = selected_var.get()

    for mc in connected_microcontrollers:
        if mc['port'] == selected_port:
            details_text.delete(1.0, tk.END)
            details_text.insert(tk.END, f"Name: {mc['name']}\n")
            details_text.insert(tk.END, f"Port: {mc['port']}\n")
            details_text.insert(tk.END, f"Architecture: {mc['architecture']}\n")
            details_text.insert(tk.END, f"Required Drivers: {mc['required_drivers']}\n")
            break

def main():
    connected_microcontrollers = get_microcontroller_details()

    if not connected_microcontrollers:
        messagebox.showinfo("No Microcontroller Found", "No microcontroller found.")
        return

    root = tk.Tk()
    root.title("Microcontroller Communication")
    root.geometry("600x400")

    label = tk.Label(root, text="Select the microcontroller:")
    label.pack(pady=10)

    selected_var = tk.StringVar()
    selected_var.set(connected_microcontrollers[0]['port'])
    for mc in connected_microcontrollers:
        radio_button = tk.Radiobutton(root, text=f"{mc['name']} ({mc['port']})", variable=selected_var, value=mc['port'])
        radio_button.pack(anchor=tk.W)

    details_text = tk.Text(root, height=10, width=50)
    details_text.pack(pady=10)

    show_selected_microcontroller_details(selected_var, details_text, connected_microcontrollers)

    value_label = tk.Label(root, text="Enter a numeric value:")
    value_label.pack(pady=5)

    value_entry = tk.Entry(root)
    value_entry.pack(pady=5)

    def send_value():
        send_numeric_input(selected_var.get(), value_entry)

    send_button = tk.Button(root, text="Send Value", command=send_value)
    send_button.pack(pady=10)

    root.mainloop()

            
if __name__ == "__main__":
    main()
