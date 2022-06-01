process parse_results {
    publishDir "./output/$id", mode: 'copy', overwrite: true
    
    input:
    tuple val(telo_type), path(file)
    val(id)

    output:
    path('*txt'), emit: parsed

    script:
    """
    python $baseDir/scripts/parse_results.py $file $id
    """
}