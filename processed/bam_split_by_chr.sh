#!/bin/bash
#usage   

SAMTOOLS=$1
BAM_INPUT=$2
PATH_OUTPUT=$3
BAMTOOLS=~/bio/app/bamtools/bin/bamtools/2.3.0/bamtools
#create the target directory
mkdir -p ${PATH_OUTPUT}

if [ -f $BAMTOOLS ];
then

 cd ${PATH_OUTPUT} && ~/bio/app/bamtools/bin/bamtools split -in ${BAM_INPUT} -refPrefix "" -reference
 for i in *.chr*bam 
 do 
  sampleName=${i%.bam}
  chrName=${sampleName#*.}
  ${SAMTOOLS} view -h -F 0x4 -q 10 ${i} | awk '{if(/^@SQ/ && !/^@SQ\tSN:'$chrName'/) next} {if(/^@/) print $0}{if ($3~/^'$chrName'/) print $0}' | ${SAMTOOLS} view -hbS - > ${PATH_OUTPUT}/${sampleName}.tmp
  mv ${PATH_OUTPUT}/${sampleName}.tmp ${PATH_OUTPUT}/${sampleName}.bam
 done
else
 fileName=$(basename "$BAM_INPUT")
 #extension="${fileName##*.}"
 sampleName="${fileName%.*}"
 #split the bam
 for i in `${SAMTOOLS} view -H ${BAM_INPUT} | awk -F"\t" '/@SQ/{print $2}' |  cut -d":" -f2`
 do
  ${SAMTOOLS} view -h -F 0x4 -q 10 ${BAM_INPUT} $i | awk '{if(/^@SQ/ && !/^@SQ\tSN:'$i'/) next} {if(/^@/) print $0}{if ($3~/^'$i'/) print $0}' | $1 view -hbS - > ${PATH_OUTPUT}/${sampleName}.$i.tmp
  mv ${PATH_OUTPUT}/${sampleName}.$i.tmp ${PATH_OUTPUT}/${sampleName}.$i.bam
 done
fi
