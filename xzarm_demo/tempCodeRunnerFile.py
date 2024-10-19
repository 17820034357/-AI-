def xzarm_asr_rec(MIC_INDEX=0, DURATION=5):
    '''
    调用麦克风录音，需用arecord -l命令获取麦克风ID
    DURATION，录音时长
    '''
    print('开始 {} 秒录音'.format(DURATION))
    os.system('sudo arecord -D "plughw:{}" -f dat -c 1 -r 16000 -d {} temp/speech_record.wav'.format(MIC_INDEX, DURATION))
    print('录音结束')