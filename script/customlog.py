from os import path
from time import asctime, localtime, time

def wlog(logfile, logbody, level='Info'):
    # 日志结构：[时间戳] 消息级别: <文件名> 消息内容
    nowtime = '[' + asctime(localtime(time()))[4:19] + ']'
    with open(logfile, 'a', encoding='UTF-8') as log:
        log.write(nowtime + ' ' +  level +': <' + path.basename(__file__) + '> ' + logbody + '\n')