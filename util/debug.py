import logging
"""
    详细信息使用info
    简略信息使用debug
"""
def set_debuger(level):
    _log_level = [logging.WARNING,logging.INFO,logging.DEBUG]
    LOG_FORMAT = "%(asctime)s %(levelname)s\t%(threadName)s %(message)s "#配置输出日志格式
    DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a ' #配置输出时间格式
    LOG_LEVEL = _log_level[level]

    _format = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    _handler = logging.StreamHandler()
    _handler.setFormatter(_format)

    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(_handler)
    
    return logger