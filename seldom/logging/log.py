import sys
import logging.handlers
from colorama import Fore, Style
import os, time

log_file = (os.path.dirname(os.path.dirname(__file__))) + '/' + time.strftime('%Y-%m-%d') + '.log'  # log文件目录
# _logger = logging.getLogger('seldom')
# _logger.setLevel(logging.DEBUG)  # 设置日志记录级别
#
# fh = logging.FileHandler(log_file, 'a', encoding='utf-8')  # 文件输出
# fh.setLevel(logging.DEBUG)
#
# _handler = logging.StreamHandler(sys.stdout)  # 控制台输出
# _handler.setLevel(logging.DEBUG)
#
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
# fh.setFormatter(formatter)
# _handler.setFormatter(formatter)
#
# _logger.addHandler(fh)
# _logger.addHandler(_handler)
#
#
# def debug(msg):
#     _logger.debug("DEBUG " + str(msg))
#
#
# def info(msg):
#     _logger.info(Fore.GREEN + "INFO " + str(msg) + Style.RESET_ALL)
#
#
# def error(msg):
#     _logger.error(Fore.RED + "ERROR " + str(msg) + Style.RESET_ALL)
#
#
# def warn(msg):
#     _logger.warning(Fore.YELLOW + "WARNING " + str(msg) + Style.RESET_ALL)
#
#
# def _print(msg):
#     _logger.debug(Fore.BLUE + "PRINT " + str(msg) + Style.RESET_ALL)
#
#
# def set_level(level):
#     """ 设置log级别
#
#     :param level: logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR
#     :return:
#     """
#     _logger.setLevel(level)
#
#
# def set_level_to_debug():
#     _logger.setLevel(logging.DEBUG)


# def set_level_to_info():
#     _logger.setLevel(logging.INFO)
#
#
# def set_level_to_warn():
#     _logger.setLevel(logging.WARN)
#
#
# def set_level_to_error():
#     _logger.setLevel(logging.ERROR)

# if __name__ == '__main__':
#     # log_file = (os.path.dirname(os.path.dirname(__file__))) + '/' + time.strftime('%Y-%m-%d') + '.log'
#     print(log_file)

class Log():
    """日志模块，在log路径下生成log文件，以小时分割。同时控制台也会打印，当使用使用unittest添加用例调用HTMLTest报告模块时
    控制台的输出内容会被HTMLTest报告模块接受而不再控制台显示
    """

    def print_console(self, level, message):
        # 创建一个log
        # log_file_path = Method().output_dir('log') + time.strftime('%Y-%m-%d-%H') + '.log'
        log_file_path = (os.path.dirname(os.path.dirname(__file__))) + '/' \
                        + time.strftime('%Y-%m-%d') + '.log'  # log文件目录

        logger = logging.getLogger(__name__)

        # 设置日志记录级别
        logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(log_file_path, 'a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s- %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给log添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)

        # 记录一条日志
        if level == 'info':
            logger.info(message)
        elif level == 'debug':
            logger.debug(message)
        elif level == 'warning':
            logger.warning(message)
        elif level == 'error':
            logger.error(message)
        logger.removeHandler(ch)
        logger.removeHandler(fh)
        # time.sleep(1)
        fh.close()

    def debug(self, message):
        self.print_console('debug', message)

    def info(self, message):
        self.print_console('info', message)

    def warn(self, message):
        self.print_console('warn', message)

    def error(self, message):
        self.print_console('error', message)
