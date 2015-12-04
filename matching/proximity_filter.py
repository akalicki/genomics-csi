"""
Usage: (python) proximity_filter.py <input_snps> <output_file>

Take a list of input SNPs, exclude variants that are close to each other and
output the resulting list of filtered SNPs.
"""
import sys

REQUIRED_GAP = 20000

def filter_variants(input_snps, output_file):
    """Write header and filtered SNPs from input_snps to output_file"""
    line = input_snps.readline()
    while line[0] == '#':  # read past header lines
        output_file.write(line)
        line = input_snps.readline()
    
    [rsid, chrom, pos, geno] = line.split('\t')
    last_chrom = chrom
    last_pos = int(pos)
    output_file.write(line)

    for line in input_snps:
        [rsid, chrom, pos, geno] = line.split('\t')
        if chrom != last_chrom or int(pos) - last_pos > REQUIRED_GAP:
            output_file.write(line)
            last_pos = int(pos)
            last_chrom = chrom

if __name__ == '__main__':
    with open(sys.argv[1]) as input_snps, open(sys.argv[2], 'w') as output_file:
        filter_variants(input_snps, output_file)