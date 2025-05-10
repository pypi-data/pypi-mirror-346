# -*- coding: utf-8 -*-
from Bio import SeqIO
from okmodule import Module


class SubSeq(Module):
    """从一个完整的fasta文件中提取部分序列

    Args:
         infile: 完整的fasta文件
            ids: 需要提取的序列编号
        outfile: 输出文件
          extra: 额外内容，像提取的序列文件写入额外信息
    """
    def __init__(self, infile, ids, outfile, extra=None):
        self.infile = infile
        if isinstance(ids, list):
            ids = set(ids)
        self.ids = ids
        self.outfile = outfile
        self.extra = extra

    def main(self):
        with open(self.outfile, 'w') as fp:
            count = 0
            total = len(self.ids)
            for seq in SeqIO.parse(self.infile, 'fasta'):
                if seq.id not in self.ids:
                    continue
                count += 1
                fp.write(seq.format('fasta'))
                if count == total:
                    break
            if self.extra is not None:
                fp.write(self.extra)
