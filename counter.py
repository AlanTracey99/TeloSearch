"""
kmer counter
By Damon-Lee Pointon (dp24)

Takes a concatenated list of jf_final_count files
and produces a dict of:
{kmer, [kmer_count, times found]}

"""

import sys

lines = {}
results = {}
with open(sys.argv[1], 'r') as file:
    for line in file:
        kmer = line.split(" ")[0]
        kmer_count = int(line.split(" ")[1])
        if kmer in lines.keys():
            lines[kmer][0] += kmer_count
            lines[kmer][1] += 1
        else:
            lines[kmer] = [kmer_count, 1]

for k,v in lines.items():
    if v[0]>5 and v[1]>2:
        results[k]=v
        