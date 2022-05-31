process cat_all {
    publishDir "./output/$id", mode: 'copy'

    input:
    path(x)
    val(id)

    output:
    path ("total_kmer_counts.txt"), emit: total_kmer_counts

    script:
    """
    cat $x >> total_kmer_counts.txt
    """
}
