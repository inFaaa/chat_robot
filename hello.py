import werobot

robot = werobot.WeRoBot(token='tokenhere')

@robot.text
def hello_world():
    return 'Hello World!'

robot.run()
