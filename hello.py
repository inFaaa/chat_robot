import werobot

robot = werobot.WeRoBot(token='tokenhere')

@robot.handler
def hello_world():
    return 'Hello World!'

robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
