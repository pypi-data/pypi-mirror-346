# -*- coding: utf-8 -*-
from okmodule import Option, Flag, Command


class IQTree(Command):
    """使用iqtree构建进化树

    使用本模块需要安装iqtree3（https://iqtree.github.io）

    Args:
        alignment_file: PHYLIP/FASTA/NEXUS/CLUSTAL/MSF alignment file(s)
        model: Model name
        prefix: Prefix for all output files
        quiet: Quiet mode, suppress printing to screen
        threads: No. cores/threads or AUTO-detect (default: 1)
    """
    alignment_file = Option('-s')
    model = Option('-m')
    prefix = Option('--prefix')
    quiet = Flag('--quiet')
    threads = Option('-T')

    def path(self):
        return ['iqtree']
