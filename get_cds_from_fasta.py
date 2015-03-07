#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File    	: get_cds_from_fasta.py
Author  	: Dominik R. Laetsch, dominik.laetsch at gmail dot com 
Version 	: 0.1
Description : 
To do 		: ...
"""

from __future__ import division
import sys

def getRegion(seq, start, stop, strand):
		region = seq[int(start)-1:int(stop)]
		if strand == '-':
			complement = {'A':'T','C':'G','G':'C','T':'A','N':'N'}
			region = "".join([complement.get(nt.upper(), '') for nt in region[::-1]])
		return region

def parseContigs(contig_file):
	contig_dict = {}
	contig_name = ''
	contig_seq = ''
	with open(contig_file) as fh:
		for line in fh:
			if line.startswith(">"):
				# header
				if (contig_name and contig_seq):
					contig_dict[contig_name] = contig_seq
					contig_seq = '' 
				contig_name = line.lstrip(">").rstrip("\n")
			else:
				contig_seq += line.rstrip("\n")
		contig_dict[contig_name] = contig_seq
	print contig_dict
	return contig_dict

def parseGffAndPrint(gff_file, contigs, annotation_type):
	with open(gff_file) as fh:
		for line in fh:
			if not line.startswith("#"):
				field = line.split()
				if field[2] == annotation_type:
					if field[0] in contigs:
						contig, start, stop, strand = field[0], field[3], field[4], field[6]
						seq = contigs[contig]
						print ">" + contig + ";" + strand + ";" + start + ";" + stop 
						print seq
						print getRegion(seq, 1, len(seq), '-') 
						print getRegion(seq, start, stop, strand) 
					else: 
						sys.exit("[ERROR] - %s is not in contig file" %contig)
						


if __name__ == "__main__":
	contig_file, gff_file = '', ''
	try:
		contig_file = sys.argv[1]
		gff_file = sys.argv[2]
		annotation_type = sys.argv[3]
	except:
		sys.exit("Usage: ./get_cds_from_fasta.py [CONTIGFILE] [GFF3] [TYPE]")
	
	contigs = parseContigs(contig_file)
	parseGffAndPrint(gff_file, contigs, annotation_type)


