from flask import Blueprint
from werobot import WeRoBot

web = Blueprint('web',__name__)
robot = WeRoBot(token='token')

# @web.app_errorhandler(404)
# def not_found(e):
#     return "not found"

from . import test1
# from . import
# from . import
# from . import