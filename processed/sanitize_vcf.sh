#!/bin/bash

for vcf_file in chr/vcf/*.vcf; do
    cat $vcf_file \
        | sed 's/VCFv4.2/VCFv4.1/' \
        | sed 's/,Version=3>/>/' \
        | sed 's/,Version=\"3\">/>/' \
        | sed 's/Number=R/Number=./' > $vcf_file
    bgzip $vcf_file
done

exit 0
