import logging
import os

class Setting:
    LEVEL           = logging.DEBUG
    BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
    FILE_NAME       = os.path.join(BASE_DIR, "shrimp_bot.log")
    FORMAT          = "[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s"

def get_logger(name):
    """봇 로그 클래스

    :param name: 로거 이름
    :type name: str
    :return: 로거 인스턴스
        
    """

    logger          = logging.getLogger(name)
    formatter       = logging.Formatter(Setting.FORMAT)
    stream_handler  = logging.StreamHandler() 
    file_handler    = logging.FileHandler(
        filename    = Setting.FILE_NAME,
        encoding    = 'utf-8'
    )

    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    logger.setLevel(Setting.LEVEL)

    return logger
