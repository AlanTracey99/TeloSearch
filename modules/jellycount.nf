process jellycount {
	cpus 1

	input:
	tuple val(kmer), path(scaff)
    
	output:
	path("$kmer.${scaff.baseName}.jf"), emit: jf_files

    """
    echo $scaff
    jellyfish count -L 3 -m $kmer -s 100000 $scaff -o $kmer.${scaff.baseName}.jf
    """
}
