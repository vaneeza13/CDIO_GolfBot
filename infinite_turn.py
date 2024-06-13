#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.motor import MediumMotor, OUTPUT_C  # Assuming claw motor is a medium motor, change to LargeMotor if necessary
from time import sleep

# Initialize the motors
left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_B)
claw_motor = MediumMotor(OUTPUT_C)

def open_claw():
    claw_motor.on_for_seconds(SpeedPercent(50), 1)  # Open claw for 1 second

def close_claw():
    claw_motor.on_for_seconds(SpeedPercent(-50), 1)  # Close claw for 1 second

try:
    # Start an infinite loop to make the robot turn around and operate the claw
    while True:
        # Set the left motor to move forward and the right motor to move backward
        # left_motor.on(SpeedPercent(50))  # 50% speed forward
        # right_motor.on(SpeedPercent(-50))  # 50% speed backward
        
        # Open and close the claw periodically
        open_claw()
        sleep(1)  # Wait for 1 second
        close_claw()
        sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    # Stop the motors when a KeyboardInterrupt (Ctrl+C) is received
    left_motor.off()
    right_motor.off()
    claw_motor.off()
    print("Robot stopped.")
