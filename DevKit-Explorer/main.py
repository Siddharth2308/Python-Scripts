import serial
import serial.tools.list_ports

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
            file_path = 'test.ino.standard.hex'
            upload_binary_file(microcontroller, file_path)

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

def send_numeric_input(port):
    try:
        ser = serial.Serial(port, 115200)  # Open the serial port

        while True:
            user_input = input("Enter a numeric value (or 'q' to quit): ")

            if user_input.lower() == 'q':
                break

            try:
                value = int(user_input)
                ser.write(str(value).encode())  # Convert int to string and send it as bytes
                print(str(value).encode())
            except ValueError:
                print("Invalid input. Please enter a valid numeric value or 'q' to quit.")

        ser.close()
        print("Serial communication closed.")
    except Exception as e:
        print(f"Error during serial communication: {e}")


def main():
    connected_microcontrollers = get_microcontroller_details()

    if not connected_microcontrollers:
        print("No microcontroller found.")
    else:
        for index, mc in enumerate(connected_microcontrollers, 1):
            print(f"Microcontroller {index}:")
            print(f"  Name: {mc['name']}")
            print(f"  Port: {mc['port']}")
            print(f"  Architecture: {mc['architecture']}")
            print(f"  Required Drivers: {mc['required_drivers']}")
            print()

        # Example usage of the send_numeric_input function
        selected_microcontroller_index = int(input("Select the microcontroller (enter the number): ")) - 1
        if 0 <= selected_microcontroller_index < len(connected_microcontrollers):
            selected_port = connected_microcontrollers[selected_microcontroller_index]['port']
            send_numeric_input(selected_port)
        else:
            print("Invalid selection. Exiting...")

            
if __name__ == "__main__":
    main()
