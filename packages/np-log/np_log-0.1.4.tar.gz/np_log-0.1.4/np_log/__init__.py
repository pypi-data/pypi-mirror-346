import datetime
import logging
import logging.handlers
import os
import sys

# 创建多级目录
def mkdir_dir(path):
    # 判断路径是否存在
    isExists = os.path.exists(path)

    if not isExists:
        # 如果不存在，则创建目录（多层）
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False

# 自定义过滤器，用于替换 filename 为绝对路径
class AbsolutePathFilter(logging.Filter):
    def filter(self, record):
        record.abspath = os.path.abspath(record.pathname)
        return True

# 自定义日志格式化器，用于添加颜色
class ColorFormatter(logging.Formatter):
    # 定义不同日志等级的颜色
    COLORS = {
        logging.DEBUG: "\033[36m",  # Cyan
        logging.INFO: "\033[32m",  # Green
        logging.WARNING: "\033[33m",  # Yellow
        logging.ERROR: "\033[31m",  # Red
        logging.CRITICAL: "\033[35m",  # Magenta
    }
    RESET = "\033[0m"  # Reset color

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, "")
        message = logging.Formatter.format(self, record)
        return f"{log_color}{message}{self.RESET}"

# 创建日志
def setup_logging(name=None, is_logfile=True, console_level="DEBUG", file_level="DEBUG", log_max_days=7, log_max_size=50):
    """
    创建日志配置
    :param name: 日志器名称，默认为调用者的文件名
    :param is_logfile: 是否创建日志文件，默认为 True
    :param console_level: 控制台日志输出级别，默认为 "DEBUG"
    :param file_level: 文件日志输出级别，默认为 "DEBUG"
    :param log_max_days: 日志文件保存天数，默认为 7 天
    :param log_max_size: 单个日志文件最大大小（单位：MB），默认为 50MB
    :return: 配置好的日志器
    """
    # 如果没有传入 name，则获取调用者的文件名
    if name is None:
        frame = sys._getframe(1)  # 获取上一级调用的帧信息
        caller_filename = os.path.basename(frame.f_code.co_filename)
        name = os.path.splitext(caller_filename)[0]  # 去掉文件扩展名
    # 使用固定的日志器名称
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 清理现有处理器
    if logger.hasHandlers():
        logger.handlers.clear()

    # 创建流处理器
    ch = logging.StreamHandler()
    ch.setLevel(logging.getLevelName(console_level.upper()))  # 将字符串转换为日志级别
    formatter = ColorFormatter(
        "%(asctime)s [%(levelname)s] [ \"%(filename)s:%(lineno)d\" ] %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # 添加自定义过滤器
    logger.addFilter(AbsolutePathFilter())

    # 根据 is_logfile 参数决定是否创建文件处理器
    if is_logfile:
        now = datetime.datetime.now().strftime("%Y%m%d")
        log_dir = f'logs/{now}'
        mkdir_dir(log_dir)
        log_file = os.path.join(log_dir, f'{name}.log')
        # 创建 RotatingFileHandler，设置最大文件大小和备份文件数量
        fh = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=log_max_size * 1024 * 1024,  # 将MB转换为字节
            backupCount=log_max_days,
            encoding='utf-8'
        )
        fh.setLevel(logging.getLevelName(file_level.upper()))  # 将字符串转换为日志级别
        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(file_formatter)
        logger.addHandler(fh)

    # 禁止日志传播
    logger.propagate = False

    return logger


if __name__ == "__main__":
    # 设置控制台日志级别为 "INFO"，文件日志级别为 "WARNING"，日志文件保存天数为 10 天，单个日志文件最大大小为 50MB
    logger = setup_logging(console_level="INFO", file_level="WARNING", log_max_days=10, log_max_size=50)

    logger.debug("这是一条 debug 日志")
    logger.info("这是一条 info 日志")
    logger.warning("这是一条 warning 日志")
    logger.error("这是一条 error 日志")
    logger.critical("这是一条 critical 日志")