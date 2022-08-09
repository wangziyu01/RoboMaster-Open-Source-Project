#导入第三方库
import cv2
import time,traceback
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
    Aimbot_tt_height = Aimbot_tt.get_height()
    cv2.putText(frame, "AimBot Flying System 2023", (235, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    string = "attitude:"+ str(attitude)
    cv2.putText(frame,string, (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return frame
if __name__ == "__main__":
    Aimbot_tt = robot.Drone()#创建Drone类的实例对象Aimbot_tt
    time.sleep(0.05);#缓冲
    try:#尝试(通过判断程序是否报错)
        connect_tt_robot('192.168.10.2')#连接无人机并初始化(IP需要更改) 请先执行ipconfig命令复制IP地址到此处
        print("如果按q程序窗口无法关闭，请关闭编辑器 \n")
        Aimbot_tt_camera = Aimbot_tt.camera#获取camera对象
        print("成功获取camera对象")
        Aimbot_tt_camera.set_down_vision(1) #下视 1开启 0关闭
        Aimbot_tt_camera.start_video_stream(display=False)#打开无人机视频流的传输
        while True:
            Aimbot_tt_video = Aimbot_tt_camera.read_cv2_image()#通过Opencv(cv2)获取无人机的视频流
            Aimbot_tt_video = Show_UI(Aimbot_tt_video)
            cv2.imshow("Aimbot Flying System 2023",Aimbot_tt_video)#显示获取到的图像
            # 监测键盘输入是否为q，为q则退出程序(方便测试)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q退出,结束程序
                print("程序已正常退出")
                break
        # 释放摄像头
        Aimbot_tt_video.release()
        # 结束所有窗口
        cv2.destroyAllWindows()
        Aimbot_tt.close()
    except:#如果程序报错，则运行下面程序
        print("程序出错，请检查程序问题或查看无人机是否连接\n")
        traceback.print_exc()#打印报错信息
