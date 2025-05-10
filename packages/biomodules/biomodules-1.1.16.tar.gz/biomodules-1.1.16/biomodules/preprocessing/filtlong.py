# -*- coding: utf-8 -*-
from okmodule import Argument, Option, Command


class Filtlong(Command):
    """使用Filtlong过滤reads。

    使用该模块需要安装Filtlong（https://github.com/rrwick/Filtlong）。
    
    Args:
        min_length: 最小read长度
        min_mean_q: 最小read平均质量值
        input_reads: 输入reads文件路径
    """
    min_length = Option('--min_length')
    min_mean_q = Option('--min_mean_q')
    input_reads = Argument()
