#!/usr/bin/env python3


'''
MIT License
 
Copyright (c) 2022 Genome Research Ltd.
 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



'''

import os
import sys
import re
import argparse
import pyfastaq
import subprocess
from subprocess import check_output
from datetime import datetime
from time import gmtime, strftime
from Bio import SeqIO
from Bio.Seq import Seq
from itertools import islice
import time





canonical=["TTAGG","TTGGG","TTGTGG","GAGCCTTGTTT","TCAGG","TTGCA", \
"TCTGGG","TTTGGATAGG","TTCGGG","ACTGGTGT","TTTAGGG","TGGGTC"]


def caprop(fasta):

    
    A_count=0
    C_count=0
    G_count=0
    T_count=0
    
    for base in fasta:
        b=base.upper()
        if b == 'A':
            A_count+=1
        elif b == 'C':
            C_count+=1
        elif b == 'G':
            G_count+=1
        elif b == 'T':
            T_count+=1

    ACGT=A_count+C_count+G_count+T_count
    C=C_count
    A=A_count
    cprop=(C/ACGT)*100
    aprop=(A/ACGT)*100
    maxprop=max([aprop,cprop])


    return maxprop


def rev_comp(dna):
    
    y=dna.upper()
    x=y.replace('A','t').replace('T','a').replace('C','g').replace('G','c')	 

    return x[::-1].upper()

def check_tandemness(candidate_kmers, fastafile):
    #for k,v in candidate_kmers.items():
        #print(k,v)

    tandMers=[]
    results=[]
    temp={}
    fastadict={}

    with open(fastafile,'r') as f:
        for line in f:
            if line[0]==">":
                k=line.strip().replace(">","")
                fastadict[k]=""
            else:
                fastadict[k]=line.strip().upper()	#ensure seq is upper case

    for k,v in candidate_kmers.items():
        t=k*50
        tandem_bases=30
        tt=t[:tandem_bases]+"-"+k	#taking a slice of our 50kmer artificial tandem probe	
        tandMers.append(tt)
                        
    for k,v in fastadict.items():
        #print(k,v)
        for tm in tandMers:
            t=tm.split("-")
            if caprop(t[0])>30:	#ensure telomeres are flipped towards TG composition rather than CA
                t=[rev_comp(t[0]),rev_comp(t[1])]
            #record number of matches of tandem-mer in temp
            #t[0]=tandem-mer
            #v.count tandem-mer is how many times it's found in that end
            hits=v.count(t[0])+rev_comp(v).count(t[0])
            if t[0] not in temp:
                temp[t[0]]=hits
            else:
                temp[t[0]]+=hits
                
    
                    
    #if matches of tandem-mer exceeds 10, it's unlikely to be simply seq-error				
    for k,v in temp.items():
        if v > 10:
            for tm in tandMers:
                if k==tm.split("-")[0]:
                    results.append(tm.split("-"))	
    
    check=[]
    check2=[]
    check3=[]
    removed=[]
    tandems={}
    tandemstring=""
    div=[2,3,5,7]
    for r in results:
        check.append(r)
    #removing kmers nested within longer kmers
    for r in results:
        for c in check:
            for d in div:
                if len(r[1])==len(c[1])/d and c[1].find(r[1]) != -1:
                    #print("( removed candidate: ",c,")\n")
                    removed.append(c)	
                elif c not in removed:
                    if c not in check2:
                        check2.append(c)
                        
    #checking we don't duplicate tandem-mers
    for c in check2:	
        if tandemstring=="":
            tandemstring=c[0]
            tandems[c[0]]=[]
        if c[0][8:22] not in tandemstring and rev_comp(c[0][8:22]) not in tandemstring:
            tandems[c[0]]=[]
            tandemstring+=c[0]

                
    for c in check2:
        for k,v in tandems.items():
            if c[1] in k:
                if c[1] not in v:
                    v.append(c[1])

    canonical_output=[]
    can=[]
    noncanonical_output=[]
    
    print("="*54)
    print("\n      ","R","E","S","U","L","T","S","\t", sep=" -- ")
    print()
    for k,v in tandems.items():
        m=len(min(v, key=len))
        for ca in canonical:
            if ca in k or rev_comp(ca) in k:
                canonical_output.append("="*54+"\n")
                line="LIKELY_TELO-REPEAT:\t"+k
                if line not in canonical_output:
                    canonical_output.append(line)
                can.append(k)
                for i in v:
                    khits=candidate_kmers[i][0]
                    kends=candidate_kmers[i][1]
                    if len(i) == m:
                        line1="telo_kmer:\t\t"+i
                        line2=i+"_count_at_ends:\t"+str(khits)
                        line3=i+"_scaff_ends_count:\t"+str(kends)
                        if line in canonical_output:
                            if line1 not in canonical_output:
                                canonical_output.append(line1)
                            if line2 not in canonical_output:	
                                canonical_output.append(line2)
                            if line3 not in canonical_output:
                                canonical_output.append(line3)
                    
                        
    noncanonical_output.append("\nOTHER_RESULTS:\n")				
    for k,v in tandems.items():
        m=len(min(v, key=len))
        if k not in can:
            noncanonical_output.append("-"*54+"\n")
            line="candidate_telo-repeat:\t"+k
            if line not in noncanonical_output:
                noncanonical_output.append(line)
            for i in v:
                khits=candidate_kmers[i][0]
                kends=candidate_kmers[i][1]
                if len(i) == m:
                    line1="candidate_telo_kmer:\t"+i
                    line2=i+"_count_at_ends:\t"+str(khits)
                    line3=i+"_scaff_ends_count:\t"+str(kends)
                    if line1 not in noncanonical_output:
                        noncanonical_output.append(line1)
                    if line2 not in noncanonical_output:	
                        noncanonical_output.append(line2)
                    if line3 not in noncanonical_output:	
                        noncanonical_output.append(line3)
                        
    

    ########### short block of code removes tandem-mers based on overly long kmers that
    #happen to occur in the sequence fasta due to errors, typically slurring of mono-runs
    #In testing, first tandem-mer is the high confidence one, 2nd one is the one with seq errors which we throw away
    s=[i for i, n in enumerate(canonical_output) if n == "="*54+"\n"]
    for i in s:
        if canonical_output[i-1][0:6]=="LIKELY":
            del(canonical_output[i-3:i])
    ###########						
                        
    with open("canonical.txt","w") as fout:
        if len(canonical_output)>0:
            for c in canonical_output:
                print(c)
                if not "====" in c:
                    fout.write(c+"\n")
        else:
            print("="*54+"\n")
            print("\nNo canonical telomere motif found\n")
    with open("non_canonical.txt","w") as fout:
        if len(noncanonical_output)>1:
            for n in noncanonical_output:
                print(n)
                if not "----" in n and not "====" in n:
                    fout.write(n+"\n")
        else:
            print("-"*54+"\n")
            print("\nNo non-canonical telomere motif found\n")



def process_counts(infile):

    lines = {}
    inter = {}
    final = {}
    with open(infile, 'r') as file:
        for line in file:
            kmer = line.split(" ")[0]
            kmer_count = int(line.split(" ")[1])
            if caprop(kmer)>30:

               kmer=rev_comp(kmer)
               if kmer in lines.keys():
                lines[kmer][0] += kmer_count
                lines[kmer][1] += 1		#a kmer occuring on another line must be from another scaff
            else:
                lines[kmer] = [kmer_count, 1]



    for k,v in lines.items():
        khits=v[0]
        kends=v[1]
        if khits >5 and kends >2:   
            final[k]=v


    #These are our telo candidate kmers before we check for tandem-ness

    return final



def main():
    
    print("""\n\n\nFinds most likely telomere motif in Hi-fi or equivalent quality assembly where telomeres \n
    are expected to occur at the ends of multiple scaffolds\n\n""")
    start_time = datetime.now()
    infile = sys.argv[1]
    endsfile = sys.argv[2]
    candidate_kmers = process_counts(infile)
    print("\nchecking tandemness of candidates...\n")
    check_tandemness(candidate_kmers, endsfile)
    end_time=datetime.now()
    print('\n\nFINISHED:\t{}'.format(end_time - start_time)+"\n\n")

if __name__ == '__main__':
    main()
