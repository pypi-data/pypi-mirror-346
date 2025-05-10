# -*- coding: utf-8 -*-
from okmodule import Option, Command


class Blastn(Command):
    """使用blastn进行序列比对。
    
    Args:
        db: BLAST database name
        query: Input file name
        out: Output file name
        evalue: Expectation value (E) threshold for saving hits. Default = 10 (1000 for blastn-short)
        max_hsps: Set maximum number of HSPs per subject sequence to save for each query
        outfmt: alignment view options:
            0 = Pairwise,
            1 = Query-anchored showing identities,
            2 = Query-anchored no identities,
            3 = Flat query-anchored showing identities,
            4 = Flat query-anchored no identities,
            5 = BLAST XML,
            6 = Tabular,
            7 = Tabular with comment lines,
            8 = Seqalign (Text ASN.1),
            9 = Seqalign (Binary ASN.1),
            10 = Comma-separated values,
            11 = BLAST archive (ASN.1),
            12 = Seqalign (JSON),
            13 = Multiple-file BLAST JSON,
            14 = Multiple-file BLAST XML2,
            15 = Single-file BLAST JSON,
            16 = Single-file BLAST XML2,
            17 = Sequence Alignment/Map (SAM),
            18 = Organism Report
        num_alignments: Number of database sequences to show alignments for
        max_target_seqs: Maximum number of aligned sequences to keep
        num_threads: Number of threads (CPUs) to use in the BLAST search
    """
    db = Option('-db')
    query = Option('-query')
    out = Option('-out')
    evalue = Option('-evalue')
    max_hsps = Option('-max_hsps')
    outfmt = Option('-outfmt')
    num_alignments = Option('-num_alignments')
    max_target_seqs = Option('-max_target_seqs')
    num_threads = Option('-num_threads')
