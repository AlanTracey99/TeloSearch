process jellydump {
    cpus 1
    
    input:
    path( x )
    
    output:
    path( "${x}_final_counts" ), emit: jf_final_out
    
    script:
    """
    jellyfish dump -c $x | sort -k2,2n > ${x}_final_counts
    """
    
}

// was getting error just pointing to the curly braces - fix for this was to remove % function from process



