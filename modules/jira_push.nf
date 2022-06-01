process jira_push {
    input:
    path(intermediate)
    val(jira_id)
    path(envs_file)

    script:
    """
    python $baseDir/scripts/jira_telo_push.py $jira_id $intermediate $envs_file
    """
}