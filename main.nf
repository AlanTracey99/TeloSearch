nextflow.enable.dsl=2

include { split_ends } from "./modules/split_ends.nf"
include { jellycount } from "./modules/jellycount.nf"
include { jellydump } from "./modules/jellydump.nf"
include { cat_all } from "./modules/cat.nf"

kmers = params.klo..params.khi

log.info """\
	T E L O - N F   P I P E L I N E    
	================================

	fasta:      ${params.fasta}
	ends:       ${params.ends}
	kmers:      ${kmers}
    publishDir: ${param.save_dir}
	Top and tailing input fasta...
	"""

workflow top_tail {

    //
    // SPLIT_ENDS TO GET END OF SCAFFOLDS
    //
    split_ends ( params.fasta, params.ends )

    // Comvverts [file, file, file] + [2, 4, 6] to 
    // [[2, file1], [2, file2], [2, file3], [4, file1], [4, file2]....]

    ind_scaff = split_ends.out.scaff.view()
    kmer_ch = Channel.from(kmers).combine(ind_scaff.flatten()).view()

    //
    // JELLYFISH FOR KMER COUNTING ON SCAFF ENDS
    //
    jellycount ( kmer_ch )
    jellycount.out.jf_ch.collect().view()


    
    //
    // JELLYFISH DUMP TO GET THE COUNTS
    //
    // dsl2 allows a channel to be used more than once
    jf_counts = jellycount.out.jf_ch	// get output from jfish count channel
    jellydump ( jf_counts )
    jellydump.out.jf_final_out.collect().view()
    
    cat_all ( jellydump.out.jf_final_out.collect())

}
