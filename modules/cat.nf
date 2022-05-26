process cat_all {

    input:
    path(x)

    output:
    path ("total_kmer_counts.txt"), emit: total_kmer_counts

    script:
    """
    cat $x >> total_kmer_counts.txt
    """
}
