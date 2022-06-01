process jira_push {
    // Sets the HTTPS PROXY env required for the API call to occur inside the job environment.

    input:
    tuple path(file1), path(file2)
    val(jira_id)
    path(envs_file)

    script:
    """
    printf ' & ' | cat $file1 - $file2 > intermediate.txt
    python $baseDir/scripts/jira_telo_push.py $jira_id intermediate.txt $envs_file
    """
}