# -*- coding: utf-8 -*-
from okmodule import Module


class LowDepth(Module):
    """从samtools depth生成的文件中提取出深度较低的位点。
    
    Args：
        depth_file: samtools depth生成的位点深度文件
        min_depth: 最小深度
        low_depth_file: 低深度位点结果文件
    """
    def __init__(self, depth_file, min_depth, low_depth_file):
        self.depth_file = depth_file
        self.min_depth = min_depth
        self.low_depth_file = low_depth_file

    def main(self):
        with self.depth_file.open() as ifp, self.low_depth_file.open('w') as ofp:
            for line in ifp:
                chrom, pos, depth = line.rstrip().split('\t')
                if int(depth) < self.min_depth:
                    ofp.write(f'{chrom}\t{pos}\n')
