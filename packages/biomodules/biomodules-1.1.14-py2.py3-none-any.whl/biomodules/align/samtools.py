# -*- coding: utf-8 -*-
from okmodule import Flag, Option, Argument, Command


class SamtoolsView(Command):
    """使用samtools view处理sam/bam文件。

    需要安装samtools（https://github.com/samtools/samtools）。

    Args:
        bam: Output BAM
        min_mq: Only include in output reads that have mapping quality >= INT
        threads: Number of additional threads to use
        output: Write output to file
        input: Input bam or sam file
    """
    bam = Flag('-b')
    min_mq = Option('-q')
    threads = Option('-@')
    output = Option('-o')
    input = Argument()


class SamtoolsSort(Command):
    """使用samtools sort对bam文件进行排序。

    需要安装samtools（https://github.com/samtools/samtools）。

    Args:
        threads: Number of additional threads to use
        output: Write output to file
        input: Input bam file
    """
    threads = Option('-@')
    output = Option('-o')
    input = Argument()


class SamtoolsIndex(Command):
    """使用samtools index对bam文件生成索引。

    需要安装samtools（https://github.com/samtools/samtools）。

    Args:
        threads: Sets the number of threads
        output: Write index to FILE [alternative to <out.index> in args]
        input: Input bam file
    """
    threads = Option('-@')
    output = Option('-o')
    input = Argument()


class SamtoolsDepth(Command):
    """使用samtools depth计算位点深度。

    需要安装samtools（https://github.com/samtools/samtools）。

    Args:
        all: Output all positions (including zero depth)
        threads: Number of additional threads to use
        output: Write output to FILE
        input: Input bam file
    """
    all_positions = Flag('-a')
    threads = Option('-@')
    output = Option('-o')
    input = Argument()
