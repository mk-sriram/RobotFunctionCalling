import google.generativeai as genai
import os
from dotenv import load_dotenv
import serial
import time

# Initialize serial connection in this module
ser = serial.Serial("/dev/cu.usbmodem111201", baudrate=9600, timeout=1)
time.sleep(1)  # Wait for the connection to stabilize

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the .env file
api_key = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API
genai.configure(api_key=api_key)

# Define the servo control function
def move_servo(angle: int) -> str:
    """
    Moves the servo to the specified angle.
    
    Args:
        angle (int): The angle to move the servo to (0-180).
    Returns:
        str: Confirmation message.
    """
    print(f"Servo is moving to {angle} degrees...")
    
    if 0 <= angle <= 180:
        command = f"{angle}\n"  # Format the angle command
        ser.write(command.encode())  # Send the command via serial
        print(f"Servo moved to {angle} degrees.")
    else:
        raise ValueError("Angle must be between 0 and 180 degrees.")
    return f"Servo moved to {angle} degrees."

# Define the servo control function
def move_servo_continuously(angle_start: int, angle_end: int, delay: float = 0.05) -> str:
    """
    Moves the servo continuously between two specified angles.

    Args:
        angle_start (int): The starting angle (0-180).
        angle_end (int): The ending angle (0-180).
        step (int): The increment step for each movement (default: 1).
        delay (float): The delay between movements in seconds (default: 0.05).

    Returns:
        str: Confirmation message after completing the movement.
    """
    if not (0 <= angle_start <= 180) or not (0 <= angle_end <= 180):
        raise ValueError("Angles must be between 0 and 180 degrees.")

    print(f"Servo is moving from {angle_start} to {angle_end} degrees...")

    if angle_start < angle_end:
        # Moving forward
        for angle in range(int(angle_start), int(angle_end) + 1, 10):
            command = f"{angle}\n"
            ser.write(command.encode())  # Send the command via serial
            time.sleep(delay)  # Delay to allow the servo to move
    else:
        # Moving backward
        for angle in range(int(angle_start), int(angle_end) - 1, 10):
            command = f"{angle}\n"
            ser.write(command.encode())  # Send the command via serial
            time.sleep(delay)  # Delay to allow the servo to move

    print(f"Servo completed movement from {angle_start} to {angle_end}.")
    return f"Servo moved continuously from {angle_start} to {angle_end} degrees."


# Set up the model with the function
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[move_servo, move_servo_continuously]
)

# Start a chat session
chat = model.start_chat(enable_automatic_function_calling=True)

# CLI interaction
def cli_interaction():
    print("Type your command to move the servo (type 'exit' to quit).")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Send the user input to Gemini
        response = chat.send_message(user_input)

        # Handle response
        print("Gemini Response:", response.text)

# Run the CLI
if __name__ == "__main__":
    cli_interaction()
