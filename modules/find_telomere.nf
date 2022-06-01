process find_telomere {
    publishDir "./output/$id", mode: 'copy', overwrite: true

    input:
    path(telomere)
    path(fasta)
    val( id )

    output:
    tuple path("$id*.telomere"), path("$id*.windows"), emit: windows_telo

    script:
    """
    telo_kmer=`cat $telomere | tr -d '!& '`
    $baseDir/scripts/find_telomere.sh $fasta \$telo_kmer ./
    """
}