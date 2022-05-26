process	results	{
	cpus 1
	publishDir "./output", mode: "move", overwrite: true
	
	input:
	path(total_kmer_counts)
	path(ends_fa)
	
	output:
	path("canonical.txt"), emit: can
	path("non_canonical.txt"), emit: noncan
	
	script:
	"""
	python $baseDir/results.py $total_kmer_counts $ends_fa
	"""
}
