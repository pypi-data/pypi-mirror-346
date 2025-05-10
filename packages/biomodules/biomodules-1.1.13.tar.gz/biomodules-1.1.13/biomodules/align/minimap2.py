# -*- coding: utf-8 -*-
from okmodule import Option, Flag, Argument, Command


class Minimap2(Command):
    """使用minimap2进行序列比对。

    使用该模块需要安装minimap2（https://github.com/lh3/minimap2）。

    Args:
        sam: output in the SAM format (PAF by default)
        preset: - lr:hq - accurate long reads (error rate <1%) against a reference genome
                - splice/splice:hq - spliced alignment for long reads/accurate long reads
                - asm5/asm10/asm20 - asm-to-ref mapping, for ~0.1/1/5% sequence divergence
                - sr - short reads against a reference
                - map-pb/map-hifi/map-ont/map-iclr - CLR/HiFi/Nanopore/ICLR vs reference mapping
                - ava-pb/ava-ont - PacBio CLR/Nanopore read overlap
        threads: number of threads
        output: output alignments to FILE
        target: target file or index
        query: query file
    """
    sam = Flag('-a')
    preset = Option('-x')
    threads = Option('-t')
    output = Option('-o')
    target = Argument()
    query = Argument()
