process jira_push {
    input:
    tuple val(telo_type), val(telo_kmer)
    val(jira_id)

    script:
    """
    if [[ ${telo_kmer} != "NULL" ]];then
        python $baseDir/scripts/jira_telo_push.py $jira_id $telo_type $telo_kmer
    else 
        echo "Problematic Tuple ( val( $telo_type ) val( $telo_kmer )  )"
    fi
    """
}