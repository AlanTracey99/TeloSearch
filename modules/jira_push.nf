process jira_push {
    input:
    tuple val(telo_type), val(telo_kmer)
    val(jira_id)

    script:
    """
    python $baseDir/scripts/jira_telo_push.py $jira_id $telo_type $telo_kmer
    """
}