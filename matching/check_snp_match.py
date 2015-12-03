"""
Usage: (python) check_snp_match.py <snp_file> <ref_snp_file>

Prints the number and percentage match of snp_file SNPS to ref_snp_file SNPS.
"""
import sys

def build_snp_map(ref_file):
    """Build a map of RSIDs to genotype strings"""
    ref_map = {}
    for line in ref_file:
        if line[0] == '#':  # skip header lines
            continue
        data = line.split('\t')
        rsid = data[0]
        genotype = data[3].rstrip()
        ref_map[rsid] = genotype
    return ref_map

def intersect_maps(snp_map, ref_map):
    """Return a map of all intersections of the snp_map and ref_map"""
    intersection = {}
    for rsid in snp_map:
        if rsid in ref_map:
            intersection[rsid] = snp_map[rsid]
    return intersection

if __name__ == '__main__':
    with open(sys.argv[1]) as snp_file, open(sys.argv[2]) as ref_file:
        snp_map = build_snp_map(snp_file)
        ref_map = build_snp_map(ref_file)
        intersection = intersect_maps(snp_map, ref_map)
        num_intersect = len(intersection)
        print('\n'.join(intersection))
        num_snps = len(snp_map)
        print "%d out of %d (%.2f%%) SNPs matched" \
            % (num_intersect, num_snps, num_intersect * 100.0 / num_snps)
