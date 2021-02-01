"""PR14. Robot."""

from PiBot import PiBot

robot = PiBot()
right_colour = robot.get_third_line_sensor_from_right()
left_colour = robot.get_third_line_sensor_from_left()
robot.set_wheels_speed(50)
# robot will travel until sensors see the line.
while left_colour > 200 and right_colour > 200:
    right_colour = robot.get_third_line_sensor_from_right()
    left_colour = robot.get_third_line_sensor_from_left()
    robot.sleep(0.05)

# when he saw the line, for loop to make robot move 5 'seconds' more.
for second in range(5):
    robot.set_wheels_speed(100)
    robot.sleep(0.05)
robot.set_wheels_speed(0)
robot.done()
