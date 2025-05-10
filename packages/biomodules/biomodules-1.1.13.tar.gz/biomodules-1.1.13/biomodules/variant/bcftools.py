# -*- coding: utf-8 -*-
from okmodule import Flag, Option, Argument, Command


class BcftoolsIndex(Command):
    """bcftools index.

    bcftools (https://github.com/samtools/bcftools) need to be installed.

    Args:
        force: Overwrite index if it already exists.
        threads: Use multithreading with INT worker threads.
        vcf: The VCF file.
    """
    force = Flag('-f')
    threads = Option('--threads')
    vcf = Argument()



class BcftoolsConsensus(Command):
    """bcftools consensus.

    bcftools (https://github.com/samtools/bcftools) need to be installed.

    Args:
        fasta_ref: Reference sequence in fasta format.
        mask: Replace regions according to the mask_with option.
        mask_with: Replace with CHAR (skips overlapping variants); change to uppercase (uc) or lowercase (lc).
        output: Write output to a file.
        vcf: The VCF file.
    """
    fasta_ref = Option('-f')
    mask = Option('-m')
    mask_with = Option('--mask-with')
    output = Option('-o')
    vcf = Argument()
