# xzarm_asr.py
# 小智-学长 2024-10-19
# 录音+语音识别

print('导入录音+语音识别模块')

import pyaudio
import wave
import numpy as np
import os
import sys
from API_KEY import *
import base64
import os
import requests
import json
from API_KEY import *
import os

# 确定麦克风索引号
# import sounddevice as sd
# print(sd.query_devices())
#arecord -l

def xzarm_asr_rec(MIC_INDEX=3, DURATION=5):
    '''
    调用麦克风录音，需用arecord -l命令获取麦克风ID
    DURATION，录音时长
    '''
    print('开始 {} 秒录音'.format(DURATION))
    os.system('sudo arecord -D "plughw:{}" -f dat -c 1 -r 16000 -d {} temp/speech_record.wav'.format(MIC_INDEX, DURATION))
    print('录音结束')
