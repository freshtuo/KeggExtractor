# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 14:30:16 2018

@author: taz2008
"""

# fetch_genes_in_pathways.py
# given a set of pathways, fetch genes in each pathway
# 

import sys
import urllib2
from re import search
from time import sleep

# functions
def digestHtml(thtml):
	##### split html content into multiple info blocks
	##### a block starts with a block id starting from the first position of a line
	##### '///' indicates the end of html
	# split data by lines
	tdata = thtml.split("\n")
	# split data by block
	tloc = []
	for k,tline in enumerate(tdata):
		if search("^///", tline):# end of data
			tloc.append(k)
			break
		if search("^\S", tline):# start of a block
			tloc.append(k)
	#print len(tloc)-1,"blocks detected."
	# extract header for each block and save corresponding info
	tretdic = {}
	for k in xrange(len(tloc)-1):# each block
		# process first line of a block: 
		# block_id   entry_1
		bid, bentry = search("^(\S+)\s(.*)", tdata[tloc[k]]).groups()
		# add all entries in the block
		binfo = [bentry.strip()]# entry 1
		binfo.extend([x.strip() for x in tdata[tloc[k]+1:tloc[k+1]]])
		# add to dictionary
		if bid.strip() in tretdic:
			#print "Warning: un-unique block ids found:", bid
			tretdic[bid].extend(binfo)
			##sys.exit(1)
		else:
			tretdic[bid] = binfo
	return tretdic

def getGenes(tbdic):
	# extract genes in GENE block
	# locate GENE block
	if "GENE" not in tbdic:
		print "Error: failed to find GENE block."
		sys.exit(2)
	#print len(tbdic["GENE"]),"entries in GENE block."
	# check if gene names are available
	tmiss = [x.split()[0] for x in tbdic["GENE"] if ";" not in x]
	if tmiss:
		print "Warning: missing gene names for",",".join(tmiss),"please manually correct them!"
	# collect gene names
	return [x.split(";")[0].split()[-1] for x in tbdic["GENE"]]

def getName(tbdic):
	# extract pathway name
	# locate NAME block
	if "NAME" not in tbdic:
		print "Error: failed to find NAME block."
		sys.exit(3)
	return tbdic["NAME"][0]

def processPathway(tkgid, tsp):
	# download pathway data and extract name & genes
	tgenes = []
	tname = ''
	try:
		print "processing %s%s..."%(sp,kgid),
		url = "http://rest.kegg.jp/get/%s%s"%(tsp,tkgid)
		uf = urllib2.urlopen(url)
		html = uf.read()
		blocks = digestHtml(html)
		#print len(blocks),"blocks loaded."
		tgenes = getGenes(blocks)
		#print len(genes), "genes extracted."
		tname = getName(blocks)
		print "ok."
	except urllib2.HTTPError as e:
		print e.code, e.reason, ":", e.url
	# wait 5 seconds before connecting again
	sleep(5)
	return (tname,tgenes)

# main
# species: 'hsa' for human; 'ko' for general pathways
sp = "hsa"
# KEGG id
#kgid = "03015"
# a set of pathways
pathwayfile = "eg/pathways.txt"
# output folder
outdir = "info/"
# outfile
outfile = outdir+"KEGG.selected_pathways.genes.txt"

# read in pathways
fin = file(pathwayfile,'r')
pathways = [[y.strip() for y in x.split("\t")] for x in fin.readlines()]
fin.close()
print len(pathways),"pathways to process."

# extract gene names in each pathway and write to file
fout = file(outfile,'w')
for kgid, des in pathways:
	pname, pgenes = processPathway(kgid, sp)
	# double check pathway name
	if pname != '' and pname.split(" - ")[0].strip() != des:
		print "pathway name not matched:", des, pname.split("-")[0].strip()
	fout.write("%s%s\t%s\t%d\t%s\n"%(sp,kgid,pname,len(pgenes)," ".join(pgenes)))
fout.close()

print "Complete!"
