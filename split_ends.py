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


import sys
from datetime import datetime
import subprocess
from subprocess import check_output
import argparse
import pyfastaq
from Bio import SeqIO
from Bio.Seq import Seq
from itertools import islice
import time


def location(f):

	cmd="readlink -f "+f
	b=subprocess.getoutput(cmd)
	
	return b
	
def top_and_tail(fastafile, size):

	pyfastaq.utils.syscall("rm -rf ends.fa")
	with open("ends.fa", 'w') as fout:
		for seq_record in SeqIO.parse(fastafile, "fasta"):
			scflen=len(seq_record.seq)
			s=int(size)+1
			sq1=seq_record.seq[0:s]
			sq2=seq_record.seq[scflen-s:scflen]
			fout.write('>'+seq_record.id+'L\n'+str(sq1)+"L\n"+'>'+seq_record.id+'R\n'+str(sq2)+"\n")
	#Below method rejected on grounds that line lengths may be 200mb and not necessarily 60bp!		
	#cmd="grep -A"+size+" -B"+size+" '>' "+fastafile+" > ends.fa"
	
def process_fasta(fasta, num):

	results={}
	final={}
	ends=[]
	with open(fasta,'r') as f:
		for line in f:
			x=line.strip().split()
			if x!=[]:
				if x[0][0]==">":
					header=x[0].replace(">","")[:-1]
					if header not in results:
						results[header]=[[],[]]
				elif results[header]==[[],[]]:
					results[header][0]=x
				elif results[header][0]!=[]:
					results[header][1]=x
					
					
				

					
	for item in islice(results, num):
		ends.append(item)
	print("\nLooking at head and tail of the following scaffs:\n")
	for k,v in results.items():
		if k in ends:
			print(k.replace(">",""))
			a="".join(v[0])
			b="".join(v[1])
			final[k+"L"]=a.upper()	#ensure bases are upper case
			final[k+"R"]=b.upper()


	return final
					


def write_split_fastas(splits):

	fastas={}
	for k,v in splits.items():
		with open(k.replace(">","")+".fa",'w') as fout:
			fout.write(">"+k+"\n")
			fout.write(v)
			fastas[k]=v
	return fastas	
	
	
		


def main():

	parser = argparse.ArgumentParser(description='Tops and tails scaffolds',formatter_class=argparse.ArgumentDefaultsHelpFormatter) 

	#positional args
	parser.add_argument('fasta', metavar='fasta', type=str, help='assembly fasta')
	
	#optional args
	parser.add_argument('--size', metavar='size', type=int, help='top and tail scf bp', default=200)
	parser.add_argument('--klo', metavar='klo', type=int, help='min kmer', default=4)
	parser.add_argument('--khi', metavar='khi', type=int, help='max kmer', default=15)
	parser.add_argument('--ends', metavar='ends', type=int, help='ends to scan', default=1000)

	if len(sys.argv) <1: 
		parser.print_help()
		

	args = parser.parse_args()  #gets the arguments
	start_time = datetime.now()
	
	fasta=location(args.fasta)
	
	
	print("\nTop and tailing input scaffold fasta...\n")
	print(fasta, args.size)
	
	#Writes fasta file of just ends (ends.fa) from input fasta file (args.fasta)
	top_and_tail(fasta, args.size)
	
	fasta=location("ends.fa")
	
	if args.ends:
		ends=int(int(args.ends)/2)
	
	
	split_fastas=process_fasta(fasta, ends)

	num_ends=int(len(split_fastas)/2)
	

	fastas = write_split_fastas(split_fastas)
	
	
	
	
	



if __name__ == '__main__':
	main()

