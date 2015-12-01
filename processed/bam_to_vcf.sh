#!/bin/bash

REF_FASTA=$1

for bam_file in chr/bam/*.bam; do
    raw_file=${bam_file/mapped.baq./}
    raw_file=${raw_file/.bam/.raw.vcf}
    filt_file=${raw_file/.raw/.filt}
    samtools mpileup -C50 -uf $REF_FASTA $bam_file | bcftools call -mv > $raw_file
    bcftools filter -s LowQual -e '%QUAL<20 || DP>100' $raw_file > $filt_file
    mv $filt_file chr/vcf
    rm -f raw_file
done

exit 0