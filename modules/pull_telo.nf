process pull_telo {
    input:
    tuple val(telo_type), path(file)

    output:
    tuple val(telo_type),
            env(telo_kmer_seq), emit: telo_data

    script:
    """
    sleep 10

    telo_kmer=\$(sed -n "2p" $file)
    telo_kmer_seq=`cut -f 2 -d ":" <<< \${telo_kmer}`

    if [ -z \${telo_kmer_seq} ]; then
        telo_kmer_seq="NULL";
    fi
    """
}