process split_ends {
	cpus 1
    
	input:
	path(fasta)
	val(ends)
	
	output:
	path("scaff*.fa"), emit: scaff
	path("ends.fa"), emit: ends_fa
	
	script:
    """
    python $baseDir/split_ends.py $fasta --size $ends
    """
}
