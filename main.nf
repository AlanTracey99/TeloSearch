nextflow.enable.dsl=2

include { split_ends } from "./modules/split_ends.nf"
include { jellycount } from "./modules/jellycount.nf"
include { jellydump } from "./modules/jellydump.nf"
include { cat_all } from "./modules/cat.nf"
include { results } from "./modules/results.nf"
include { parse_results } from "./modules/parse_results.nf"
include { cat_results } from "./modules/cat_results.nf"
include { find_telomere } from "./modules/find_telomere.nf"
// include { jira_push } from "./modules/jira_push.nf"



kmers = params.klo..params.khi

log.info """\
	T E L O - N F   P I P E L I N E    
	================================

    TolID: ${params.tolid}
    JiraID: ${params.jiraid}
	fasta: ${params.fasta}
	ends:  ${params.ends}
	size:  ${params.size}
	kmers: ${kmers}
	Pull out putative telomeric sequence for further analysis.
	"""

workflow top_tail {

    //
    // SPLIT_ENDS TO GET END OF SCAFFOLDS
    //
    split_ends ( params.fasta, params.ends, params.size )

    // Converts [file, file, file] + [2, 4, 6] to 
    // [[2, file1], [2, file2], [2, file3], [4, file1], [4, file2]....]
    ind_scaff = split_ends.out.scaff
    ends_fa = split_ends.out.ends_fa
    kmer_ch = Channel.from(kmers).combine(ind_scaff.flatten())

    //
    // JELLYFISH FOR KMER COUNTING ON SCAFF ENDS
    //
    jellycount ( kmer_ch )
    
    //
    // JELLYFISH DUMP TO GET THE COUNTS
    //
    // dsl2 allows a channel to be used more than once
    jellydump ( jellycount.out.jf_ch )
    
    //
    // CONCATENATE THE COUNTS
    //
    cat_all ( jellydump.out.jf_final_out.collect(), params.tolid)
    
    //
    // PYTHON RESULTS_INTER.PY TO GET TELOMERE MOTIF
    //
    results ( cat_all.out.total_kmer_counts, split_ends.out.ends_fa, params.tolid )
    results_ch = results.out.can.concat(results.out.noncan)
    //
    // PARSE RESULTS, CONVERT RESULTS INTO FORMAT FOR JIRA_PUSH
    //
    parse_results ( results_ch, params.tolid )
    
    //
    // CAT_RESULTS TAKES THE MULTIPLE PARSED RESULTS ADD APPENDS TO ONE FILE
    //
    cat_results ( parse_results.out.parsed.collect(), params.tolid )
    seq_ch = cat_results.out.seq_results.collect().view()

    //
    // USE THE FIND_TELOMERE.SHELL TO OUTPUT THE NEEDED .WINDOWS FILE
    //
    find_telomere ( cat_results.out.cat_results, params.fasta, params.tolid )

    //
    // JIRA_PUSH ENTERS THE RESULTS OF PULL_TELO INTO ASSOCIATED JIRA TICKET
    //
    //jira_push (cat_results.out.cat_results, params.jiraid, params.python_env)

}
