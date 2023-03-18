"""
-*-coding: utf-8-*-

24点核心计算程序

版权所有(C) 2023 wangziyu0305

Copyright(C) 2023 wangziyu0305

Ver 2.0.0 Release

Bug(s):

1.无法在RoboMaster APP中运行    解决

更新日志：

1.0.0_Release 计算24点混合运算

2.0.0.230203_Alpha 修复减法函数中ab-c问题

2.0.0.230204_Beta_1 新增加ab-c-d方式（感谢Jason王）

2.0.0.230205_Beta_2 添加/完善注释

2.0.0.230215_RC 通过功能测试

2.0.0 Release
"""

# 定义公用变量
ID_list = [13, 16, 16, 16]  # 获取到的ID
num_list = []  # 经过处理后的数字（不含符号）
symbol = 41  # 加法40 减法41 乘法33 除法42
# shoot_list = []
shoot_ID_list = []  # 击打列表


def full_arrangement(numbers):
    # numbers 形参，传入列表（生成列表元素全排列）
    number_seq = []
    for p_number1 in numbers:
        n1 = numbers.copy()
        n1.remove(p_number1)
        for p_number2 in n1:
            n2 = n1.copy()
            n2.remove(p_number2)
            for p_number3 in n2:
                n3 = n2.copy()
                n3.remove(p_number3)
                seq = [p_number1, p_number2, p_number3, n3[0]]
                number_seq.append(seq)
    return number_seq  # 返回全排列二维数组


def cal_24(nums):
    # nums：形参，传入已全排列的二维数组（列表）进行判断使用何种计算方式
    shoot_list = []
    if symbol == 40:  # 符号位为40，使用加法，调用加法计算函数
        for item in nums:
            shoot_list = addition(item)  # 如果失败（shoot_list无元素）则使用全排列下一个数组（下面一样）
            if len(shoot_list) != 0:
                break
    elif symbol == 41:  # 符号位为41，使用减法，调用减法函数
        for item in nums:
            shoot_list = subtraction(item)
            if len(shoot_list) != 0:
                break
    elif symbol == 42:  # 符号位为42，使用除法，调用除法函数
        for item in nums:
            shoot_list = division(item)
            if len(shoot_list) != 0 and len(shoot_list) < 5:
                break
    elif symbol == 33:  # 符号位为33，使用乘法，调用乘法函数
        for item in nums:
            shoot_list = multiplication(item)
            if len(shoot_list) != 0:
                break
    return shoot_list


def subtraction(item):  # 减法计算函数
    shoot_list = []
    result = item[0] * 10 + item[1] - item[2]  # ab-c
    if result == 24:
        shoot_list = [item[0], item[1], symbol, item[2]]
    else:
        result = item[0] * 10 + item[1] - item[2] * 10 - item[3]  # ab-cd
        if result == 24:
            shoot_list = [item[0], item[1], symbol, item[2], item[3]]
        else:
            result = item[0] * 10 + item[1] - item[2] - item[3]  # ab-c-d
            if result == 24:
                shoot_list = [item[0], item[1], symbol, item[2], symbol, item[3]]
    return shoot_list  # 返回shoot_list


def addition(item):  # 加法计算函数
    shoot_list = []
    result = item[0] + item[1] + item[2]  # a+b+c
    if result == 24:
        shoot_list = [item[0], symbol, item[2], item[3]]
    else:
        result = item[0] + item[1] + item[2] + item[3]  # a+b+c+d
        if result == 24:
            shoot_list = [item[0], symbol, item[1], symbol, item[2], symbol, item[3]]
        else:
            result = item[0] * 10 + item[1] + item[2]  # ab+c
            if result == 24:
                shoot_list = [item[0], item[1], symbol, item[2]]
            else:
                result = item[0] * 10 + item[1] + item[2] + item[3]  # ab+c+d
                if result == 24:
                    shoot_list = [item[0], item[1], symbol, item[2], symbol, item[3]]
                else:
                    result = item[0] * 10 + item[1] + item[2] * 10 + item[3]  # ab+cd
                    if result == 24:
                        shoot_list = [item[0], item[1], symbol, item[2], item[3]]
    return shoot_list


def division(item):  # 除法计算函数
    shoot_list = []
    if 1 in item and 2 in item and 0 in item and 5 in item:  # 特判120/5
        shoot_list = [1, 2, 0, symbol, 5]
        return shoot_list
    if item[2] != 0:
        temp = (item[0] * 10 + item[1]) / item[2]
        if temp == 24:
            shoot_list = [item[0], item[1], symbol, item[2]]
        else:
            if item[3] != 0:
                if (temp / item[3]) == 24:
                    shoot_list = [item[0], item[1], symbol, item[2], symbol, item[3]]
                elif (item[0] * 100 + item[1] * 10 + item[2]) / item[3] == 24:
                    shoot_list = [item[0], item[1], item[2], symbol, item[3]]
    return shoot_list


def multiplication(item):  # 乘法计算函数
    shoot_list = []
    result = item[0] * item[1]  # a*b
    if result == 24:
        shoot_list = [item[0], symbol, item[1]]
    else:
        result = item[0] * 10 + item[1] * item[2]  # ab*c
        if result == 24:
            shoot_list = [item[0], item[1], symbol, item[2]]
        else:
            result = item[0] * item[1] * item[2]  # a*b*c
            if result == 24:
                shoot_list = [item[0], symbol, item[1], symbol, item[2]]
    return shoot_list


# -------------------------------------------------------函数部分结束-----------------------------------------------------

if __name__ == '__main__':  # 主函数开始
    for i in ID_list:
        i -= 10
        if i > 10:
            symbol = i
        else:
            num_list.append(i)
    ATK = cal_24(full_arrangement(num_list))
    for i in ATK:
        i += 10
        shoot_ID_list.append(i)
    print(shoot_ID_list) # 打印结果
