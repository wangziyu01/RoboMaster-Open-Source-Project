"""
CopyRight(C) 2022 wangziyu01 and wangziyu0305 All Rights Reserved.
版权所有(C) 2022 wangziyu01 和 wangziyu0305 保留所有权利
Version:1.4.7 release
Modify Log:
2021/12/04 Create
2021/12/04 Fixed several bugs
2021/12/04 Add time control
2021/12/11 Change the time control logic
2021/12/11 Add turn to angle Function
2021/12/18 Add Turn to original direction Function
2021/12/18 Add Variable Range List
2022/3/13 Change copyright information
2022/3/13 Fixed several bugs
2022/3/13 Fixed several bugs
2022/8/7  Fixed several bugs Change the function name "moveTime" to "move_with_time"
2022/9/3  Fixed an issue that could cause the program to terminate abnormally
Function list:
move(s,v,angle)
moveTime(t,v,angle)
turnToAngle(v,target_angle)
turn_to_initial(v)
variable range list:
v:-600~600
s:0~infinity
angle:-180~180
target_angle:-180~180
"""

variable_X = 0
variable_Y = 0
variable_s = 0
variable_x0 = 0
variable_y0 = 0


def start():
    move_with_time(1, 1, -90)
    # turn_to_angle(300, -90)
    # turn_to_initial(300)
    # move(1, 1.5,0)
    # Please call the function here(move/moveTime/turnToAngle/turn_to_initial)
    # 请在此处调用函数（move/move_with_time/turnToAngle/turn_to_initial)


def move(s, v, angle) -> None:
    """
    :param s: 移动距离 单位：米(m)
    :param v: 移动速度 单位：m/s
    :param angle: 角度 单位：度（°）
    """
    # global variable_X
    # global variable_Y
    # global variable_s
    # global variable_x0
    # global variable_y0
    robot_ctrl.set_mode(rm_define.robot_mode_chassis_follow)
    variable_X = 0
    variable_Y = 0
    variable_s = 0
    variable_x0 = chassis_ctrl.get_position_based_power_on(rm_define.chassis_forward)
    variable_y0 = chassis_ctrl.get_position_based_power_on(rm_define.chassis_translation)
    while variable_s <= s:
        variable_X = chassis_ctrl.get_position_based_power_on(rm_define.chassis_forward)
        variable_Y = chassis_ctrl.get_position_based_power_on(rm_define.chassis_translation)
        variable_s = math.sqrt((variable_X - variable_x0) * (variable_X - variable_x0) + (variable_Y - variable_y0) * (
                    variable_Y - variable_y0))
        chassis_ctrl.move_degree_with_speed(v, angle)
    chassis_ctrl.move_with_speed(0, 0, 0)


def move_with_time(v, t, angle):
    """

    :rtype: none 无返回值
    :param v: 速度 单位：m/s
    :param t: 运动时间 单位：秒(s)
    :param angle: 角度 单位：度（°）
    """
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    chassis_ctrl.move_degree_with_speed(v, angle)
    chassis_ctrl.set_rotate_speed(v)
    w1 = w4 = (v*math.cos(angle) + v*math.sin(angle)) / 0.05075 *94.2
    w2 = w3 = (v*math.cos(angle) - v*math.sin(angle)) / 0.05075 *94.2
    print(str(w1) + " "+ str(w2) + ' ' + str(w3) + ' ' + str(w4))
    chassis_ctrl.set_wheel_speed(w1,w2,w3,w4)
    time.sleep(t)
    chassis_ctrl.move_with_speed(0, 0, 0)
    



def turn_to_angle(v, target_angle):
    chassis_ctrl.set_rotate_speed(v)
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    error = target_angle - chassis_ctrl.get_position_based_power_on(rm_define.chassis_rotate)
    if error > 0:
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, error)
    else:
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, abs(error))

    chassis_ctrl.move_with_speed(0, 0, 0)


def turn_to_initial(v: int):
    """

    :param v:速度 单位：m/s
    :return: None
    """
    variable_target_angle = 0
    chassis_ctrl.set_rotate_speed(v)
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    error = variable_target_angle - chassis_ctrl.get_attitude(rm_define.chassis_yaw)
    if error > 0:
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, error)
    else:
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, abs(error))

    chassis_ctrl.move_with_speed(0, 0, 0)
