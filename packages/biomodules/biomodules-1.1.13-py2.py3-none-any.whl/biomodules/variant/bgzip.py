# -*- coding: utf-8 -*-
from okmodule import Flag, Option, Argument, Command


class Bgzip(Command):
    """bgzip.

    htslib (https://github.com/samtools/htslib) needs to be installed.

    Args:
        force: Overwrite files without asking.
        keep: Don't delete input files during operation.
        threads: Number of compression threads to use.
        file: The file
    """
    force = Flag('-f')
    keep = Flag('-k')
    threads = Option('-@')
    file = Argument()
