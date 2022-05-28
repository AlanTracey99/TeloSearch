process	results	{
	cpus 1
	
	input:
	path(total_kmer_counts)
	path(ends_fa)
	
	output:
	tuple val("CAN"), path("canonical.txt"), emit: can
	tuple val("NONCAN"), path("non_canonical.txt"), emit: noncan
	
	script:
	"""
	python $baseDir/scripts/results.py $total_kmer_counts $ends_fa
	"""
}
