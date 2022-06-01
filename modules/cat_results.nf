process cat_results {
    input:
    tuple path(file1), path(file2)
    val (id)

    output:
    path("intermediate.txt"), emit: cat_results
    path('*.seq.txt'), emit: seq_results

    script:
    """
    printf ' & ' | cat $file1 - $file2 > intermediate.txt

    contents=`cat intermediate.txt | tr -d '!& '`

    if [[ "\$contents" == *","* ]]; then 
        IFS=,;
        for i in \$contents; do
            echo "\${i}" > \${i}.seq.txt ;
        done;
    else
        echo "\${contents}" > \${contents}.seq.txt
    fi

    """
}