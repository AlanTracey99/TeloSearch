"""
kmer counter
By Damon-Lee Pointon (dp24)

Takes a concatenated list of jf_final_count files
and produces a dict of:
{kmer, [kmer_count, times found]}

"""

import sys

lines = {}
with open(sys.argv[0], 'r') as file:
    for line in file:
        kmer = line.split(" ")[0]
        kmer_count = int(line.split(" ")[1])
        if kmer in lines.keys():
            print(lines[kmer])
            lines[kmer][0] += kmer_count
            lines[kmer][1] += 1
        else:
            lines[kmer] = [kmer_count, 1]

print(lines)