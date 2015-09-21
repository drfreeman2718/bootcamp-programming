# coding: utf-8

# This file is for those of you who learned Python over the summer (you did that, right?).
# In this file, I've put all of the nitty-gritty details of what makes this website work.

# Except it doesn't work, because you need to write all the functions!

# Some of these functions will just make the website easier to use. Some of them are
# important for the enrichment and clustering tasks that your teammates are working on.

# If you need any help, ask your team or a TA.


# (don't delete this but don't worry about it either)
import os # a built-in module, for dealing with filenames
from . import app # this is part of the website guts



# These are all the files you have to work with. Go open them in a text editor so you can
# get a feel for what they look like, because you need to parse each one to turn on a
# piece of the website.

# A list of yeast genes, with standard names and short descriptions.
GENE_INFO = os.path.join(app.root_path, 'data', 'gene_info.txt')

# A file that maps from GOID to name, aspect (process/function/component), etc
GO_INFO = os.path.join(app.root_path, 'data', 'go_info.txt')

# A two-column file that maps GOID to yeast genes
GO_MEMBERSHIP = os.path.join(app.root_path, 'data', 'go_membership.txt')

# A many-columned file that contains experimental data (yeast microarrays). Each column
# (after the first) is a different experiment, and each row is a gene. The values are log2
# ratios versus untreated control.
EXPERIMENT_FILE = os.path.join(app.root_path, 'data', 'experiment_data.txt')


# return a list or dictionary that maps from the id of an experiment (an int: 0, 1, ..)
# to a list of (systematic name, fold-change value) tuples
# e.g. [[('YAL001C', -0.06), ('YAL002W', -0.3), ('YAL003W', -0.07), ... ],
#       [('YAL001C', -0.58), ('YAL002W', 0.23), ('YAL003W', -0.25), ... ],
#        ... ]
def experiment():
    expt_dict = {}
    exp = 0
    while exp < 33:
    	expt_dict[exp] = []
    	exp+=1
    	
    with open('bootcamp/data/experiment_data.txt', 'r') as newfile:
    	newfile.readline()
    	for line in newfile:
    		column_list = line.split()
    		i = 0
    		for column in column_list[1:]:
    			expt_dict[i].append((column_list[0], column))
    			i+=1
	return expt_dict

# map from a gene's systematic name to its standard name
# e.g. gene_name('YGR188C') returns 'BUB1'
def gene_name(gene):
	with open('bootcamp/data/gene_info.txt', 'r') as newfile:
            for geneName in newfile:
    		geneInfo = geneName.split()
    		if geneInfo[0] == gene:
    			return geneInfo[1]


# map from a gene's systematic name to a list of the values for that gene,
# across all of the experiments.
# e.g. gene_data('YGR188C') returns [-0.09, 0.2, -0.07, ... ]
def gene_data(gene):
	with open('bootcamp/data/experiment_data.txt', 'r') as newfile:
		newfile.readline()
		for line in newfile:
			expt_list = line.split()
			if expt_list[0] == gene:
				return expt_list[1:]


# map from a systematic name to some info about the gene (whatever you want),
# e.g  'YGR188C' -> 'Protein kinase involved in the cell cycle checkpoint into anaphase'
def gene_info(gene):
    with open('bootcamp/data/gene_info.txt', 'r') as newfile:
        	for geneName in newfile:
    			geneInfo = geneName.split()
    			if geneInfo[0] == gene:
    				return geneInfo[2]


# map from a systematic name to a list of GOIDs that the gene is associated with
# e.g. 'YGR188C' -> ['GO:0005694', 'GO:0000775', 'GO:0000778', ... ]
def gene_to_go(gene):
	with open('bootcamp/data/go_membership.txt', 'r') as newfile:
		newfile.readline()
		GOID = []
		for line in newfile:
			gene_list = line.split()
			if gene_list[0] == gene:
				GOID.append(gene_list[1])
	return GOID


# map from one of the GO aspects (P, F, and C, for Process, Function, Component),
# to a list of all the GOIDs in that aspect
# e.g. 'C' -> ['GO:0005737', 'GO:0005761', 'GO:0005763', ... ]
def go_aspect(aspect):
    with open('bootcamp/data/go_info.txt', 'r') as newfile:
    	newfile.readline()
    	GOaspect = []
    	for line in newfile:
    		GO_list = line.split()
    		if GO_list[2] == aspect:
    			GOaspect.append(GO_list[0])
	return GOaspect

# map from a GOID (e.g. GO:0005737) to a *tuple* of the term, aspect, and term definition
# e.g. 'GO:0005737' -> ('cytoplasm', 'C', 'All of the contents of a cell... (etc)'
def go_info(goid):
    with open('bootcamp/data/go_info.txt', 'r') as newfile:
    	newfile.readline()
    	for line in newfile:
    		GO_list = line.split()
    		if GO_list[0] == goid:
				return GO_list[1:]


# the reverse of the gene_to_go function: map from a GOID
# to a list of genes (systematic names)
# e.g. 'GO:0005737' -> ['YAL001C', 'YAL002W', 'YAL003W', ... ]
def go_to_gene(goid):
    with open('bootcamp/data/go_membership.txt', 'r') as newfile:
		newfile.readline()
		genes = []
		for line in newfile:
			gene_list = line.split()
			if gene_list[1] == goid:
				genes.append(gene_list[0])
		return genes
	
