# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 10:54:28 2018

@author: taz2008
"""
# convert_to_gmt.py
# reformat the output genes to gmt format
# 

# working folder
workdir = "info/"
# genes file
infile = workdir+"KEGG.selected_pathways.genes.manual_fix.txt"
# output file
outfile = workdir+"KEGG.selected_pathways.genes.manual_fix.gmt"

# read in genes
fin = file(infile,'r')
pathways = [[y.strip() for y in x.split("\t")] for x in fin.readlines()]
fin.close()
print len(pathways), "pathways loaded."

# convert to gmt and output
fout = file(outfile,'w')
for entry in pathways:# each pathway
	pid = entry[0]
	plink = "https://www.genome.jp/kegg-bin/show_pathway?map=%s"%pid
	pname = "_".join(entry[1].replace("- Homo sapiens (human)","").split())
	pgenes = "\t".join(entry[3].split())
	fout.write("%s\t%s\t%s\n"%(pname,plink,pgenes))
fout.close()

print "Complete!"
