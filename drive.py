#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sound import Sound
from time import sleep
from flask import Flask, request, jsonify

app = Flask(__name__)

left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_B)
claw_motor = MediumMotor(OUTPUT_C)
robot = MoveTank(OUTPUT_A, OUTPUT_B)
sound = Sound()

# Constants
FRAME_WIDTH = 640  # Adjust according to your webcam resolution
CENTER_THRESHOLD = 20  # Pixels to consider the ball as centered

def move_towards_ball(ball_position):
    x, y = ball_position
    frame_center_x = FRAME_WIDTH // 2
    
    if abs(x - frame_center_x) > CENTER_THRESHOLD:
        if x < frame_center_x:
            robot.on(SpeedPercent(30), SpeedPercent(50))  # Turn left
        else:
            robot.on(SpeedPercent(50), SpeedPercent(30))  # Turn right
    else:
        robot.on(SpeedPercent(50), SpeedPercent(50))  # Move forward

def stop_robot():
    robot.off()

@app.route('/update', methods=['POST'])
def update_status():
    data = request.json
    if 'ball_position' in data:
        move_towards_ball(data['ball_position'])
    else:
        stop_robot()
    return jsonify({"status": "received"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
