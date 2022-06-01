"""
Author: dp24/DLBPointon
"""
from email.mime import base
import os
import sys

def file_parse(in_file):
    """
    Desc: Opens input file and pulls out strings beginning with T (for consistency)
    Returns: List of T starting kmers, list of respective counts of kmer (not currently in use)
    """
    list_of_T = []
    counts_of_T = []
    with open(in_file) as input:
        for line in input:
            if line.startswith('T'):
                list_of_T.append(line.split("_")[0])
                counts_of_T.append(line.split("\t")[-1])

    return list_of_T, counts_of_T


def check_lists(kmer_l, count_l):
    """
    Desc: Takes kmer list and creates a new list of 1 kmer per size of kmer.
    Returns: final list of unique k-mer of size x
    """
    final_kmer = []
    len_count = []
    for i in kmer_l:
        if len(final_kmer) == 0:
            final_kmer.append(i)
            len_count.append(len(i))
        elif not len(i) in len_count:
            len_count.append(len(i))
            final_kmer.append(i)
        else:
            pass
    return final_kmer


def file_new(file_base, tolid, text):
    with open(f"{tolid}_{file_base}.txt", 'w') as nfile:
        nfile.write(text)


def main():
    """
    Desc: Main logic control
    Returns: Final string for jira push
    """
    kmer_type = ''

    tolid = sys.argv[2]
    file_name = os.path.basename(sys.argv[1])
    base_name = os.path.splitext(file_name)[0]
    print(base_name)
    if base_name.startswith('can'):
        kmer_type = '!'
    elif base_name.startswith('non'):
        kmer_type = '?'
    else:
        kmer_type = "~"

    list_of_T, counts_of_T = file_parse(sys.argv[1])
    kmer_list = check_lists(list_of_T, counts_of_T)
    if len(kmer_list) == 0:
        kmer_list.append('!')

    kmer_string = ','.join(kmer_list)
    kmer_data = f'{kmer_type} - {kmer_string}'
    file_new(base_name, tolid, kmer_data)


if __name__ == '__main__':
	main()