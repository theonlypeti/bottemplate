import logging
from logging.handlers import WatchedFileHandler
from datetime import datetime
from os import makedirs
import coloredlogs

baselogger = logging.getLogger("Base")

# formatting the colorlogger
fmt = "[ %(asctime)s %(filename)s %(lineno)d %(funcName)s %(levelname)s ] %(message)s"
coloredlogs.DEFAULT_FIELD_STYLES = {'asctime': {'color': 'green'}, 'lineno': {'color': 'magenta'},
                                    'levelname': {'bold': True, 'color': 'black'}, 'filename': {'color': 'blue'},
                                    'funcname': {'color': 'cyan'}}
coloredlogs.DEFAULT_LEVEL_STYLES = {'critical': {'bold': True, 'color': 'red'},
                                    'debug': {'bold': True, 'color': 'black'}, 'error': {'color': 'red'},
                                    'info': {'color': 'green'}, 'notice': {'color': 'magenta'},
                                    'spam': {'color': 'green', 'faint': True},
                                    'success': {'bold': True, 'color': 'green'}, 'verbose': {'color': 'blue'},
                                    'warning': {'color': 'yellow'}}


def init(args):
    if args.logfile:  # if you need a text file
        FORMAT = "[{asctime}][{filename}][{lineno:4}][{funcName}][{levelname}] {message}"
        formatter = logging.Formatter(FORMAT, style="{")  # this is for default logger
        filename = f"./logs/bot_log_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt"
        makedirs(r"./logs", exist_ok=True)
        with open(filename, "w", encoding="utf-8") as _:
            pass
        fl = WatchedFileHandler(filename, encoding="utf-8")
        fl.setFormatter(formatter)
        fl.setLevel(logging.DEBUG)
        # logging.addLevelName(25, "Event")   #this might need to be moved all the way up before getting the baselogger? Update default_level_styles accordingly
        # fl.addFilter(lambda rec: rec.levelno == 25) #if u only wanna filter out the event level
        baselogger.addHandler(fl)

    baselogger.setLevel(logging.DEBUG)  # base is debug, so the file handler could catch debug msgs too
    if args.debug:
        coloredlogs.install(level=logging.DEBUG, logger=baselogger, fmt=fmt)
    else:
        coloredlogs.install(level=logging.INFO, logger=baselogger, fmt=fmt)
