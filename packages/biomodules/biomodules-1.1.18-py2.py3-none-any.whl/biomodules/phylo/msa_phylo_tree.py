# -*- coding: utf-8 -*-
from pathlib import Path

from okmodule import Module

from biomodules.align.muscle import Muscle
from biomodules.phylo.iqtree import IQTree


class MSAPhyloTree(Module):
    """使用多序列比对构建进化树

    多序列比对结果文件和树文件均保存在序列文件同级目录，
    例如，输入文件为/path/to/myseqs.fasta，那么：
    多序列比对文件路径为：/path/to/myseqs.aligned.fasta，
    树文件路径为：/path/to/myseqs.treefile
    
    Args:
        seqs_file: 序列文件
        threads: 线程数，默认为4
    """
    def __init__(self, seqs_file, threads=4):
        if isinstance(seqs_file, str):
            seqs_file = Path(seqs_file)
        self.seqs_file = seqs_file
        self.threads = threads

    def main(self):
        basedir = self.seqs_file.parent
        stem = self.seqs_file.stem
        suffix = self.seqs_file.suffix
        aligned_file = basedir / f'{stem}.aligned{suffix}'
        prefix = str(basedir / stem)
        treefile = basedir / f'{stem}.treefile'
        Muscle(
            align=self.seqs_file,
            threads=self.threads,
            output=aligned_file
        )()
        IQTree(
            alignment_file=aligned_file,
            prefix=prefix,
            quiet=True,
            threads=self.threads
        )()
        return aligned_file, treefile
