#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent
from time import sleep

# Initialize motors
left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_B)
claw_motor = MediumMotor(OUTPUT_C)

def pick_up_ball():
    claw_motor.on_for_seconds(SpeedPercent(-100), 2)  # Adjust time to ensure the claw grips the ball

def initialize_claw():
    print("Initializing claw")
    claw_motor.on_for_seconds(SpeedPercent(50), 3)  # Open the claw to a known position

def test_motor(motor, output_port):
    print("Testing motor on port {}".format(output_port))
    motor.on_for_seconds(SpeedPercent(-75), 3)
    motor.off()
    sleep(1)

if __name__ == "__main__":
    # test_motor(right_motor, "B")
    # test_motor(left_motor, "A")
    initialize_claw()
    pick_up_ball()
    
