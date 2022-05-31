process jira_push {
    // Sets the HTTPS PROXY env required for the API call to occur inside the job environment.

    input:
    tuple val(telo_type), val(telo_kmer)
    val(jira_id)
    path(envs_file)

    script:
    """
    if [[ ${telo_kmer} != "NULL" ]];then
        python $baseDir/scripts/jira_telo_push.py $jira_id $telo_type $telo_kmer $envs_file
    else 
        echo "Problematic Tuple ( val( $telo_type ) val( $telo_kmer )  )"
    fi
    """
}