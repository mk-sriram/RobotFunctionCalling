### Controls

#### 1. Move Each Servo Separately by Certain Values

- Create individual functions for each servo (`move_servo_1`, `move_servo_2`, ..., `move_servo_6`).
  - Each function takes an angle (0-180) as input.
  - Validate the input range.
  - Send the corresponding command via serial to move the specific servo.
- Include logging to track the current position of each servo for debugging.

#### 2. Each Servo Function Works Together

- Define a `move_arm` function to take a list of six angles `[angle1, angle2, ..., angle6]`.
  - Call each individual servo function with its respective angle.
  - Ensure synchronization by adding slight delays if needed.
  - Validate the angles to avoid overloading or mechanical interference.

#### 3. Take Image and Get Gemini to Output Degree Measurements

- Capture an image using a camera module (e.g., OpenCV).
  - Process the image to extract relevant features (if needed).
- Send the image to Gemini for degree predictions for each servo.
  - Parse Gemini's output to get the target angles for all six axes.
- Call `move_arm` with the predicted angles to position the robotic arm.

#### Integration Notes

- Use `genai.GenerativeModel` with functions:
  - `move_servo_n` for individual control.
  - `move_arm` for coordinated movements.
- Add a `capture_and_move` function:
  - Capture an image.
  - Get Gemini's output for target angles.
  - Call `move_arm` with the predicted angles.

#### Error Handling

- Validate all inputs from Gemini (ensure angles are between 0-180).
- Implement fallback states to reset the arm to a neutral position if any servo fails.
- Log all operations for troubleshooting.
