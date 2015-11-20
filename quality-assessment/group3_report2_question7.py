#!/usr/bin/env python
"""
Usage: (python) group3_report2_question1.py <ref.fasta> <align.sam>

<aln.sam> should be an (indexed) alignment file and <ref.fasta> the (indexed)
human genome reference sequence.

Reads an SAM alignment file as processed by BWA, and compares it to the
reference sequence to filter matches, insertions, and mismatches to build a
confusion matrix. Note that samtools is unable to find deletions using this
method.
"""
import sys
from collections import defaultdict
from pysam import AlignmentFile
from pyfaidx import Fasta

bases = ['A','C','G','T','-']
def get_confusion(ref, align):
    """Get confusion matrix from reference sequence and alignment"""
    confusion = defaultdict(int)
    i = 0
    for column in align.pileup():
        print i
        i = i + 1
        for pileup_read in column.pileups:
            for chrom in ref.keys():
                ref_base = str(ref[chrom][column.pos : column.pos + 1])
                if pileup_read.indel != 0: 
                    # positive insertion, negative deletion
                    # skip indels for now
                    continue
                
                query_pos = pileup_read.query_position
                if query_pos is None:
                    continue
                
                query_base = str(pileup_read.alignment.query_sequence[query_pos])
                key = (query_base.upper(), ref_base.upper())
                if (key[0] not in bases or key[1] not in bases):
                    continue
                confusion[key] += 1
    return confusion

if __name__ == '__main__':
    ref = Fasta(sys.argv[1])
    align = AlignmentFile(sys.argv[2])
    confusion = get_confusion(ref, align)
    print confusion
    align.close()
