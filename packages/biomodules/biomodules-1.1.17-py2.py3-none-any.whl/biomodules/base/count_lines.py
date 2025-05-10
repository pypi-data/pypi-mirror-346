# -*- coding: utf-8 -*-
from okmodule import Module


class CountLines(Module):
    """给定一个文件计算其行数。
    
    Args:
        infile: <Path>，文件；
        comment_char: <str>，注释字符（以该字符开头的行将被忽略）；
    """
    def __init__(self, infile, comment_char=None):
        self.infile = infile
        self.comment_char = comment_char

    def main(self):
        if self.comment_char is None:
            return sum(1 for _ in open(self.infile))
        return sum(1 for _ in open(self.infile) if not _.startswith(self.comment_char))
