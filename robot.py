#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
import socket
import json
import time
import math

left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_B)
claw_motor = MediumMotor(OUTPUT_C)
robot = MoveTank(OUTPUT_A, OUTPUT_B)

# Constants
DISTANCE_THRESHOLD = 50  # Distance threshold to stop moving (adjusted for better accuracy)
FIRST_BALL_POSITION = None  # Store the first detected ball position
KP = 0.5  # Proportional gain for angle adjustment

def calculate_distance(ball_position, robot_position):
    bx, by = ball_position
    rx, ry = robot_position
    return math.sqrt((bx - rx)**2 + (by - ry)**2)

def calculate_angle(ball_position, robot_position):
    bx, by = ball_position
    rx, ry = robot_position
    return math.atan2(by - ry, bx - rx)

def move_towards_ball(ball_position, robot_position):
    angle = calculate_angle(ball_position, robot_position)
    angle_degrees = math.degrees(angle)
    
    # Proportional control for smoother turning
    correction = KP * angle_degrees
    left_speed = 50 - correction
    right_speed = 50 + correction
    
    # Ensure the speed is within the valid range
    left_speed = max(min(left_speed, 100), -100)
    right_speed = max(min(right_speed, 100), -100)
    
    robot.on(SpeedPercent(left_speed), SpeedPercent(right_speed))

def stop_robot():
    robot.off()

def pick_up_ball():
    claw_motor.on_for_seconds(SpeedPercent(75), 3)  # Increase the speed and time to ensure a tight grip

def main():
    global FIRST_BALL_POSITION  # Use the global variable to store the first ball position
    server_ip = '172.20.10.6'  # Replace with the actual server IP
    server_port = 9090

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_ip, server_port))

        while True:
            sock.sendall(b'request_ball_position')
            data = sock.recv(1024)
            if not data:
                break

            response = json.loads(data.decode())
            ball_position = response.get("ball_position")
            robot_position = response.get("robot_position")

            if FIRST_BALL_POSITION is None and ball_position:
                FIRST_BALL_POSITION = ball_position  # Store the first detected ball position

            if FIRST_BALL_POSITION and robot_position:
                distance = calculate_distance(FIRST_BALL_POSITION, robot_position)
                print("First Ball position: {}".format(FIRST_BALL_POSITION))  # Print the coordinates of the ball
                print("Robot position: {}".format(robot_position))  # Print the coordinates of the robot
                print("Distance to ball: {}".format(distance))
                if distance > DISTANCE_THRESHOLD:
                    move_towards_ball(FIRST_BALL_POSITION, robot_position)
                else:
                    stop_robot()
                    pick_up_ball()
                    print("Reached the ball and picked it up!")
                    break  # Stop the loop once the ball is reached and picked up
            else:
                stop_robot()

            time.sleep(0.1)

if __name__ == "__main__":
    main()
