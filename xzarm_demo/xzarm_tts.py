# xzarm_tts.py
# 小智-学长 2024-5-23
# 语音合成

print('导入语音合成模块')

import os
import appbuilder
from API_KEY import *
os.environ["APPBUILDER_TOKEN"] = APPBUILDER_TOKEN
tts_ab = appbuilder.TTS()


def xzarm_tts_tts(TEXT='我是小智大模型AI机械臂，您可以说出你的要求，我会一一完成要求', tts_wav_path = 'temp/xzarm_tts_tts.wav'):
    '''语音合成TTS，生成wav音频文件'''
    inp = appbuilder.Message(content={"text": TEXT})
    out = tts_ab.run(inp, model="paddlespeech-tts", audio_type="wav")
    with open(tts_wav_path, "wb") as f:
        f.write(out.content["audio_binary"])
    print("TTS语音合成，导出wav音频文件至：{}".format(tts_wav_path))
#xzarm_tts_tts(TEXT='我是小智大模型AI机械臂，您可以说出你的要求，我会一一完成要求哦', tts_wav_path = 'temp/xzarm_tts_tts.wav')
def xzarm_tts_play(wav_file='start/welcome.wav'):
    '''
    播放wav音频文件
    '''
    prompt = 'aplay -t wav {} -q'.format(wav_file)
    os.system(prompt)
