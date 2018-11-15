from app import create_app,create_robot
import threading

if __name__=="__main__":
    app = create_app()
    robot = create_robot()
    #之所以这样是为了确保是正确的对象执行run
    def func1():
        app.run()
    def func2():
        robot.run()

    t1 = threading.Thread(target=func1)
    t2 = threading.Thread(target=func2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()