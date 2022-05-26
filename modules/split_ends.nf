process split_ends {
	cpus 1
    
	input:
	path(fasta)
	val(ends)
	val(size)
	
	output:
	path("*.fa"), emit: scaff
	path("ends.fasta"), emit: ends_fa
	
	script:
    """
    python $baseDir/split_ends.py $fasta --size $size  --ends $ends
    """
}
