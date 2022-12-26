"""
RMYC2022 小学组 蓝方自动程序
Bug:能量机关Pitch轴有时混乱
"""
list_maker_list = RmList()
list_number_list = RmList()
list_shoot_list = RmList()
list_line_list = RmList()
list_j = RmList()
list_k = RmList()
variable_i = 0
variable_op = 0
variable_x = 0
variable_y = 0
variable_error_x = 0
variable_turn_angle_x = 0
variable_turn_angle_y = 0
variable_ID = 0
variable_error = 0
def user_defined_atk():
    global variable_i
    global variable_op
    global variable_x
    global variable_y
    global variable_error_x
    global variable_turn_angle_x
    global variable_turn_angle_y
    global variable_ID
    global variable_error
    global list_maker_list
    global list_number_list
    global list_shoot_list
    global list_line_list
    global list_j
    global list_k
    if variable_op == 43:
        user_defined_chengfa()
    else:
        user_defined_chufa()

    variable_i = 1
    for count in range(int(len(list_shoot_list))):
        variable_ID = list_shoot_list[variable_i]
        user_defined_shoot_ID()

        variable_i = variable_i + 1
def user_defined_move3():
    global variable_i
    global variable_op
    global variable_x
    global variable_y
    global variable_error_x
    global variable_turn_angle_x
    global variable_turn_angle_y
    global variable_ID
    global variable_error
    global list_maker_list
    global list_number_list
    global list_shoot_list
    global list_line_list
    global list_j
    global list_k
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    chassis_ctrl.set_rotate_speed(200)
    chassis_ctrl.set_trans_speed(2.5)
    chassis_ctrl.set_wheel_speed(200,200,200,200)
    time.sleep(2)
    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise,90)
def user_defined_int():
    global variable_i
    global variable_op
    global variable_x
    global variable_y
    global variable_error_x
    global variable_turn_angle_x
    global variable_turn_angle_y
    global variable_ID
    global variable_error
    global list_maker_list
    global list_number_list
    global list_shoot_list
    global list_line_list
    global list_j
    global list_k
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    list_maker_list.clear()
    list_number_list.clear()
    list_shoot_list.clear()
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    vision_ctrl.marker_detection_color_set(rm_define.marker_detection_color_blue)
    vision_ctrl.set_marker_detection_distance(3)
def user_defined_atk2():
    global variable_i
    global variable_op
    global variable_x
    global variable_y
    global variable_error_x
    global variable_turn_angle_x
    global variable_turn_angle_y
    global variable_ID
    global variable_error
    global list_maker_list
    global list_number_list
    global list_shoot_list
    global list_line_list
    global list_j
    global list_k
    gimbal_ctrl.yaw_ctrl(0)
    list_maker_list.clear()
    list_number_list.clear()
    list_shoot_list.clear()
    time.sleep(1.01)
    list_maker_list=RmList(vision_ctrl.get_marker_detection_info())
    while not len(list_maker_list) >= 26:
        list_maker_list=RmList(vision_ctrl.get_marker_detection_info())
    while not ((20 in (list_maker_list)) or (39 in (list_maker_list)) or (30 in (list_maker_list))):
        user_defined_get_number_list()

        user_defined_atk()

        gimbal_ctrl.yaw_ctrl(0)
        time.sleep(0.05)
        list_maker_list.clear()
        list_number_list.clear()
        list_shoot_list.clear()
        time.sleep(1)
        list_maker_list=RmList(vision_ctrl.get_marker_detection_info())
        while not len(list_maker_list) >= 16:
            list_maker_list=RmList(vision_ctrl.get_marker_detection_info())
    media_ctrl.play_sound(rm_define.media_sound_recognize_success)
def user_defined_line_alignment():
    global variable_i
    global variable_op
    global variable_x
    global variable_y
    global variable_error_x
    global variable_turn_angle_x
    global variable_turn_angle_y
    global variable_ID
    global variable_error
    global list_maker_list
    global list_number_list
    global list_shoot_list
    global list_line_list
    global list_j
    global list_k
    vision_ctrl.disable_detection(rm_define.vision_detection_marker)
    vision_ctrl.enable_detection(rm_define.vision_detection_line)
    vision_ctrl.line_follow_color_set(rm_define.line_follow_color_blue)
    gimbal_ctrl.pitch_ctrl(-20)
    chassis_ctrl.set_trans_speed(0.1)
    while not len(list_line_list) >= 42:
        list_line_list=RmList(vision_ctrl.get_line_detection_info())
    variable_error = abs(0.5 - list_line_list[15])
    while not variable_error <= 0.03:
        variable_error = abs(0.5 - list_line_list[15])
        list_line_list=RmList(vision_ctrl.get_line_detection_info())
        if 1 - list_line_list[15] <= 0.5:
            chassis_ctrl.move(90)
        else:
            chassis_ctrl.move(-90)
    vision_ctrl.disable_detection(rm_define.vision_detection_line)
def user_defined_shoot_ID():
    global variable_i
    global variable_op
    global variable_x
    global variable_y
    global variable_error_x
    global variable_turn_angle_x
    global variable_turn_angle_y
    global variable_ID
    global variable_error
    global list_maker_list
    global list_number_list
    global list_shoot_list
    global list_line_list
    global list_j
    global list_k
    variable_x = list_maker_list[(list_maker_list.index(variable_ID)) + 1]
    variable_y = list_maker_list[(list_maker_list.index(variable_ID)) + 2]
    variable_error_x = variable_x - 0.5
    variable_turn_angle_x = variable_error_x * 110
    variable_turn_angle_y = (0.5 - variable_y) * 68 - abs(variable_error_x) * 10
    gimbal_ctrl.angle_ctrl(variable_turn_angle_x, variable_turn_angle_y + 19)
    time.sleep(0.08)
    gun_ctrl.fire_once()
    time.sleep(0.08)
    if variable_ID < 25:
        list_maker_list.pop((list_maker_list.index(variable_ID)))
def user_defined_move():
    global variable_i
    global variable_op
    global variable_x
    global variable_y
    global variable_error_x
    global variable_turn_angle_x
    global variable_turn_angle_y
    global variable_ID
    global variable_error
    global list_maker_list
    global list_number_list
    global list_shoot_list
    global list_line_list
    global list_j
    global list_k
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    gimbal_ctrl.set_rotate_speed(180)
    chassis_ctrl.set_trans_speed(2.5)
    chassis_ctrl.set_rotate_speed(90)
    chassis_ctrl.move_with_distance(90,0.3)
    vision_ctrl.enable_detection(rm_define.vision_detection_line)
    vision_ctrl.line_follow_color_set(rm_define.line_follow_color_blue)
    chassis_ctrl.move_with_distance(0,1.7)
    chassis_ctrl.rotate_with_degree(rm_define.clockwise,90)
    chassis_ctrl.move_with_distance(0,1)
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    gimbal_ctrl.yaw_ctrl(86)
    gimbal_ctrl.rotate_with_degree(rm_define.gimbal_down,5)
    time.sleep(1)
    gimbal_ctrl.yaw_ctrl(0)
    gimbal_ctrl.rotate_with_degree(rm_define.gimbal_up,5)
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    chassis_ctrl.move_with_distance(-90,0.3)
    chassis_ctrl.move_with_distance(0,0.7)
    chassis_ctrl.move_with_distance(90,0.3)
    robot_ctrl.set_mode(rm_define.robot_mode_free)
def user_defined_chufa():
    global variable_i
    global variable_op
    global variable_x
    global variable_y
    global variable_error_x
    global variable_turn_angle_x
    global variable_turn_angle_y
    global variable_ID
    global variable_error
    global list_maker_list
    global list_number_list
    global list_shoot_list
    global list_line_list
    global list_j
    global list_k
    if (2 in (list_number_list)):
        if (1 in (list_number_list)):
            if (4 in (list_number_list)):
                if (8 in (list_number_list)):
                    list_shoot_list.append(14)
                    list_shoot_list.append(18)
                    list_shoot_list.append(variable_op)
                    list_shoot_list.append(12)
                else:
                    list_shoot_list.append(12)
                    list_shoot_list.append(14)
                    list_shoot_list.append(variable_op)
                    list_shoot_list.append(11)
            else:
                if (5 in (list_number_list)):
                    list_shoot_list.append(11)
                    list_shoot_list.append(12)
                    list_shoot_list.append(10)
                    list_shoot_list.append(variable_op)
                    list_shoot_list.append(15)
                else:
                    if (6 in (list_number_list)):
                        list_shoot_list.append(12)
                        list_shoot_list.append(11)
                        list_shoot_list.append(16)
                        list_shoot_list.append(variable_op)
                        list_shoot_list.append(19)
                    else:
                        if (8 in (list_number_list)):
                            list_shoot_list.append(11)
                            list_shoot_list.append(19)
                            list_shoot_list.append(12)
                            list_shoot_list.append(variable_op)
                            list_shoot_list.append(18)
                        else:
                            if (3 in (list_number_list)):
                                list_shoot_list.append(17)
                                list_shoot_list.append(12)
                                list_shoot_list.append(variable_op)
                                list_shoot_list.append(13)
                            else:
                                list_shoot_list.append(999)
        else:
            if (3 in (list_number_list)):
                if (7 in (list_number_list)):
                    list_shoot_list.append(17)
                    list_shoot_list.append(12)
                    list_shoot_list.append(variable_op)
                    list_shoot_list.append(13)
                else:
                    if (8 in (list_number_list)):
                        list_shoot_list.append(14)
                        list_shoot_list.append(18)
                        list_shoot_list.append(variable_op)
                        list_shoot_list.append(12)
            else:
                if (4 in (list_number_list)):
                    if (8 in (list_number_list)):
                        list_shoot_list.append(14)
                        list_shoot_list.append(18)
                        list_shoot_list.append(variable_op)
                        list_shoot_list.append(12)
                    else:
                        if (6 in (list_number_list)):
                            list_shoot_list.append(19)
                            list_shoot_list.append(16)
                            list_shoot_list.append(variable_op)
                            list_shoot_list.append(14)
                else:
                    list_shoot_list.append(19)
                    list_shoot_list.append(16)
                    list_shoot_list.append(variable_op)
                    list_shoot_list.append(12)
                    list_shoot_list.append(variable_op)
                    list_shoot_list.append(12)
    else:
        if (6 in (list_number_list)):
            if (4 in (list_number_list)):
                if (9 in (list_number_list)):
                    list_shoot_list.append(19)
                    list_shoot_list.append(16)
                    list_shoot_list.append(variable_op)
                    list_shoot_list.append(4)
                else:
                    if (1 in (list_number_list)):
                        list_shoot_list.append(11)
                        list_shoot_list.append(14)
                        list_shoot_list.append(14)
                        list_shoot_list.append(variable_op)
                        list_shoot_list.append(16)
            else:
                list_shoot_list.append(11)
                list_shoot_list.append(16)
                list_shoot_list.append(18)
                list_shoot_list.append(variable_op)
                list_shoot_list.append(17)
def user_defined_move2():
    global variable_i
    global variable_op
    global variable_x
    global variable_y
    global variable_error_x
    global variable_turn_angle_x
    global variable_turn_angle_y
    global variable_ID
    global variable_error
    global list_maker_list
    global list_number_list
    global list_shoot_list
    global list_line_list
    global list_j
    global list_k
    chassis_ctrl.set_trans_speed(1)
    chassis_ctrl.move_with_distance(-90,1.2)
    chassis_ctrl.set_wheel_speed(-100,100,100,-100)
    time.sleep(1)
    chassis_ctrl.stop()
    time.sleep(0.07)
    chassis_ctrl.move_with_distance(0,1.2)
    chassis_ctrl.stop()
    time.sleep(0.07)
    chassis_ctrl.set_wheel_speed(-100,100,100,-100)
    time.sleep(1)
    chassis_ctrl.stop()
    time.sleep(0.07)
    chassis_ctrl.move_with_distance(90,0.6)
    chassis_ctrl.move_with_distance(0,1)
def user_defined_chengfa():
    global variable_i
    global variable_op
    global variable_x
    global variable_y
    global variable_error_x
    global variable_turn_angle_x
    global variable_turn_angle_y
    global variable_ID
    global variable_error
    global list_maker_list
    global list_number_list
    global list_shoot_list
    global list_line_list
    global list_j
    global list_k
    if (8 in (list_number_list)):
        if (3 in (list_number_list)):
            list_shoot_list.append(13)
            list_shoot_list.append(variable_op)
            list_shoot_list.append(18)
    else:
        if (6 in (list_number_list)):
            if (4 in (list_number_list)):
                list_shoot_list.append(14)
                list_shoot_list.append(variable_op)
                list_shoot_list.append(16)
            else:
                if (2 in (list_number_list)):
                    if (1 in (list_number_list)):
                        list_shoot_list.append(12)
                        list_shoot_list.append(variable_op)
                        list_shoot_list.append(11)
                        list_shoot_list.append(12)
                    else:
                        list_shoot_list.append(12)
                        list_shoot_list.append(variable_op)
                        list_shoot_list.append(12)
                        list_shoot_list.append(variable_op)
                        list_shoot_list.append(16)
                else:
                    pass
        else:
            if (2 in (list_number_list)):
                if (1 in (list_number_list)):
                    if (4 in (list_number_list)):
                        if (3 in (list_number_list)):
                            list_shoot_list.append(12)
                            list_shoot_list.append(variable_op)
                            list_shoot_list.append(13)
                            list_shoot_list.append(variable_op)
                            list_shoot_list.append(14)
                        else:
                            list_shoot_list.append(11)
                            list_shoot_list.append(variable_op)
                            list_shoot_list.append(12)
                            list_shoot_list.append(14)
                    else:
                        list_shoot_list.append(12)
                        list_shoot_list.append(variable_op)
                        list_shoot_list.append(11)
                        list_shoot_list.append(12)
                else:
                    if (3 in (list_number_list)):
                        if (4 in (list_number_list)):
                            list_shoot_list.append(12)
                            list_shoot_list.append(variable_op)
                            list_shoot_list.append(13)
                            list_shoot_list.append(variable_op)
                            list_shoot_list.append(14)
                        else:
                            list_shoot_list.append(12)
                            list_shoot_list.append(variable_op)
                            list_shoot_list.append(12)
                            list_shoot_list.append(variable_op)
                            list_shoot_list.append(12)
                            list_shoot_list.append(variable_op)
                            list_shoot_list.append(13)
def user_defined_get_number_list():
    global variable_i
    global variable_op
    global variable_x
    global variable_y
    global variable_error_x
    global variable_turn_angle_x
    global variable_turn_angle_y
    global variable_ID
    global variable_error
    global list_maker_list
    global list_number_list
    global list_shoot_list
    global list_line_list
    global list_j
    global list_k
    gimbal_ctrl.set_rotate_speed(200)
    gimbal_ctrl.pitch_ctrl(15)
    time.sleep(0.3)
    list_number_list.clear()
    list_maker_list=RmList(vision_ctrl.get_marker_detection_info())
    while not len(list_maker_list) >= 26:
        list_maker_list=RmList(vision_ctrl.get_marker_detection_info())
    media_ctrl.play_sound(rm_define.media_sound_scanning)
    variable_i = 2
    for count in range(5):
        if list_maker_list[variable_i] < 20:
            list_number_list.append(list_maker_list[variable_i] - 10)
        else:
            variable_op = list_maker_list[variable_i]
        variable_i = variable_i + 5
def start():
    global variable_i
    global variable_op
    global variable_x
    global variable_y
    global variable_error_x
    global variable_turn_angle_x
    global variable_turn_angle_y
    global variable_ID
    global variable_error
    global list_maker_list
    global list_number_list
    global list_shoot_list
    global list_line_list
    global list_j
    global list_k
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    gimbal_ctrl.recenter()
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    user_defined_move()

    user_defined_int()

    user_defined_get_number_list()

    user_defined_atk()

    user_defined_atk2()

    gimbal_ctrl.yaw_ctrl(0)
    time.sleep(1)
    user_defined_move2()

    user_defined_move3()

    chassis_ctrl.move_with_distance(180,0.5)
