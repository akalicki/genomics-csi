"""
Usage: (python) dbsnp_to_ids.py <dbsnp_matches.xml>

Counts all matches of rsids in <dbsnp_matches.xml> where the
submitter was either 1000GENOMES or HUMANGENOME_JCVI (Craig Venter).
Prints a list of the most likely matches.
"""
from collections import defaultdict
import operator
import sys
import xml.etree.cElementTree as etree

PREFIX = "{http://www.ncbi.nlm.nih.gov/SNP/docsum}"
HANDLE_CV = "HUMANGENOME_JCVI"
HANDLE_1000 = "1000GENOMES"

PILOT_1000 = "pilot_"
NA_1000 = "NA"

def get_snp_matches(xml_file):
    """Build a map of IDs to occurrences based off allele matches"""
    matches = defaultdict(int)

    tree = etree.parse(xml_file)
    root = tree.getroot()
    for rs in root.findall(PREFIX + "Rs"):
        rsid = rs.attrib["rsId"]
        for ss in rs.findall(PREFIX + "Ss"):
            handle = ss.attrib["handle"]
            if handle == HANDLE_CV:
                matches[HANDLE_CV] += 1
            elif handle == HANDLE_1000:
                snp_id = ss.attrib["locSnpId"]
                if snp_id.startswith(PILOT_1000):
                    snp_id = '_'.join([x for x in snp_id.split('_')[0:3]])
                    matches[snp_id] += 1
                elif snp_id.startswith(NA_1000):
                    snp_id = snp_id.split('_', 1)[0]
                    matches[snp_id] += 1
    return matches

if __name__ == '__main__':
    with open(sys.argv[1]) as xml_file:
        id_matches = get_snp_matches(xml_file)
        matches_sorted = sorted(id_matches.items(), key=operator.itemgetter(1), reverse=True)

        print "\n\nMATCH COUNTS:"
        print "----------------------------------------"
        for match in matches_sorted:
            print "%s\t%d" % (match[0], match[1])
