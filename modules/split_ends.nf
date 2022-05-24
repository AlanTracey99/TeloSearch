process split_ends {
	cpus 1
	queue 'normal'
	executor 'lsf'
    
	input:
	path(fasta)
	val(ends)
	
	output:
	path("scaff*.fa"), emit: scaff
	
	script:
    """
    python /nfs/team135/alt/curation/telo/nf/split_ends.py $fasta --size $ends
    """
}