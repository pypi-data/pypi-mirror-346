# -*- coding: utf-8 -*-
from pathlib import Path
from shutil import copyfileobj

from okmodule import Module


class MergeDir(Module):
    """给定一个输入文件夹和一个输出文件，把该文件夹下的所有文件合并到该文件中。

    Args:
        indir: <pathlib.Path>，输入文件夹
        outfile: <pathlib.Path>，输出文件
    """
    def __init__(self, indir, outfile):
        if isinstance(indir, str):
            indir = Path(indir)
        self.indir = indir
        if isinstance(outfile, str):
            outfile = Path(outfile)
        self.outfile = outfile

    def main(self):
        with self.outfile.open('wb') as ofp:
            for infile in self.indir.iterdir():
                if infile.is_dir() or infile.name.startswith('.'):
                    continue
                with open(infile, 'rb') as ifp:
                    copyfileobj(ifp, ofp)
