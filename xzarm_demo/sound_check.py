# sound_check.py
# 快速检查语音相关的所有功能：麦克风、录音、扬声器播放声音、语音识别、语音合成
# 小智-学长 2024-10-19

from xzarm_asr import *             # 录音+语音识别
from xzarm_tts import *             # 语音合成模块
print('开始录音5秒')
xzarm_asr_rec(DURATION=5)   # 录音
print('播放录音')
xzarm_tts_play('temp/speech_record.wav')
speech_result = xzarm_asr_recognition()
print('开始语音合成')
xzarm_tts_tts(speech_result)
print('播放语音合成音频')
xzarm_tts_play('temp/xzarm_tts_tts.wav')

