#!/bin/bash

for vcf_file in chr/vcf/*.vcf; do
    vcf_sanitized=${vcf_file/.vcf/.sanitized.vcf}
    cat $vcf_file \
        | sed 's/VCFv4.2/VCFv4.1/' \
        | sed 's/,Version=3>/>/' \
        | sed 's/,Version=\"3\">/>/' \
        | sed 's/Number=R/Number=./' > $vcf_sanitized
    bgzip $vcf_sanitized
    mv "$vcf_sanitized.gz" chr/vcf_sanitized
done

exit 0
