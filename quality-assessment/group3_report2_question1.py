#!/usr/bin/env python
"""
Usage: (python) group3_report2_question1.py <PASS FILE> <FAIL FILE>
Reads a pair of input FASTQ file as processed by poretools and counts
the number of 2D reads that were found in each.
"""
import sys
import re


filename_re = re.compile(r"ch(\d+)_file(\d+)_strand_(.*):")


def parse_filename_line(s):
    """Returns a 3-tuple consisting of channel number, file number,
    and boolean flag true if 2D read"""
    matches = filename_re.search(s)
    if matches:
        channel_number = int(matches.group(1))
        file_number = int(matches.group(2))
        twodirections = (matches.group(3) == "twodirections")
        return (channel_number, file_number, twodirections)


def get_reads(f):
    """Creates a set of 2d reads found in f."""
    reads2d = set([])
    for line in f.readlines():
        if line[0] == '@':  # skip most irrelevant lines
            z = parse_filename_line(line)
            if z and z[2]:
                reads2d.add((z[0], z[1]))
    return reads2d

if __name__ == '__main__':
    with open(sys.argv[1]) as passfile, open(sys.argv[2]) as failfile:
        pass2d = get_reads(passfile)
        fail2d = get_reads(failfile)
        print ("Passed: %d 2D reads" % len(pass2d))
        print ("Failed: %d 2D reads" % len(fail2d))
