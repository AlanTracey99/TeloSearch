#!/bin/bash

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
file_name=`basename $file`

if [ ! -e $file_name ]; then
	ln -s $file
fi

file=$file_name
prefix=`echo $file | sed 's/.fasta$//g' | sed 's/.fa$//g'`


/nfs/team135/yy5/vgptools/vgp-assembly/pipeline/telomere/find_telomere $file $telomereSeq > $out_dir/$prefix.telomere
/usr/bin/java -Xms1g -Xmx1g -cp $VGP_PIPELINE/telomere/telomere.jar FindTelomereWindows $out_dir/$prefix.telomere 99.9 > $out_dir/$prefix.windows
cat $out_dir/$prefix.windows |awk '{if ($4 > 100000 && $3-$5 > 100000) print $0}'


