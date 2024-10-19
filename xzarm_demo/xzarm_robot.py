# xzarm_robot.py
# 小智-学长 2024-10-19
# 启动并连接机械臂，导入各种工具包

print('导入机械臂连接模块')

from pymycobot import MyCobot280
from pymycobot import PI_PORT, PI_BAUD
import cv2
import numpy as np
import time
from xzarm_pump import *

# 连接机械臂
mc = MyCobot280(PI_PORT, PI_BAUD)
# 设置运动模式为插补
mc.set_fresh_mode(0)

import RPi.GPIO as GPIO
# 初始化GPIO
GPIO.setwarnings(False)   # 不打印 warning 信息
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.output(20, 1)        # 关闭吸泵电磁阀

def back_zero():
    '''
    机械臂归零
    '''
    print('机械臂归零')
    mc.send_angles([0, 0, 0, 0, 0, 0], 40)
    time.sleep(3)

def relax_arms():
    print('放松机械臂关节')
    mc.release_all_servos()

def head_shake():
    # 左右摆头
    mc.send_angles([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],70)
    time.sleep(1)
    for count in range(2):
        mc.send_angle(5, 30, 80)
        time.sleep(0.5)
        mc.send_angle(5, -30,80)
        time.sleep(0.5)
    # mc.send_angles([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],70)
    # time.sleep(1)
    mc.send_angles([0, 0, 0, 0, 0, 0], 40)
    time.sleep(2)

def head_dance():
    # 跳舞
    mc.send_angles([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],70)
    time.sleep(1)
    for count in range(1):
        mc.send_angles([(-0.17),(-94.3),118.91,(-39.9),59.32,(-0.52)],80)
        time.sleep(1.2)
        mc.send_angles([67.85,(-3.42),(-116.98),106.52,23.11,(-0.52)],80)
        time.sleep(1.7)
        mc.send_angles([(-38.14),(-115.04),116.63,69.69,3.25,(-11.6)],80)
        time.sleep(1.7)
        mc.send_angles([2.72,(-26.19),140.27,(-110.74),(-6.15),(-11.25)],80)
        time.sleep(1)
        mc.send_angles([0,0,0,0,0,0],80)

def head_nod():
    # 点头
    mc.send_angles([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],70)
    for count in range(2):
        mc.send_angle(4, 13, 70)
        time.sleep(0.5)
        mc.send_angle(4, -20, 70)
        time.sleep(1)
        mc.send_angle(4,13,70)
        time.sleep(0.5)
    mc.send_angles([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],70)

def move_to_coords(X=150, Y=-130, HEIGHT_SAFE=230):
    print('移动至指定坐标：X {} Y {}'.format(X, Y))
    mc.send_coords([X, Y, HEIGHT_SAFE, 0, 180, 90], 20, 0)
    time.sleep(4)

def single_joint_move(joint_index, angle):
    print('关节 {} 旋转至 {} 度'.format(joint_index, angle))
    mc.send_angle(joint_index, angle, 40)
    time.sleep(2)

def move_to_top_view():
    print('移动至俯视姿态')
    mc.send_angles([2.46, -8.26, -5.53, -74.0, -0.43, 94.74], 10)
    time.sleep(3)

def top_view_shot(check=False):
    '''
    拍摄一张图片并保存
    check：是否需要人工看屏幕确认拍照成功，再在键盘上按q键确认继续
    '''
    print('    移动至俯视姿态')
    move_to_top_view()
    
    # 获取摄像头，传入0表示获取系统默认摄像头
    cap = cv2.VideoCapture(0)
    # 打开cap
    cap.open(0)
    time.sleep(0.3)
    success, img_bgr = cap.read()
    
    # 保存图像
    print('    保存至temp/vl_now.jpg')
    cv2.imwrite('temp/vl_now.jpg', img_bgr)

    # 屏幕上展示图像
    cv2.destroyAllWindows()   # 关闭所有opencv窗口
    cv2.imshow('zihao_vlm', img_bgr) 
    
    if check:
        print('请确认拍照成功，按c键继续，按q键退出')
        while(True):
            key = cv2.waitKey(10) & 0xFF
            if key == ord('c'): # 按c键继续
                break
            if key == ord('q'): # 按q键退出
                # exit()
                cv2.destroyAllWindows()   # 关闭所有opencv窗口
                raise NameError('按q退出')
    else:
        if cv2.waitKey(10) & 0xFF == None:
            pass
        
    # 关闭摄像头
    cap.release()
    # 关闭图像窗口
    # cv2.destroyAllWindows()

def hand_eye_calibration(X_pixel=160, Y_pixel=120):
    '''
    输入目标点在图像中的像素坐标，转换为机械臂坐标
    '''
    # 计算机械臂的Y轴（对应图像的X轴）上的坐标
    # 整理两个标定点的坐标
    cali_1_pixel = [591,435]                       # 左上角，第一个标定点的像素坐标，要手动填！
    cali_1_mc = [239.6, 117.1]                  # 左上角，第一个标定点的机械臂坐标，要手动填！
    cali_2_pixel = [51,71]                         # 右下角，第二个标定点的像素坐标
    cali_2_mc = [51.0, -140.6]                    # 右下角，第二个标定点的机械臂坐标，要手动填！


    Y_cali_im = [cali_2_pixel[0], cali_1_pixel[0]]  # 图像的X轴像素坐标（先小后大）
    Y_cali_mc = [cali_2_mc[1], cali_1_mc[1]]  # 机械臂的Y轴坐标
    
    Y_mc = np.interp(X_pixel, Y_cali_im, Y_cali_mc)  # 使用插值法计算机械臂Y轴的坐标
    
    # 计算机械臂的X轴（对应图像的Y轴）上的坐标
    X_cali_im = [cali_2_pixel[1], cali_1_pixel[1]]  # 图像的Y轴像素坐标（先小后大）
    X_cali_mc = [cali_2_mc[0], cali_1_mc[0]]  # 机械臂的X轴坐标
    
    X_mc = np.interp(Y_pixel, X_cali_im, X_cali_mc)  # 使用插值法计算机械臂X轴的坐标
  



    return X_mc, Y_mc

# 吸泵吸取并移动物体
def pump_move(mc, XY_START=[230,-50], HEIGHT_START=120, XY_END=[100,220], HEIGHT_END=120, HEIGHT_SAFE=200):

    '''
    用吸泵，将物体从起点吸取移动至终点

    mc：机械臂实例
    XY_START：起点机械臂坐标
    HEIGHT_START：起点高度，方块用90，药盒子用70
    XY_END：终点机械臂坐标
    HEIGHT_END：终点高度
    HEIGHT_SAFE：搬运途中安全高度
    '''
    
    # 初始化GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)

    # 设置运动模式为插补
    mc.set_fresh_mode(0)
    
    # # 机械臂归零
    # print('    机械臂归零')
    # mc.send_angles([0, 0, 0, 0, 0, 0], 40)
    # time.sleep(4)
    
    # 吸泵移动至物体上方
    print('    吸泵移动至物体上方')
    mc.send_coords([XY_START[0], XY_START[1], HEIGHT_SAFE, 0, 180, 90], 20, 0)
    time.sleep(2)


    
    # 吸泵向下吸取物体
    print('    吸泵向下吸取物体')
    XY_START[0]-=15
    mc.send_coords([XY_START[0], XY_START[1], HEIGHT_START, 0, 180, 90], 15, 0)
    time.sleep(2)
    
    # 开启吸泵
    pump_on()

    # 升起物体
    print('    升起物体')
    mc.send_coord(3, HEIGHT_SAFE,20)
    time.sleep(2)

    # 搬运物体至目标上方
    print('    搬运物体至目标上方')
    mc.send_coords([XY_END[0], XY_END[1], HEIGHT_SAFE, 0, 180, 90], 15, 0)
    time.sleep(2)

    # 向下放下物体
    print('    向下放下物体')
    mc.send_coords([XY_END[0], XY_END[1], HEIGHT_END, 0, 180, 90], 20, 0)
    time.sleep(2)

    # 关闭吸泵
    pump_off()

    # 机械臂归零
    print('    机械臂归零')
    mc.send_angles([0, 0, 0, 0, 0, 0], 40)
    time.sleep(2)
#pump_move(mc, XY_START=[183,-100], HEIGHT_START=120, XY_END=[197,88], HEIGHT_END=120, HEIGHT_SAFE=200)