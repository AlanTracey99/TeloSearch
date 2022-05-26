process cat_all {
    //publishDir "./", mode: 'move'

    input:
    path(x)

    output:
    path ("total_kmer_counts.txt"), emit: total_kmer_counts

    script:
    """
    cat $x > total_kmer_counts.txt
    """
}
