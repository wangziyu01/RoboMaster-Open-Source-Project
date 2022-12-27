'''
使用前，请参阅使用说明（于Discussions）
请安装 Robomaster Python SDK 和 OpenCV-Python
'''

#导入第三方库
from ast import Try
import cv2
import time,traceback
import numpy as np
#RoboMaster SDK
import robomaster
from robomaster import robot
from robomaster import camera


#函数部分
def connect_tt_robot(IP):#连接无人机并初始化函数
    robomaster.config.LOCAL_IP_STR = IP#指定SDK的本地IP地址
    Aimbot_tt.initialize()#初始化无人机
    print("已初始化无人机")
    Aimbot_tt_version = Aimbot_tt.get_sdk_version()#获取飞机版本信息
    print("TT sdk version: {0}".format(Aimbot_tt_version))
    Aimbot_SN = Aimbot_tt.get_sn()#获取无人机的SN号
    print("TT sn: {0}".format(Aimbot_SN))

def Show_UI(frame):#显示UI函数
    attitude = Aimbot_tt.get_attitude()
    Aimbot_tt_battery = Aimbot_tt.battery.get_battery()
    cv2.putText(frame, "AimBot Flying System 2023", (235, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    string1 = "attitude:"+ str(attitude)
    cv2.putText(frame,string1, (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    string2 = "battery:"+ str(Aimbot_tt_battery) + ' %'
    cv2.putText(frame,string2, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return frame
#上色（未使用）
"""
color_dict = {"black": [0, 0, 0], 
              "red": [238, 0, 0], 
              "pink": [255, 192, 203]}
def gray2rgb(gray, color_dict):
    convert gray image into RGB image
    :param gray: single channel image with numpy type 
    :param color_dict: color map
    :return:  rgb image
    # 1：创建新图像容器
    rgb_image = np.zeros(shape=(*gray.shape, 3))
    # 2： 遍历每个像素点
    for i in range(rgb_image.shape[0]):
        for j in range(rgb_image.shape[1]):
            # 3：对不同的灰度值选择不同的颜色
            if gray[i, j].all() < 15:
                rgb_image[i, j, :] = color_dict["black"]
            elif 140 >= gray[i, j] >= 15:
                rgb_image[i, j, :] = color_dict["red"]
            else:
                rgb_image[i, j, :] = color_dict["pink"]

    return rgb_image.astype(np.uint8)
    """
if __name__ == "__main__":
    Aimbot_tt = robot.Drone()#创建Drone类的实例对象Aimbot_tt
    time.sleep(0.05);#缓冲
    try:#尝试(通过判断程序是否报错)
        connect_tt_robot('192.168.10.3')#连接无人机并初始化(IP需要更改) 请使用ipconfig
        print("如果按q程序窗口无法关闭，请关闭程序编辑器 \n")
        Aimbot_tt_camera = Aimbot_tt.camera#获取camera对象
        Aimbot_tt_camera.set_down_vision(0) #下视 1开启 0关闭  下视方法
        Aimbot_tt_camera.start_video_stream(display=False)#打开无人机视频流的传输
        Aimbot_tt_camera.set_fps('high')
        Aimbot_tt_camera.set_resolution('high')
        Aimbot_tt_camera.set_bitrate(6)
        while True:
            Aimbot_tt_video = Aimbot_tt_camera.read_cv2_image()#通过Opencv(cv2)获取无人机的视频流
            Aimbot_tt_video = Show_UI(Aimbot_tt_video) #gray2rgb(Aimbot_tt_video,color_dict)
            cv2.imshow("Aimbot Flying System 2023",Aimbot_tt_video)#显示获取到的图像
            # 监测键盘输入是否为q，为q则退出程序(方便测试)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q退出,结束程序
                break
        # 释放摄像头
        Aimbot_tt_video.release()
        # 结束所有窗口
        cv2.destroyAllWindows()
        Aimbot_tt.close()
        print("成功关闭程序")
    except:#如果程序报错，则运行下面程序
        print("程序出错，请检查程序问题或查看无人机是否连接\n")
        traceback.print_exc()#打印报错信息
