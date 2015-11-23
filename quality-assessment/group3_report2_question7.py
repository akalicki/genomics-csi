#!/usr/bin/env python
"""
Usage:
    samtools mpileup --max-depth 8000 <aln.bam> -f <ref.fasta> |
    python group3_report2_question1.py

<aln.bam> should be an (indexed) alignment file and <ref.fasta> the (indexed)
human genome reference sequence.

Reads a BAM alignment file as processed by BWA and poretools, and compares it to
the reference sequence to filter matches, insertions, and mismatches to build a
confusion matrix.
"""
import sys
from collections import defaultdict

def get_confusion(f):
    """Get confusion matrix from mileup output"""
    confusion = defaultdict(int)
    for line in f:
        info = line.split('\t')
        ref_base = info[2]
        read_bases = info[4]
        add_dict = get_new_entries(ref_base, read_bases)
        for key in add_dict:
            confusion[key] += add_dict[key]
        print confusion
    return confusion

bases = ['A','C','G','T']
def get_new_entries(ref_base, read_bases):
    """Return matching, mismatching, and indels for given base strings"""
    ref_base = ref_base.upper()
    entries = defaultdict(int)

    i = 0
    while i < len(read_bases):
        char = read_bases[i].upper()
        if char in ['.', ',']:    # match
            entries[(ref_base, ref_base)] += 1
        elif char in bases:       # mismatch
            entries[(ref_base, char)] += 1
        elif char in ['+', '-']:  # indel
            num_indels = int(read_bases[i + 1])
            for j in range(num_indels):
                indel = read_bases[i + j + 2].upper()
                if indel not in bases:
                    continue
                if char == '+':   # insertion
                    entries[('-', indel)] += 1
                else:             # deletion
                    entries[(indel, '-')] += 1
            i += num_indels + 2
            continue
        i += 1
    return entries

if __name__ == '__main__':
    confusion = get_confusion(sys.stdin)
    print(confusion)
