# RMYC2022, 步兵(红、蓝阵营设置)第一分钟自动程序, By Bruce_冷, Gavin向,wangziyu0305
"""
#******  运行逻辑流程 ******#
#0 摆放位置：基地启动区，靠短场地边，面向基地护甲、前端平齐地垫接缝中缝(1/2中线)(后端平齐黄线)
#1 从基地出发，达到L形状地块(给2s扫描"S"护甲标签)
#2 L地块，激活能量机关（ATK）
#3 上公路，射击敌方基地

# 更新记录
v1.0 :L形地块激活，两倍镜，上公路，打基地    -2022年3月31日
v1.1 :加入一些靠墙定位    -2022年4月10日
v1.2 :巡线上公路，及冗余优化    -2022年4月23日
     :-利用Debug程序,ATK去除打"1"的Bug？
v1.3 :加入“bei_shu”、“color”全局变量 -2022年5月7日
(Vx   :红蓝合一、)

# Bug
Bugs: 蓝方会出现有时ATK,Pitch轴角度胡乱的问题，改成固定上抬角度 -2022年5月8日

"""

import time

# 声明各全局变量(传递数据给函数使用，在该函数中得加入"global")
color = "red"  # 设定己方阵营(颜色) "red"/"blue"
bei_shu = 2 # 相机放大倍数可调,用于"ATK"\"Base"   （2倍似乎通用：高墙、L形地块都行）
variable_pitch_0 = 0    # 记录识别到26项数据时，云台的俯仰角度
fuhao = 0   # 运算符号（计算过程中会 -10 ）
Marker_list = RmList()  # 只有这个为Rm列表，第一项的索引index为 1（其余的列表都为常规列表）
pid_PID_line = PIDCtrl() # 创建巡线PID(模块)

"""**********               主函数,程序从这里开始运行(EP行动)               **********"""
def start():
    # 主函数里，不要写多行文本注释
    # robot_ctrl.set_mode(rm_define.robot_mode_free) # 自由模式
    # vision_ctrl.disable_detection(rm_define.vision_detection_marker) # 关闭标签识别

    # # test
    # line_follow_time(5.5)
    # time.sleep(4)

    # 计算用时
    t0 = time.perf_counter()

    initial_S() # 初始设定，识别“S”的颜色
    # # 步兵移动到L形地块    
    run_angle(-132, 1.5, 1.65) # 1.52
    run_time_pro(-90, 80, 1) # 靠墙（L）
    run_time_pro(90, 80, 0.20) # 从（L地块）移出来
    gimbal_ctrl.set_rotate_speed(200)
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    gimbal_ctrl.angle_ctrl(0, -20) # 扫“S”
    time.sleep(2)

    # 准备激活，对准ATK(能量机关)
    turn_to_angle_P(-94) # -94°

    initial_ATK() # ATK初始化设定(激活颜色……等)
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    gimbal_ctrl.recenter() # 云台回中（消除机器人旋转带来的误差）
    # media_ctrl.play_sound(rm_define.media_sound_count_down,wait_for_complete=True)
    time.sleep(0.2) # 给一定的回中的时间
    untill_all_Marker_2() # 直到扫描到所有5个标签    

    shoot_once() # 射击一轮
    until_ATK() # 直到成功-ATK
    # ATK over
    vision_ctrl.disable_detection(rm_define.vision_detection_marker) # 关闭标签识别,为线识别准备
    media_ctrl.play_sound(rm_define.media_sound_recognize_success)  # 提示音
    gimbal_ctrl.set_rotate_speed(210)
    gimbal_ctrl.angle_ctrl(0, 0)
    print("******My EP, Well done! ******")  #  激活成功之后，提示符
    print("******Good Good Studying, Day Day Up! ******")  #  "好好学习，天天向上"，提示符

    #  上公路的两种方案，建议巡线上公路
    # 上公路-第一种（存移动）
    # turn_to_angle_P(-180)
    # run_angle(0, 1.5, 2.35) #2.22
    # media_ctrl.play_sound(rm_define.media_sound_scanning)
    # # turn_to_angle(-90)
    # turn_to_angle_P(-90)
    # run_time_pro(-90, 80, 1.2)
    # run_time_pro(90, 80, 0.2)
    # media_ctrl.play_sound(rm_define.media_sound_scanning)
    # run_angle(0, 1.5, 3.02)

    # 上公路-第二种（巡线，解决起伏路的问题）
    turn_to_angle_P(-180)
    robot_ctrl.set_mode(rm_define.robot_mode_free) 
    gimbal_ctrl.angle_ctrl(0, -20) # 低头看公路
    time.sleep(0.5) # 等待0.5s（冗余设计，操作手看是否会翻车）
    # run_angle(0, 0.9, 0.3) # 前进0.3m
    chassis_ctrl.move_degree_with_speed(0.8,0) # 前进一小段
    time.sleep(0.5)
    line_follow_time(6.9) # 巡线6.8s(速度、PID参数改的话在函数里去找)

    # 在公路上射击基地（靠边，后退留出射击位置）
    run_angle(-45, 0.5, 0.3) # 左前45度，进0.3m
    run_time_pro(0, 60, 0.6) # 前0度，进0.6s
    run_time_pro(-90, 80, 1.0)
    run_time_pro(180, 150, 0.7) # 后撤一段时间(距离)

    # 查看用时
    t = time.perf_counter() - t0
    print("How many time = ", t, "s")

    # 瞄准基地射击
    gimbal_ctrl.recenter() # 云台回中（消除机器人旋转带来的误差）
    time.sleep(0.2) # 给一定的(够)回中的时间
    bei_shu = 2
    initial_BASE()
    untill_BASE_Marker()
    shoot_BASE()

    # 最后转向资源岛
    run_time_pro(90, 80, 0.2)
    turn_to_angle_P(10) # 10度
    # ***自动程序运行到此结束***


"""**********               自定义函数               **********"""
# 初始设定，开启标签识别，识别“S”的颜色设置
def initial_S():
    global color
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)  # 开启标签识别
    vision_ctrl.set_marker_detection_distance(3)  # 设定可识别距离
    if color == "blue": # 设置识别的颜色
        vision_ctrl.marker_detection_color_set(rm_define.marker_detection_color_blue)  # 设定标签颜色为 蓝
        print("marker_detection = blue")
    else:
        vision_ctrl.marker_detection_color_set(rm_define.marker_detection_color_red)  # 设定标签颜色（默认红色）

# 进行ATK的初始化设置（第一分钟自动）
def initial_ATK():
    global bei_shu
    global color
    robot_ctrl.set_mode(rm_define.robot_mode_free)  # 设定“自由模式”
    media_ctrl.zoom_value_update(bei_shu)  # 设定相机放大倍数
    # media_ctrl.exposure_value_update(rm_define.exposure_value_large)   # 设定相机曝光值, [环境暗 对应 曝光值小] (small、medium、large)
    # media_ctrl.exposure_value_update(rm_define.exposure_value_medium)   # 设定相机曝光值（室内使用？）
    # media_ctrl.exposure_value_update(rm_define.exposure_value_medium)   # 设定相机曝光值（很暗的环境）
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)  # 开启标签识别
    vision_ctrl.set_marker_detection_distance(3)  # 设定可识别距离
    if color == "blue": # 设置识别的颜色
        vision_ctrl.marker_detection_color_set(rm_define.marker_detection_color_blue)  # 设定标签颜色为 蓝
        print("marker_detection = blue")
    else:
        vision_ctrl.marker_detection_color_set(rm_define.marker_detection_color_red)  # 设定标签颜色（默认红色）
    gun_ctrl.set_fire_count(1)  # 水弹1发/次    
    # variable_pitch_adjust = 1  ##（想用于自动计算云台俯仰角，根据距离不同自动计算）暂时未做好

# 扫描标签直到识别到 >26个及以上的列表项目数
# 全局变量：【variable_pitch_0】扫描成功时，云台的俯仰角；【Marker_list】标签列表
def untill_all_Marker_2():
    # 固定上抬角度，想解决移动过程中，识别到问题。上、下胡乱打的Bug —2022年5月8日
    global variable_pitch_0     # 需要在函数里使用全局变量，就得也声明。否则变为局部（报错）
    global Marker_list
    gimbal_ctrl.set_rotate_speed(150)   # 云台初始速度（第一分钟自动）
    gimbal_ctrl.angle_ctrl(0, 10)    # 云台抬高6°(定位云台扫描标签的初始视角（可修改）)
    Marker_list=RmList(vision_ctrl.get_marker_detection_info())    # 更新列表
    time.sleep(0.3) # 短暂延时，为了准确识别标签
    gimbal_ctrl.set_rotate_speed(30)    #上抬扫描速度（快一点应该也可行）
    while not len(Marker_list) >= 26:
        # gimbal_ctrl.rotate_with_degree(rm_define.gimbal_up,1)   # 循环每运行一次，上抬1°（学习澳门一队伍的方法）
        # if gimbal_ctrl.get_axis_angle(rm_define.gimbal_axis_pitch) >= 18.5:   # 上抬最大角度（可修改）
        #     gimbal_ctrl.set_rotate_speed(80)    # 回位速度
        #     gimbal_ctrl.pitch_ctrl(6)    # 回到初始视角
        #     gimbal_ctrl.set_rotate_speed(30)    # 扫描速度
        time.sleep(0.2)    # 每上抬一次，添加短暂延时，为了准确识别标签
        Marker_list=RmList(vision_ctrl.get_marker_detection_info())    # 更新列表
        print("Marker s = ", Marker_list[1]) # ——Debug——查看标签的数量
    gimbal_ctrl.stop()
    # Marker_list=RmList(vision_ctrl.get_marker_detection_info())    # 再次更新列表(Debug,俯仰角错乱的问题,2022年5月8日)
    time.sleep(0.1) # 短暂延时，为了准确
    variable_pitch_0 = gimbal_ctrl.get_axis_angle(rm_define.gimbal_axis_pitch)  # 获取当前俯仰轴角度，为射击准备
    print("pitch_shibie", variable_pitch_0)
    # print("Marker_list = ", Marker_list) # ——Debug——查看扫描到的标签列表
    media_ctrl.play_sound(rm_define.media_sound_recognize_success) # 扫描完毕的提示音
    gimbal_ctrl.set_rotate_speed(240)   # 设定射击时的旋转速度（可修改）
    
# 从MarkerL_list列表中，获取ID并依次加入到列表末尾，最后返回该列表
def get_ID(arr):
    ID_list = []
    index = 2  # 从Marker_list(RmList)的第二项依次开始取ID
    for count in range(5):
        ID_list.append(arr[index])
        index = index + 5
    return ID_list  # 返回列表数据

# 从ID_list中分出运算符号及数字（全部进行 -10 操作），最后返回该符号及列表数据
# 全局变量：【fuhao】
def get_numbers(arr):
    global fuhao    # 全局变量
    number_list = []
    for i in arr:
        i = i - 10  # -10操作
        if (i > 10):
            fuhao = i   # fuhao 也进行了 “-10”
        else:
            number_list.append(i)   # 比如：ID12 > 2（阿拉伯数字）
    return number_list  # 返回列表数据

#先判断为加减乘除的哪一个，再把所有的排列拿过来，依次进行对应的运算（加减乘除）
def do_24(nums): # [nums] 为排列之后的，二维数组，如：[[1,5,6,9],[1,5,9,6],...]
    shoot_list = []
    if fuhao == 40: # +加法，原ID:50
        for item in nums:   # 遍历排列，依次计算
            shoot_list = jia_fa(item)   # 调用计算函数，并返回计算结果
            if len(shoot_list) != 0: # 结果列表不为空，表示算出24点
                break
    elif fuhao == 41:   # -减法，原ID:51
        for item in nums:
            shoot_list = jian_fa(item)
            if len(shoot_list) != 0:
                break
    elif fuhao == 33:   # *乘法，原ID:43
        for item in nums:
            shoot_list = cheng_fa(item)
            if len(shoot_list) != 0:
                break
    elif fuhao == 42:   # /除法，原ID:52
        for item in nums:
            shoot_list = chu_fa(item)
            if len(shoot_list) != 0:
                break
    # 计算完，返回射击顺序列表（所有ID已经 -10）
    return shoot_list

"""加法"""
def jia_fa(item):
    # A+B+C / A+B+C+D / AB+C / AB+C+D / AB+CD
    # 每次调用函数时，先清空列表
    shoot_list = []
    # AB+C
    result = item[0]*10 + item[1] + item[2]
    if result == 24:
        shoot_list = [item[0], item[1], 40, item[2]]
    else:
        # AB+CD
        result = (item[0]*10 + item[1]) + (item[2]*10 + item[3])
        if result == 24:
            shoot_list = [item[0], item[1], 40, item[2], item[3]]
        else:
            # AB+C+D
            result = (item[0]*10 + item[1]) + item[2] + item[3]
            if result == 24:
                # 去除, 加数为0的相关元素
                if item[2] == 0:
                    shoot_list = [item[0], item[1], 40, item[3]]
                elif item[3] == 0:
                    shoot_list = [item[0], item[1], 40, item[2]]
                else:
                    shoot_list = [item[0], item[1], 40, item[2], 40, item[3]]
            else:
                # A+B+C    
                result = item[0] + item[1] + item[2] 
                if result == 24:
                    shoot_list = [item[0], 40, item[1], 40, item[2]]
                else:
                    # A+B+C+D
                    result = item[0] + item[1] + item[2] + item[3]        
                    if result == 24:
                        # 去除, 加数为0的相关元素
                        if item[1] == 0:
                            shoot_list = [item[0], 40, item[2], 40, item[3]]
                        elif item[2] == 0:
                            shoot_list = [item[0], 40, item[1], 40, item[3]]
                        elif item[3] == 0:
                            shoot_list = [item[0], 40, item[1], 40, item[2]]
                        else:
                            shoot_list = [item[0], 40, item[1], 40, item[2], 40, item[3]]            
                    else:
                        return []
    return shoot_list

"""减法"""
def jian_fa(item):
    # AB-C / AB-C-D / AB-CD
    # 每次调用函数时，先清空列表
    shoot_list = []
    result = item[0]*10 + item[1] - item[2] #AB-C
    if result == 24:
        shoot_list = [item[0], item[1], 41, item[2]]
    else:
        result = item[0]*10 + item[1] - item[2] - item[3] #AB-C-D
        if result == 24:
            #shoot_list = [item[0], item[1], 41, item[2], 41, item[3]]
            # 去除,减数为0的相关元素
            if item[2] == 0:
                shoot_list = [item[0], item[1], 41, item[3]]
            elif item[3] == 0:
                shoot_list = [item[0], item[1], 41, item[2]]
            else:
                shoot_list = [item[0], item[1], 41, item[2], 41, item[3]]
        else:
            result = item[0]*10 + item[1] - item[2]*10 -item[3] #AB-CD
            if result == 24:
                shoot_list = [item[0], item[1], 41, item[2], item[3]]
            else:
                return []
    return shoot_list


"""乘法"""
def cheng_fa(item):
    # A*B / A*B*C / A*B*C*D
    # bug :如果包含多个1，可以不射击（节约两发子弹）？？
    # 每次调用函数时，先清空列表
    shoot_list = []
    result = item[0] * item[1] # A*B
    if (result == 24):
        shoot_list = [item[0], 33, item[1]]
    elif (result < 24):
        result *= item[2] # A*B*C
        if (result == 24):
            shoot_list = [item[0], 33, item[1], 33, item[2]]
        elif (result < 24):
            result *= item[3] # A*B*C*D
            if (result == 24):
                shoot_list = [item[0], 33, item[1], 33, item[2], 33, item[3]]
    if (len(shoot_list) == 0): # 以上没结果
        result = (item[0] * 10 + item[1]) * item[2] # AB*C
        if (result == 24):
            shoot_list = [item[0], item[1], 33, item[2]]
        # 此项应该可以不要
        elif ((result * item[3]) == 24): # AB*C*D   
            shoot_list = [item[0], item[1], 33, item[2], 33, item[3]]
        else:
            return []
    return shoot_list

"""除法"""
def chu_fa(item):
    shoot_list = []
    # bug :如果包含多个1，可以不射击（节约两发子弹）？？
    if (item[2] != 0): # c != 0
        result = (item[0] * 10 + item[1]) / item[2] # AB/C
        if (result == 24):
            shoot_list = [item[0], item[1], 42, item[2]]
        else:
            if (item[3] != 0):
                if ((result / item[3]) == 24): #AB/C/D
                    shoot_list = [item[0],  item[1], 42, item[2], 42, item[3]]
                else:
                    result = (item[0] * 100 + item[1] * 10 + item[2]) / item[3] #ABC/D
                    if (result == 24):
                        shoot_list = [item[0], item[1], item[2], 42, item[3]]
    elif (item[3] != 0):    # [120/5]  第3项为0，并且第4项不为0的情况。
        result = (item[0] * 100 + item[1] * 10 + item[2]) / item[3] #ABC/D
        if (result == 24):
            shoot_list = [item[0], item[1], item[2], 42, item[3]]
    else:
        return []
    return shoot_list


"""**********排列组合的相关函数**********"""
# 定义perm函数实现全排列的一种算法，参考：https://www.cnblogs.com/superhin/p/13052312.html
def perm(arr):
    # 实现全排列
    length = len(arr)   # 获取长度
    if length == 1:  # 递归出口
        return [arr]

    result = []  # 存储结果
    fixed = arr[0]  # 取常规列表arr的第一项(index = 0)
    rest = arr[1:]  # 截取列表的剩余项目(切片)

    for _arr in perm(rest):  # 遍历上层的每一个结果
        for i in range(0, length):  # 插入每一个位置得到新序列
            new_rest = _arr.copy()  # 需要复制一份
            new_rest.insert(i, fixed)   # i:index，插入取出的那一项
            result.append(new_rest)  # 把序列加入到结果中
    return result  # 返回一个二维数组

def make_number_seq(numbers): #排列组合[[[],[],^]
    number_seq = []
    for p_number1 in numbers:
        n1 = numbers.copy() #n1 = numbers[:]
        n1.remove(p_number1) #移出n1列表中的 p_number
        for p_number2 in n1:
            n2 = n1.copy()
            n2.remove(p_number2)
            for p_number3 in n2:
                n3 = n2.copy()
                n3.remove(p_number3)
                seq = [p_number1, p_number2, p_number3, n3[0]]
                number_seq.append(seq)
    return number_seq

"""瞄准及射击的函数"""
def shoot_ID(variable_ID):
    # 控制云台旋转，射击的函数（形式参数：variable_ID）
    # 优化说明：开两倍镜头可用（倍数计算）  - 2022年3月30日
    global variable_pitch_0
    global Marker_list
    global bei_shu
    index_ID = Marker_list.index(variable_ID)   # 记录从列表中找出variblie_ID(形式参数)值第一个匹配项的索引位置
    # print("ID", Marker_list[index_ID])
    x = Marker_list[index_ID + 1]   # 获取该ID标签的x坐标
    y = Marker_list[index_ID + 2]   # 获取该ID标签的y坐标
    error_x = x - 0.5
    turn_angle_x = (error_x * 106)  # 通过比例，计算瞄准的航向角度（相对于yaw=0）
    turn_angle_y = ((0.5 - y) * 68 - abs(error_x) * 4)  # abs()是为了调斜向射击的偏差
    time.sleep(0.06)    # 云台转动到位之后，短暂停顿，保证射击精度    
    # 当开倍镜时，云台角度相应进行换算。
    gimbal_ctrl.angle_ctrl(turn_angle_x / bei_shu, (variable_pitch_0 - 4) + turn_angle_y / bei_shu) # 优化v2.0(倍镜)
    # gimbal_ctrl.angle_ctrl(turn_angle_x, (variable_pitch_0 + 3) + turn_angle_y) # 优化v1.0，加入扫描成功时的俯仰角
    print("pitch =", gimbal_ctrl.get_axis_angle(rm_define.gimbal_axis_pitch)) # 查看当前俯仰轴角度

    gun_ctrl.fire_once()    # 射击一次
    media_ctrl.play_sound(rm_define.media_sound_shoot)  # 提示音
    time.sleep(0.1)    # 射击一发之后停顿，保证射击精度
    time.sleep(0.3)    # 测试用延时，便于观看效果
    
    # 射击一次之后，删除一个射击后的数字标签的对应数据（RMTYC2022）
    if Marker_list[index_ID] == (fuhao + 10):
        pass
    else:
        for count in range(5):
            Marker_list.pop(index_ID)
    # print(Marker_list)    # 检测是否成功删除

# 在获取到5个标签数据之后，执行一次激活
def shoot_once():
    global variable_pitch_0
    global Marker_list

    ID_list = []    # 设为空列表
    num_list = []    # 设为空列表
    ID_list = get_ID(Marker_list)
    num_list = get_numbers(ID_list)
    print("fuhao", fuhao)
    # print("Number_list", num_list)
    # time.sleep(1)

    # 优化，排序处理，为了节省子弹。
    if fuhao == 40:  # 加法优化(从小到大排序),让两位数的加法先于个加法算出来
        num_list.sort(reverse=False) # 永久改变排序，为了避免加法：9+9+5+1的情况（实际：15+9较好-优先级问题）
    else:   # 减法、乘法、除法优化(从大到小),让从大是算起,省子弹
        num_list.sort(reverse=True) # 从大到小排序
    print("shuzi(sort)", num_list)

    shoot_list = do_24(perm(num_list))
    print("ATK:", shoot_list)

    shoot_ID_list = []  # 常规列表，第一项索引index为 0 （需要先定义）
    for i in  shoot_list:
        i = i + 10
        shoot_ID_list.append(i) # 没有先定义列表，就不能进行操作
    
    print("shoot_IDs",shoot_ID_list)    # 查看准备，射击的ID序列

    for ID in shoot_ID_list:
        print(ID)   # 查看每次击打的ID
        shoot_ID(ID)

# 射击一次之后，再次检测，直到激活成功
def until_ATK():
    global variable_pitch_0
    global Marker_list

    media_ctrl.play_sound(rm_define.media_sound_scanning)  # 射击一轮之后的提示音
    Marker_list=RmList()
    time.sleep(1.1)     # 必须等待1s，需要排除 ID = 6（前进箭头）或者 描到ATK（间隔时间太短会误判）

    gimbal_ctrl.set_rotate_speed(250)   # 控制速度
    gimbal_ctrl.yaw_ctrl(0)    # 控制航向轴视野回中间（俯仰轴不变），方便查看是否有"ATK"
    while not len(Marker_list) >= 21:   # 直到包含4个标签
        Marker_list=RmList(vision_ctrl.get_marker_detection_info())
    time.sleep(0.1)
    print("Marker :",Marker_list)  # 打印列表，以查看是否含有 “ATK”

    # 循环，是否出现 “A”或“K”或“T”，否则再次尝试激活
    # while not ((20 in (Marker_list)) or (30 in (Marker_list)) or (39 in (Marker_list))): # 有时 8，会误差识别成 K ？？
    while not ((20 in (Marker_list) and 30 in (Marker_list)) or (30 in (Marker_list) and 39 in (Marker_list)) or (20 in (Marker_list) and 39 in (Marker_list))):
        untill_all_Marker_2()
        shoot_once()   # 再完整激活一次
        media_ctrl.play_sound(rm_define.media_sound_scanning)  # 射击一轮之后的提示音
        Marker_list=RmList()
        time.sleep(1.1)     # 必须等待1s，需要排除 ID = 6（前进箭头）或者 描到ATK（间隔时间太短会误判）
        print("Marker :(again jinru until_ATK)",Marker_list)

        gimbal_ctrl.set_rotate_speed(250)   # 控制速度
        gimbal_ctrl.yaw_ctrl(0)    # 控制航向轴视野回中间（俯仰轴不变）
        while not len(Marker_list) >= 21:   # 直到包含4个标签
            Marker_list=RmList(vision_ctrl.get_marker_detection_info())
        time.sleep(0.1)
        # print("Marker :",Marker_list)
    # # 为了测试
    # media_ctrl.play_sound(rm_define.media_sound_count_down)  # 提示音

"""底盘移动系列函数"""
def run_angle(angle, speed, s):
    #参数说明：(angle:-180~180; speed:0.0~3.5m/s(1.5米合适); s:0.01 ~ $m)
    robot_ctrl.set_mode(rm_define.robot_mode_chassis_follow)#底盘跟随云台
    variable_s_x_0 = chassis_ctrl.get_position_based_power_on(rm_define.chassis_forward)
    variable_s_y_0 = chassis_ctrl.get_position_based_power_on(rm_define.chassis_translation)
    variable_distance = 0
    while not variable_distance >= s:
        chassis_ctrl.move_degree_with_speed(speed, angle)
        #chassis_ctrl.set_trans_speed(speed)
        variable_distance = math.sqrt((chassis_ctrl.get_position_based_power_on(rm_define.chassis_forward) - variable_s_x_0) * (chassis_ctrl.get_position_based_power_on(rm_define.chassis_forward) - variable_s_x_0) + (chassis_ctrl.get_position_based_power_on(rm_define.chassis_translation) - variable_s_y_0) * (chassis_ctrl.get_position_based_power_on(rm_define.chassis_translation) - variable_s_y_0))
    chassis_ctrl.move_with_speed(0,0,0)
    chassis_ctrl.stop()
    # print("run_angle() Done!") # ——Debug——

def run_time(lf_speed, rf_speed, lr_speed, rr_speed, t):
    # 前后左右，4个方向移动靠墙定位，麦轮控制
    # 参数说明：(lf:left_forward(左前), lr:left_rear(左后), speed:-300~300; t:0.01 ~ )
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow) # 云台跟随底盘
    chassis_ctrl.set_wheel_speed(lf_speed, rf_speed, lr_speed, rr_speed)
    time.sleep(t) # t 参数设定（传参）
    chassis_ctrl.move_with_speed(0,0,0) # 刹车
    chassis_ctrl.stop() # 底盘停止
    # print("run_time() Done!") # ——Debug——

def run_time_pro(direction, speed, t):
    # 前后左右，4个方向移动靠墙定位，麦轮控制
    # 参数说明：(direction:[0,90,-90,180], speed建议:-300~300; t:0.01 ~ )
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow) # 云台跟随底盘
    # chassis_ctrl.set_wheel_speed(lf_speed, rf_speed, lr_speed, rr_speed)(lf:left_forward(左前) lr:left_rear(左后))
    if direction == 0:
        chassis_ctrl.set_wheel_speed(speed, speed, speed, speed)
    elif direction == 180:
        chassis_ctrl.set_wheel_speed(-speed, -speed, -speed, -speed)
    elif direction == 90:
        chassis_ctrl.set_wheel_speed(speed, -speed, -speed, speed)
    elif direction == -90:
        chassis_ctrl.set_wheel_speed(-speed, speed, speed, -speed)
    else:
        print("run_time(), Parameter error")
        return 0
    time.sleep(t) # t 参数设定（传参）
    chassis_ctrl.move_with_speed(0,0,0) # 刹车
    chassis_ctrl.stop() # 底盘停止
    # print("run_time_pro() Done!") # ——Debug——

def turn_to_angle(angle_target):
    """转到某个朝向，程序运行瞬间为0°; 参数：angle_target[-180,180]"""
    # Bug:有时到指定角度也会要较长的时间
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow) # 云台跟随
    chassis_ctrl.set_rotate_speed(200) # 设定旋转速率
    variable_direction = chassis_ctrl.get_position_based_power_on(rm_define.chassis_rotate)
    variable_error = angle_target - variable_direction # 参数:目标角度
    if variable_error > 0:
        media_ctrl.play_sound(rm_define.media_sound_solmization_3C)
        chassis_ctrl.rotate_with_degree(rm_define.clockwise,abs(variable_error))
    else:
        media_ctrl.play_sound(rm_define.media_sound_solmization_3B)
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise,abs(variable_error))
    media_ctrl.play_sound(rm_define.media_sound_recognize_success)
    chassis_ctrl.stop()
    # print("turn_to_angle() Done!") # ——Debug——

def turn_to_angle_P(angle):
    # 转向简单P控制(克服内部函数，旋转角度控制的回调太久的问题) - 依旧可以再优化(error大于180时)
    # 底盘转到某个角度，转向P及简单控制;   参数说明：(angle:-178~180)
    # 参数设置时，不要让error角度大于180（比如：当前-90，那转到后方就写-180）
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow) # 云台跟随底盘
    variable_chaoxiang = chassis_ctrl.get_position_based_power_on(rm_define.chassis_rotate)
    variable_error = angle - variable_chaoxiang
    while not abs(variable_error) <= 0.3: # 转向角度精度，偏差值设定
        variable_chaoxiang = chassis_ctrl.get_position_based_power_on(rm_define.chassis_rotate)
        variable_error = angle - variable_chaoxiang
        if abs(variable_error) > 200:
            media_ctrl.play_sound(rm_define.media_sound_solmization_1C) # music
            chassis_ctrl.move_with_speed(0, 0, -0.08 * variable_error) # 比例系数自主设置
        else:
            if abs(variable_error) > 8:
                media_ctrl.play_sound(rm_define.media_sound_solmization_2C) # music
                chassis_ctrl.move_with_speed(0, 0, 3 * variable_error) # 比例系数自主设置
            else:
                if variable_error > 0:
                    chassis_ctrl.move_with_speed(0, 0, 9) # 末端转向速度控制
                else:
                    chassis_ctrl.move_with_speed(0, 0, -9) # 末端转向速度控制
        # print("angle_error", variable_error)
    chassis_ctrl.move_with_speed(0, 0, 0)
    chassis_ctrl.stop()
    # print("Turn_angle Done!") # ——Debug——

def turn_reset():
    """航向归0; 参数：none(转到底盘航向轴角度为0，开机初始角度)"""
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    chassis_ctrl.set_rotate_speed(200) #设定旋转速率
    yaw = chassis_ctrl.get_attitude(rm_define.chassis_yaw) #获取当前的航向轴姿态角
    variable_error = 0 - yaw #计算当前航向与开机初始航向0°的差值，即为需要旋转的航向轴角度
    print("yaw=", yaw)
    if variable_error > 0:
        media_ctrl.play_sound(rm_define.media_sound_solmization_3C)
        chassis_ctrl.rotate_with_degree(rm_define.clockwise,abs(variable_error))
    else:
        media_ctrl.play_sound(rm_define.media_sound_solmization_3B)
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise,abs(variable_error))
    media_ctrl.play_sound(rm_define.media_sound_recognize_success)
    chassis_ctrl.stop()

"""PID巡线函数"""
def line_follow_time(t):
    # 步兵控制云台旋转，巡线时间控制，默认红色    
    global color
    vision_ctrl.disable_detection(rm_define.vision_detection_marker)  # 关闭标签识别
    vision_ctrl.enable_detection(rm_define.vision_detection_line) # 开启线识别
    gun_ctrl.set_fire_count(1)  # 水弹1发/次      
    if color == "blue": # 设置识别的颜色
        vision_ctrl.line_follow_color_set(rm_define.line_follow_color_blue)  # 设定线识别颜色为 蓝
        print("line_detection = blue")
    else:
        vision_ctrl.line_follow_color_set(rm_define.line_follow_color_red) # 设定线识别颜色(默认红色)
    media_ctrl.zoom_value_update(1) # 相机放大倍数
    robot_ctrl.set_mode(rm_define.robot_mode_chassis_follow) # 底盘跟随云台
    gimbal_ctrl.set_rotate_speed(200) # 云台旋转速度
    gimbal_ctrl.angle_ctrl(0, -20) # 低头巡线，-20度
    pid_PID_line.set_ctrl_params(250,0,30) # 【PID】的关键参数
    media_ctrl.play_sound(rm_define.media_sound_scanning) # 提示音(debug用)
    tools.timer_ctrl(rm_define.timer_start) # 开启计时器
    while not tools.timer_current() > t: # 【参数】巡线时间（用计时器控制）
        list_line_list=RmList(vision_ctrl.get_line_detection_info()) # 更新线识别信息
        if len(list_line_list) == 42:
            variable_X5 = list_line_list[19] # 取第5个点的x坐标
            pid_PID_line.set_error(variable_X5 - 0.5)
            gimbal_ctrl.rotate_with_speed(pid_PID_line.get_output(),0) # PID的输出控制云台yaw轴速度
            chassis_ctrl.move_degree_with_speed(0.8,0) # 底盘以0.8m/s的速度，以0°前进(底盘跟随云台)
        else:
            chassis_ctrl.move_degree_with_speed(0.2,0) # 没扫到线时，慢速前进
    chassis_ctrl.stop() # 巡线时间到之后，底盘停止
    tools.timer_ctrl(rm_define.timer_stop) # 关闭计时器
    vision_ctrl.disable_detection(rm_define.vision_detection_line) # 关闭线识别
    gimbal_ctrl.angle_ctrl(0,0) # 云台回0
    media_ctrl.play_sound(rm_define.media_sound_recognize_success) # 提示音(debug用)

"""打基地函数"""
# 射击基地的初始化设置（第一分钟自动）——蓝方基地
def initial_BASE():
    global color
    robot_ctrl.set_mode(rm_define.robot_mode_free)  # 设定“自由模式”
    # media_ctrl.zoom_value_update(1)  # 设定相机放大倍数
    media_ctrl.zoom_value_update(2)  # 设定相机放大倍数
    media_ctrl.exposure_value_update(rm_define.exposure_value_large)   # 设定相机曝光值, [环境暗 对应 曝光值小] (small、medium、large)
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)  # 开启标签识别
    if color == "blue": # 设置识别的颜色
        vision_ctrl.marker_detection_color_set(rm_define.marker_detection_color_red)  # 设定基地标签颜色为 红
        print("[Base] marker_detection = red")
    else:
        vision_ctrl.marker_detection_color_set(rm_define.marker_detection_color_blue)  # 设定基地标签颜色为蓝
    vision_ctrl.set_marker_detection_distance(3)  # 设定可识别距离
    print("[Base] marker_detection = blue")
    gun_ctrl.set_fire_count(1)  # 水弹1发/次

# 全局变量：【variable_pitch_0】扫描成功时，云台的俯仰角；【Marker_list】标签列表
def untill_BASE_Marker():
    global variable_pitch_0     # 需要在函数里使用全局变量，就得也声明。否则变为局部（报错）
    global Marker_list
    gimbal_ctrl.set_rotate_speed(150)   # 云台初始速度（第一分钟自动）
    gimbal_ctrl.angle_ctrl(0, 0)    # 定位云台扫描标签的初始视角（可修改）
    Marker_list=RmList(vision_ctrl.get_marker_detection_info())    # 更新列表
    time.sleep(0.2) # 短暂延时，为了准确识别标签
    gimbal_ctrl.set_rotate_speed(30)    #上抬扫描速度（快一点应该也可行）
    while not len(Marker_list) >= 6:
        # gimbal_ctrl.rotate_with_degree(rm_define.gimbal_up,1)   # 循环每运行一次，上抬1°（学习澳门一队伍的方法）
        # if gimbal_ctrl.get_axis_angle(rm_define.gimbal_axis_pitch) >= 18:   # 上抬最大角度（可修改）
        #     gimbal_ctrl.set_rotate_speed(80)    # 回位速度
        #     gimbal_ctrl.pitch_ctrl(6)    # 回到初始视角
        #     gimbal_ctrl.set_rotate_speed(30)    # 扫描速度
        time.sleep(0.2)    # 每上抬一次，添加短暂延时，为了准确识别标签
        Marker_list=RmList(vision_ctrl.get_marker_detection_info())    # 更新列表
        print("Marker s = ", Marker_list[1]) # ——Debug——查看扫描到的标签数量
    gimbal_ctrl.stop()
    variable_pitch_0 = gimbal_ctrl.get_axis_angle(rm_define.gimbal_axis_pitch)  # 获取当前俯仰轴角度，为射击准备
    # print("pitch_0_shibie_Base", variable_pitch_0)
    print("Base_Marker_list = ", Marker_list) # ——Debug——查看扫描到的标签列表
    media_ctrl.play_sound(rm_define.media_sound_recognize_success) # 扫描完毕的提示音
    gimbal_ctrl.set_rotate_speed(240)   # 设定射击时的旋转速度（可修改）

# 瞄准基地护甲并击打（第一分钟自动，2倍镜）
def shoot_BASE():
    global variable_pitch_0
    global Marker_list
    global bei_shu
    # print(Marker_list) # ——Debug——
    # 获取扫描到的基地标签信息中的数字ID(不管敌方工程举起了R标签) 
    for ID in range(10, 20): # 从0到9(不过，RMYC2022中，第一分钟，为基地标签为 0#)
        if ID in Marker_list:
            index_ID = Marker_list.index(ID)
        else:
            index_ID = 2 # 否则，取列表中的第2项(ID项)
    print("ID", Marker_list[index_ID]) # ——Debug——
    x = Marker_list[index_ID + 1]
    y = Marker_list[index_ID + 2]
    # print("x, y", x, y)
    error_x = x - 0.5
    turn_angle_x = (error_x * 108)
    turn_angle_y = ((0.5 - y) * 61 - abs(error_x) * 4)  # abs()是为了调斜向射击的偏差
    time.sleep(0.15)    # 云台转动到位之后，短暂停顿，保证射击精度
    gimbal_ctrl.angle_ctrl(turn_angle_x / bei_shu, (variable_pitch_0 + 2.5) + turn_angle_y / bei_shu) # 优化v2.0(倍镜)
    time.sleep(0.2)    # 停顿
    for i in range(70): # 最大限度(射击循环70次)
        gun_ctrl.fire_once()
        time.sleep(0.26)    # 射击之后停顿0.3s(防止过热，同时想保证弹道稳定)
        # time.sleep(0.1)    # 测试用延时，便于观看效果
        media_ctrl.play_sound(rm_define.media_sound_shoot)  # 提示音
    vision_ctrl.disable_detection(rm_define.vision_detection_marker) # 关闭标签识别

