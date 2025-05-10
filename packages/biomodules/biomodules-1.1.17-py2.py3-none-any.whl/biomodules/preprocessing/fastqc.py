# -*- coding: utf-8 -*-
from okmodule import Argument, Option, Flag, Command


class Fastqc(Command):
    """使用fastqc进行质量控制。

    使用该模块需要安装fastqc（https://www.bioinformatics.babraham.ac.uk/projects/fastqc/）。

    Args:
        outdir: 输出路径
        threads: 线程数
        extract: 是否解压
        seqfile: 测序文件
    """
    outdir = Option('--outdir')
    threads = Option('--threads')
    extract = Flag('--extract')
    seqfile = Argument()
