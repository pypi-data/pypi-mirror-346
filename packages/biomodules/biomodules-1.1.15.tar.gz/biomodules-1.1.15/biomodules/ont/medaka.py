# -*- coding: utf-8 -*-
from okmodule import Option, Argument, Command


class MedakaInference(Command):
    """使用medaka inference call突变。

    Args:
        model: Model to use
        threads: Number of threads used by inference
        bam: Input alignments
        output: Output file
    """
    model = Option('--model')
    threads = Option('--threads')
    bam = Argument()
    output = Argument()


class MedakaVcf(Command):
    """使用medaka vcf生成VCF文件。
    
    Args:
        input: Consensus .hdf files
        ref_fasta: Reference sequence .fasta file
        output: Output .vcf
    """
    input = Argument()
    ref_fasta = Argument()
    output = Argument()
