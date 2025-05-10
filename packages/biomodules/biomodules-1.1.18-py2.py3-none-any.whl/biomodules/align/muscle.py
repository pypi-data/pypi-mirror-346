# -*- coding: utf-8 -*-
from okmodule import Option, Command


class Muscle(Command):
    """使用muscle进行多序列比对
    
    使用该模型需要安装muscle（https://github.com/rcedgar/muscle）

    Args:
        align: 需要比对的FASTA文件
        threads: 线程数
        output: 输出文件
    """
    align = Option('-align')
    threads = Option('-threads')
    output = Option('-output')
