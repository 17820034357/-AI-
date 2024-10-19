# xzarm_drag_teaching.py
# 小智-学长 2024-10-19
# 拖动示教

print('导入拖动示教模块')

import time
import os
import sys
import termios
import tty
import threading
import json

from pymycobot import MyCobot280
from pymycobot import PI_PORT, PI_BAUD

# 连接机械臂
mc = MyCobot280(PI_PORT, PI_BAUD, debug=False)

import termios
import tty

class Raw(object):
    """为设备设置原始输入模式"""

    def __init__(self, stream):
        self.stream = stream
        self.fd = self.stream.fileno()

    def __enter__(self):
        self.original_stty = termios.tcgetattr(self.stream)  # 保存原来的终端设置
        tty.setcbreak(self.stream)  # 设置终端为 cbreak 模式

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(self.stream, termios.TCSANOW, self.original_stty)  # 恢复原来的设置



class Helper(object):
    def __init__(self) -> None:
        self.w, self.h = os.get_terminal_size()# 获取终端的宽度和高度

    def echo(self, msg):
        print("\r{}".format(" " * self.w), end="")
        print("\r{}".format(msg), end="")


class TeachingTest(Helper):
    def __init__(self, mycobot) -> None:
        super().__init__()  # 调用父类的初始化方法
        self.mc = mycobot  # 保存传入的 mycobot 实例
        self.recording = False  # 记录状态
        self.playing = False  # 播放状态
        self.record_list = []  # 存储记录的列表
        self.record_t = None  # 记录时间
        self.play_t = None  # 播放时间


    def xzarm_asr_rec(self):
        self.record_list = []
        self.recording = True
        self.mc.set_fresh_mode(0)
        def _record():
            start_t = time.time()

            while self.recording:
                angles = self.mc.get_encoders()#获取电位值
                if angles:
                    self.record_list.append(angles)
                    time.sleep(0.1)
                    print("\r {}".format(time.time() - start_t), end="")

        self.echo("开始录制动作")
        self.record_t = threading.Thread(target=_record, daemon=True)
        self.record_t.start()

    def stop_record(self):
        if self.recording:
            self.recording = False
            self.record_t.join()
            self.echo("停止录制动作")

    def play(self):
        self.echo("开始回放动作")
        for angles in self.record_list:
            # print(angles)
            self.mc.set_encoders(angles, 80)
            time.sleep(0.1)
        self.echo("回放结束\n")

    def loop_play(self):
        self.playing = True

        def _loop():
            len_ = len(self.record_list)
            i = 0
            while self.playing:
                idx_ = i % len_
                i += 1
                self.mc.set_encoders(self.record_list[idx_], 80)
                time.sleep(0.1)

        self.echo("开始循环回放")
        self.play_t = threading.Thread(target=_loop, daemon=True)
        self.play_t.start()

    def stop_loop_play(self):
        if self.playing:
            self.playing = False
            self.play_t.join()
            self.echo("停止循环回放")

    def save_to_local(self):
        if not self.record_list:
            self.echo("No data should save.")
            return

        save_path = os.path.dirname(__file__) + "/temp/xzarm_asr_rec.txt"
        with open(save_path, "w") as f:
            json.dump(self.record_list, f, indent=2)
            self.echo("回放动作导出至:  {}".format(save_path))

    def load_from_local(self):

        with open(os.path.dirname(__file__) + "/temp/xzarm_asr_rec.txt", "r") as f:
            try:
                data = json.load(f)
                self.record_list = data
                self.echo("载入本地动作数据成功")
            except Exception:
                self.echo("Error: invalid data.")

    def print_menu(self):
        print(
            """\
        \r 拖动示教 小智-学长
        \r q: 退出
        \r r: 开始录制动作
        \r c: 停止录制动作
        \r p: 回放动作
        \r P: 循环回放/停止循环回放
        \r s: 将录制的动作保存到本地
        \r l: 从本地读取录制好的动作
        \r f: 放松机械臂
        \r----------------------------------
            """
        )

    def start(self):
        self.print_menu()

        while not False:
            with Raw(sys.stdin):
                key = sys.stdin.read(1)
                if key == "q":
                    break
                elif key == "r":  # recorder
                    self.xzarm_asr_rec()
                elif key == "c":  # stop recorder
                    self.stop_record()
                elif key == "p":  # play
                    self.play()
                elif key == "P":  # loop play
                    if not self.playing:
                        self.loop_play()
                    else:
                        self.stop_loop_play()
                elif key == "s":  # save to local
                    self.save_to_local()
                elif key == "l":  # load from local
                    self.load_from_local()
                elif key == "f":  # free move
                    self.mc.release_all_servos()
                    self.echo("Released")
                else:
                    print(key)
                    continue

def drag_teach():
    
    print('机械臂归零')
    mc.send_angles([0, 0, 0, 0, 0, 0], 40)
    time.sleep(3)
    
    recorder = TeachingTest(mc)
    recorder.start()

    print('机械臂归零')
    mc.send_angles([0, 0, 0, 0, 0, 0], 40)
    time.sleep(3)
