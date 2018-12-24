from werobot import WeRoBot
import jieba

robot = WeRoBot(token='tokenhere')

@robot.handler
def processer(message):
    seg_list = jieba.cut(message)
    return "|".join(seg_list) 
    