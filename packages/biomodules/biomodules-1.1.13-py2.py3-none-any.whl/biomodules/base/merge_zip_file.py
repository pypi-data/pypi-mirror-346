# -*- coding: utf-8 -*-
from pathlib import Path
from zipfile import ZipFile
from os.path import basename
from shutil import copyfileobj

from okmodule import Module


class MergeZipFile(Module):
    """给定一个zip文件，将该zip文件下的所有文件合并为一个文件

    infile: <pathlib.Path>，zip文件
    outfile: <pathlib.Path>，输出文件
    """
    def __init__(self, infile, outfile):
        if isinstance(infile, str):
            infile = Path(infile)
        self.infile = infile
        if isinstance(outfile, str):
            outfile = Path(outfile)
        self.outfile = outfile

    def main(self):
        with ZipFile(self.infile, 'r') as zip_file, self.outfile.open('wb') as ofp:
            for info in zip_file.infolist():
                if info.is_dir() or basename(info.filename).startswith('.'):
                    continue
                with zip_file.open(info, 'r') as ifp:
                    copyfileobj(ifp, ofp)
