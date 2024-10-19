# -*- coding: utf-8 -*-

# agent_go.py
# 小智-学长 2024-10-19
# 能看图识物、听懂指令、精准执行任务的机械臂
# 机械臂+大模型+多姿态+语音识别
#大模型AI机械臂

print('\n能看图识物、听懂指令、精准执行任务的机械臂！')
print('小智-学长 2024-10-19 \n')

# 导入常用函数
from xzarm_asr import *             # 录音+语音识别
from xzarm_robot import *           # 连接机械臂
from xzarm_model import *           # 大语言模型API
from xzarm_led import *             # 控制LED灯颜色
from xzarm_camera import *          # 摄像头
from xzarm_robot import *           # 机械臂运动
from xzarm_pump import *            # GPIO、吸泵
from xzarm_image_move import *        # 大模型识别图像，吸泵吸取并移动物体
from xzarm_drag_teaching import *   # 拖动示教
from xzarm_action import *          # 大模型AI机械臂编排
from xzarm_tts import *             # 语音合成模块
from xzarm_image_handle import *

# print('播放欢迎词')
pump_off()
# back_zero()
xzarm_tts_play('start/welcome.wav')


def agent_play():
    '''
    主函数，语音控制机械臂智能体编排动作
    '''
    # 归零
    back_zero()
    
    # print('测试摄像头')
    # check_camera()
    
    # 输入指令
    # 先回到原点，再把LED灯改为墨绿色，然后把绿色方块放在篮球上
    start_record_ok = input('是否开启录音，输入数字录音指定时长，按k打字输入，按c输入默认指令\n')
    if start_record_ok.isnumeric():
        DURATION = int(start_record_ok)
        xzarm_asr_rec(DURATION=DURATION)   # 录音
        order = xzarm_asr_recognition() # 语音识别
    elif start_record_ok == 'k':
        order = input('请输入指令')
    elif start_record_ok == 'c':
        order = '先归零，再摇头，然后把绿色方块放在篮球上'
    else:
        print('无指令，退出')
        # exit()
        raise NameError('无指令，退出')
    
    # 大模型AI机械臂编排动作
    agent_plan_output = eval(xzarm_action_plan(order))#可以把一个字符串当成代码执行
    
    print('大模型AI机械臂编排动作如下\n', agent_plan_output)
    # plan_ok = input('是否继续？按c继续，按q退出')
    plan_ok = 'c'
    if plan_ok == 'c':
        response = agent_plan_output['response'] # 获取机器人想对我说的话
        print('开始语音合成')
        xzarm_tts_tts(response)                     # 语音合成，导出wav音频文件
        xzarm_tts_play('temp/xzarm_tts_tts.wav')          # 播放语音合成音频文件
        for each in agent_plan_output['function']: # 运行大模型AI机械臂规划编排的每个函数
            print('开始执行动作', each)
            eval(each)
    elif plan_ok =='q':
        # exit()
        raise NameError('按q退出')

# agent_play()
if __name__ == '__main__':
    agent_play()

