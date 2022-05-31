process find_telomere {
    publishDir "./output", mode: 'copy', overwrite: true

    input:
    tuple val( telo_type ), val( telo_kmer )
    path(fasta)
    val( species_id )

    output:
    tuple path("*telomere"), path("*windows"), emit: windows_telo

    script:
    """
    if [[ ${telo_kmer} = "NULL" ]];then
        echo "NULL" > NULL.telomere
        echo "NULL" > NULL.windows
    else
        $baseDir/scripts/find_telomere.sh $fasta $telo_kmer . $telo_type $species_id
    fi
    """
}