# -*- coding: utf-8 -*-
import gzip

from okmodule import Module


class Fastq2Fasta(Module):
    """fastq转fasta。
    
    Args:
        fastq: <pathlib.Path>，fastq文件路径
        fasta: <pathlib.Path>，fasta文件路径
    """
    def __init__(self, fastq, fasta):
        self.fastq = fastq
        self.fasta = fasta

    def _open_fastq(self):
        if self.fastq.suffix == '.gz':
            return gzip.open(self.fastq, 'rt')
        return self.fastq.open('r')

    def main(self):
        fastq_fp = self._open_fastq()
        fasta_fp = self.fasta.open('w')
        try:
            while True:
                header = fastq_fp.readline()
                sequence = fastq_fp.readline()
                fastq_fp.readline()
                fastq_fp.readline()
                if not header:
                    break
                if header[0] != '@':
                    continue
                fasta_fp.write(f'>{header[1:]}{sequence}')
        finally:
            fastq_fp.close()
            fasta_fp.close()
