# np_log

## 快速使用
``` pip install np_log```
```python
from np_log import setup_logging
# name为日志文件名，默认为当前文件名，is_logfile为是否生成日志文件
# console_level为控制台打印级别，file_level为保存日志文件级别，默认都为DEBUG
# log_max_days为日志文件保存天数，默认为7天，log_max_size为日志保存最大大小：MB，默认为50MB
logger = setup_logging(name=None,is_logfile=True, console_level="DEBUG", file_level="DEBUG", log_max_days=7, log_max_size=50)
```

## 一、项目简介

本项目提供了一个功能丰富的日志模块，用于在 Python 应用程序中方便地记录日志。它支持控制台和文件日志输出，具备日志级别控制、日志文件按大小自动切分、日志文件保存天数限制等功能，并且能够以 UTF-8 格式保存日志文件。

## 二、功能特性

### （一）日志输出

- **控制台日志输出**：支持将日志信息输出到控制台，并且可以根据需要设置控制台日志的输出级别。
- **文件日志输出**：支持将日志信息写入文件，并且可以根据需要设置文件日志的输出级别。

### （二）日志级别控制

- 提供了常见的日志级别（DEBUG、INFO、WARNING、ERROR、CRITICAL），用户可以在初始化日志模块时分别设置控制台和文件日志的级别。

### （三）日志文件管理

- **按大小切分日志文件**：当单个日志文件大小超过指定的限制（如 50MB）时，会自动将日志文件切分为多个文件，避免单个文件过大。
- **限制日志文件保存天数**：可以设置日志文件的最大保存天数，超过该天数的旧日志文件会被自动清理。

### （四）日志格式化

- **控制台日志颜色化**：控制台输出的日志会根据不同的日志级别显示不同的颜色，便于快速区分日志的严重程度。
- **自定义日志格式**：用户可以自定义日志的格式，包括时间戳、日志级别、文件名、行号和日志消息等内容。

### （五）其他特性

- **支持多级目录创建**：如果指定的日志文件目录不存在，会自动创建多级目录。
- **日志文件以 UTF-8 格式保存**：确保日志文件支持多种字符，避免出现乱码问题。

## 三、安装与使用

### （一）安装

本模块是基于 Python 标准库 `logging` 模块实现的，无需额外安装第三方库，只需确保你的 Python 环境已安装即可。

### （二）使用方法

#### 1\. 引入模块

在你的 Python 脚本中，通过以下方式引入日志模块：

```python
from np_log import setup_logging
```


#### 2\. 初始化日志

调用 `setup_logging` 函数来初始化日志模块，以下是函数的参数说明：

| 参数名称 | 参数类型 | 是否必填 | 默认值 | 参数说明 |
| :--- | :--- | :--- | :--- | :--- |
| name | str | 否 | 调用者的文件名 | 日志器名称，用于区分不同的日志器 |
| is_logfile | bool | 否 | True | 是否创建日志文件 |
| console_level | str | 否 | "DEBUG" | 控制台日志输出级别，可选值为 "DEBUG"、"INFO"、"WARNING"、"ERROR"、"CRITICAL" |
| file_level | str | 否 | "DEBUG" | 文件日志输出级别，可选值与控制台日志级别相同 |
| log_max_days | int | 否 | 7 | 日志文件保存天数 |
| log_max_size | int | 否 | 50 | 单个日志文件最大大小（单位：MB） |

示例代码：

```python
logger = setup_logging(
    name="my_logger",
    is_logfile=True,
    console_level="INFO",
    file_level="WARNING",
    log_max_days=10,
    log_max_size=50
)
```

#### 3\. 记录日志

使用初始化后返回的 `logger` 对象来记录日志，示例如下：

```python
logger.debug("这是一条 debug 日志")
logger.info("这是一条 info 日志")
logger.warning("这是一条 warning 日志")
logger.error("这是一条 error 日志")
logger.critical("这是一条 critical 日志")
```

## 四、代码结构说明

### （一）`mkdir_dir` 函数

用于创建多级目录，如果指定的路径不存在，则会创建目录；如果目录已存在，则不进行任何操作。

### （二）`AbsolutePathFilter` 类

自定义的日志过滤器，用于将日志记录中的 `filename` 替换为文件的绝对路径。

### （三）`ColorFormatter` 类

自定义的日志格式化器，用于为控制台输出的日志添加颜色，便于区分不同级别的日志。

### （四）`CustomRotatingFileHandler` 类

继承自 `RotatingFileHandler`，重写了 `doRollover` 方法，实现自定义命名切分后的日志文件。

### （五）`setup_logging` 函数

核心函数，用于初始化日志模块。根据传入的参数配置日志器，包括设置日志级别、添加控制台和文件处理器等。

## 五、示例代码

以下是一个完整的示例代码，展示了如何使用本日志模块：

```python
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

# 自定义日志文件名格式化器
class CustomRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def doRollover(self):
        """
        重写 doRollover 方法，实现自定义命名切分后的日志文件
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # 获取当前时间戳
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # 构造新的日志文件名
        new_log_filename = f"{self.baseFilename}_{now}"
        # 重命名当前日志文件
        os.rename(self.baseFilename, new_log_filename)
        # 重新打开日志文件
        self.mode = 'a'
        self.stream = self._open()

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
        # 创建 CustomRotatingFileHandler，设置最大文件大小和备份文件数量
        fh = CustomRotatingFileHandler(
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
```

## 六、常见问题解答

### （一）日志文件为什么没有按预期切分？

- 请确保设置了正确的 `log_max_size` 参数值，并且日志文件的大小确实超过了该限制。
- 如果使用的是 `CustomRotatingFileHandler`，请检查 `doRollover` 方法的实现是否正确。

### （二）如何调整日志文件的保存路径？

- 在调用 `setup_logging` 函数时，可以通过修改 `log_dir` 的值来指定日志文件的保存路径。例如：

```python
log_dir = f'/custom/logs/{now}'
```

### （三）日志文件的编码格式不是 UTF-8 怎么办？

- 请确保在创建文件处理器时指定了 `encoding='utf-8'` 参数。如果仍然存在问题，请检查系统的默认编码设置。

## 七、版本信息

- **当前版本**：0.1.4
- **更新日期**：2025-05-08

## 八、联系方式

如果你在使用过程中遇到任何问题，或者有任何建议和反馈，可以通过以下方式联系我们：

- **邮箱**：2558949748@qq.com
- **GitHub**：https://github.com/Liu670/np_log

