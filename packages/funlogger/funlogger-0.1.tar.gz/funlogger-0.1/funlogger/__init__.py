#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2025 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: Apache Software License
import logging
import os
import re
import sys
import threading
import weakref

from colorama import Fore, Style, init

from funlogger.config import config


class Singleton(type):
    """单例模式"""

    _instance_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Singleton.__instance = None
        # 初始化存放实例地址
        self._cache = weakref.WeakValueDictionary()

    def __call__(self, *args, **kwargs):
        # 提取类初始化时的参数
        kargs = "".join([f"{key}" for key in args]) if args else ""
        kkwargs = "".join([f"{key}" for key in kwargs]) if kwargs else ""
        # 判断相同参数的实例师否被创建
        if kargs + kkwargs not in self._cache:  # 存在则从内存地址中取实例
            with Singleton._instance_lock:
                Singleton.__instance = super().__call__(*args, **kwargs)
                self._cache[kargs + kkwargs] = Singleton.__instance
        # 不存在则新建实例
        else:
            Singleton.__instance = self._cache[kargs + kkwargs]
        return Singleton.__instance


class logger(metaclass=Singleton):
    """logger"""
    _custom_tag = config.TAG

    def __init__(self, level="DEBUG", LOG_FILE_NAME="test.log", custom_tag=None):
        """
        日志配置
        :param level: case 路径
        """
        # 清空其他日志配置
        logger._custom_tag = custom_tag or "default"
        logging.root.handlers = []
        # log_path = os.path.join(LOG_FILE_PATH)
        log_path = config.LOG_FILE_PATH
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        logfile = os.path.join(
            log_path, LOG_FILE_NAME
        )

        try:
            self.ip_end = re.findall(r"\d+.\d+.\d+.(\d+)", f"{config.HOST_IP}")[0]
            self.ip_flag = f"-{self.ip_end}"
        except IndexError:
            self.ip_flag = ""
        self.sys_arch = config.SYS_ARCH
        self.date_format = "%m/%d %H:%M:%S"
        self.log_format = (
            f"{self.sys_arch}{self.ip_flag}: "
            "%(asctime)s | %(levelname)s | %(message)s"
        )
        self.logger = logging.getLogger()
        self.logger.setLevel(level)  # Log等级总开关
        self.logger.addFilter(IgnoreFilter())
        _fh = logging.FileHandler(logfile, mode="a+")
        _fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
        _fh.addFilter(IgnoreFilter())
        _fh.setFormatter(
            logging.Formatter(
                self.log_format,
                datefmt=self.date_format,
                # datefmt=f"{Fore.RED}{self.date_format}{Style.RESET_ALL}",
            )
        )
        fh_error = logging.FileHandler(logfile, mode="a+")
        _fh.setFormatter(
            logging.Formatter(
                self.log_format,
                datefmt=self.date_format,
            )
        )
        fh_error.setLevel(logging.ERROR)  # 输出到file的log等级的开关
        # 第四步，再创建一个handler，用于输出到控制台
        _ch = logging.StreamHandler()
        _ch.setLevel(level)  # 输出到console的log等级的开关
        _ch.addFilter(IgnoreFilter())
        # 第五步，定义handler的输出格式
        formatter = _ColoredFormatter(
            f"{Fore.GREEN}{self.sys_arch}{self.ip_flag}: {Style.RESET_ALL}"
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt=f"{Fore.RED}{self.date_format}{Style.RESET_ALL}",
        )
        _ch.setFormatter(formatter)
        # 第六步，将logger添加到handler里面
        self.logger.addHandler(_fh)
        self.logger.addHandler(fh_error)
        self.logger.addHandler(_ch)

    @staticmethod
    def _build_prefix(autoadd=True):
        """
        构建日志前缀，格式为 [<custom_tag>][文件名][函数名]

        Args:
            autoadd (bool): 是否添加文件名和函数名，默认为 True

        Returns:
            str: 格式化的前缀
        """
        prefix = f"[{logger._custom_tag}]"
        if autoadd:
            current_frame = sys._getframe(2) if hasattr(sys, "_getframe") else None  # 调整为 sys._getframe(2)
            if current_frame:
                file_name = os.path.basename(current_frame.f_code.co_filename)
                func_name = current_frame.f_code.co_name
                prefix += f"[{file_name}][{func_name}]"
            else:
                prefix += "[unknown][unknown]"
        return prefix

    @staticmethod
    def info(message, autoadd=True):
        """记录 INFO 级别日志"""
        formatted_message = f"{logger._build_prefix(autoadd)} {message}"
        logging.info(formatted_message)

    @staticmethod
    def debug(message, autoadd=True):
        """记录 DEBUG 级别日志"""
        formatted_message = f"{logger._build_prefix(autoadd)} {message}"
        try:
            current_frame1 = sys._getframe(2) if hasattr(sys, "_getframe") else None
            if current_frame1 and current_frame1.f_code.co_name.startswith("test_"):
                logging.info(formatted_message)
            else:
                logging.debug(formatted_message)
        except ValueError:
            logging.debug(formatted_message)

    @staticmethod
    def error(message, autoadd=True):
        """记录 ERROR 级别日志"""
        formatted_message = f"{logger._build_prefix(autoadd)} {message}"
        logging.error(formatted_message)

    @staticmethod
    def warning(message, autoadd=True):
        """记录 WARNING 级别日志"""
        formatted_message = f"{logger._build_prefix(autoadd)} {message}"
        logging.warning(formatted_message)


init(autoreset=True) 

class _ColoredFormatter(logging.Formatter):
    """自定义格式化器，为控制台日志添加颜色"""

    # 定义日志级别的颜色映射
    LEVEL_COLORS = {
        "INFO": Fore.WHITE,    # 白色
        "DEBUG": Fore.BLUE,    # 蓝色
        "ERROR": Fore.RED,     # 红色
        "WARNING": Fore.YELLOW # 黄色
    }

    def formatMessage(self, record: logging.LogRecord) -> str:
        """为日志消息添加颜色格式"""
        # 移除消息中的任何现有 ANSI 代码，防止嵌套日志干扰
        clean_message = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', record.message)

        # 获取日志级别的颜色
        level_color = self.LEVEL_COLORS.get(record.levelname, Fore.WHITE)

        # 解析消息，匹配 [custom_tag][file][func] 结构
        prefix_match = re.match(r'(\[[^\]]+\])(\[[^\]]+\])(\[[^\]]+\])(.*)', clean_message)
        if prefix_match:
            custom_tag, file_name, func_name, content = prefix_match.groups()
            # 前缀使用固定颜色（custom_tag 绿色，file/func 青色），内容使用级别颜色
            colored_message = (
                f"{Fore.GREEN}{custom_tag}{Style.RESET_ALL}"
                f"{Fore.CYAN}{file_name}{Style.RESET_ALL}"
                f"{Fore.CYAN}{func_name}{Style.RESET_ALL}"
                f"{level_color}{content}{Style.RESET_ALL}"
            )
        else:
            # 对于无预期前缀的消息（例如 autoadd=False），整体使用级别颜色
            colored_message = f"{level_color}{clean_message}{Style.RESET_ALL}"

        # 为日志级别名称应用级别颜色
        colored_level = f"{level_color}{record.levelname}{Style.RESET_ALL}"

        # 更新记录并调用父类格式化
        record.message = colored_message
        record.levelname = colored_level
        return super().formatMessage(record)
    

class IgnoreFilter(logging.Filter):
    """IgnoreFilter"""

    def filter(self, record):
        return record.name not in ("PIL.PngImagePlugin", "easyprocess")

