#!/bin/bash

# The standard find_telomere.sh script has been modified by 
# dp24 / Damon-Lee B Pointon

if [ -z $1 ]; then
	echo "Usage: ./find_telomere.sh <fasta>"
	exit -1
fi

export LD_LIBRARY_PATH=/usr/lib/jvm/java-11-openjdk-amd64/lib/:/usr/lib/gcc/x86_64-linux-gnu/7.4.0:${LD_LIBRARY_PATH}
export PATH=/software/badger/opt/gcc/7.1.0/bin:${PATH}
export VGP_PIPELINE=/software/grit/projects/vgp-assembly/pipeline/

file=$1
telomereSeq=$2
out_dir=$3
telo_type=$4
tolid=$5
file_name="${5}_${4}"

if [ ! -e $file_name ]; then
	ln -s $file
fi

file=$file_name
prefix=`echo ${file} | sed 's/.fasta$//g' | sed 's/.fa$//g'`


/nfs/team135/yy5/vgptools/vgp-assembly/pipeline/telomere/find_telomere $file $telomereSeq > $out_dir/$prefix.telomere
/usr/bin/java -Xms1g -Xmx1g -cp /software/grit/projects/vgp-assembly/pipeline/telomere/telomere.jar FindTelomereWindows $out_dir/$prefix.telomere 99.9 >$out_dir/$prefix.windows
cat $out_dir/$prefix.windows |awk '{if ($4 > 100000 && $3-$5 > 100000) print $0}'


