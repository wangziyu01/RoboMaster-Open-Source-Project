'''
CopyRight(C) 2022 wangziyu01 All Rights Reserved.

Versition:1.3.7

Modify Log:
2021/12/04 Create
2021/12/04 Fixed several bugs
2021/12/04 Add time control
2021/12/11 Change the time control logic
2021/12/11 Add turn to angle Funtion
2021/12/18 Add Turn to original direction Funtion
2021/12/18 Add Variable Range List
2022/3/13 Change copyright information
2022/3/13 Fixed several bugs
2022/3/13 Fixed several bugs
2022/8/5  Fixed several bugs Changed the name of the "moveTime" function

Funtion list:
move(s,v,angle)
moveTime(t,v,angle)
turnToAngle(v,targetAngle)
turnToInitial(v)

variable range list:
v:-600~600
s:0~infinity
angle:-180~180
targetAngle:-180~180
'''

variable_X = 0
variable_Y = 0
variable_s = 0
variable_x0 = 0
variable_y0 = 0


def start():
    #Please call the function here(move/moveTime/turnToAngle/turnToInitial)
    #请在此处调用函数（move/moveWithTime/turnToAngle/turnToInitial)

def move(s,v,angle):
    global variable_X
    global variable_Y
    global variable_s
    global variable_x0
    global variable_y0
    robot_ctrl.set_mode(rm_define.robot_mode_chassis_follow)
    variable_X = 0
    variable_Y = 0
    variable_s = 0
    variable_x0 = chassis_ctrl.get_position_based_power_on(rm_define.chassis_forward)
    variable_y0 = chassis_ctrl.get_position_based_power_on(rm_define.chassis_translation)
    while variable_s <= s:
        variable_X = chassis_ctrl.get_position_based_power_on(rm_define.chassis_forward)
        variable_Y = chassis_ctrl.get_position_based_power_on(rm_define.chassis_translation)
        variable_s = math.sqrt((variable_X-variable_x0) * (variable_X-variable_x0) + (variable_Y-variable_y0) * (variable_Y-variable_y0))
        chassis_ctrl.move_degree_with_speed(v,angle)
    chassis_ctrl.move_with_speed(0,0,0)

def moveWithTime(v, t, angle):
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    chassis_ctrl.move_degree_with_speed(v,angle)
    time.sleep(t)
    chassis_ctrl.move_with_speed(0,0,0)

def turnToAngle(v,targetAngle):
    chassis_ctrl.set_rotate_speed(v)
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    error = targetAngle-chassis_ctrl.get_position_based_power_on(rm_define.chassis_rotate)
    if(error>0):
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, error)
    else:
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, error)

    chassis_ctrl.move_with_speed(0,0,0)

def turnToInitial(v):
    variable_targetAngle = 0
    chassis_ctrl.set_rotate_speed(v)
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    error = variable_targetAngle - chassis_ctrl.get_attitude(rm_define.chassis_yaw)
    if(error>0):
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, error)
    else:
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, abs(error))

    chassis_ctrl.move_with_speed(0,0,0)
