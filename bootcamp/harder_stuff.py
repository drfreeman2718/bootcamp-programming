# coding: utf-8

# this file is for those of you with a little more coding experience. You need to calculate
# go-enrichment scores using some gene expression values.

# Feel free to add even more features if you like--the backend code is simple to figure
# out. But don't forget to help your teammates, and to figure out your perturbation!

import scipy.stats as scistat

import mpld3
import matplotlib.pyplot as plt
import seaborn 
import numpy as np
import easier_stuff as eas
# The point of this function is to calculate the enrichment scores for a single
# experiment--the probability that the list of genes is positively or negatively
# enriched for specific groups of genes.
#
# There are many ways to do this--one way is to consider the top (or bottom) N genes,
# and ask if they are significantly enriched for a given annotation. The test for this
# is called the hypergeometric distribution:
#   http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.hypergeom.html
#
# inputs:
# - a list of [(gene name, gene value) ... ]
# - a dictionary of {GOID: [list of genes associated with this term]}
# - an int, N, to use as a parameter
#
# outputs:
# - a list of GOIDs, with associated enrichment scores,
#   testing for positive enrichment (sorted from most significant to least)
# - another list of GOIDs and enrichment scores,
#   testing for negative enrichment (again sorted)
#
# 32 experiments
# 4767 genes
# 587 groups of genes
# top 100 genes from experiment
def calculate_enrichment(N=100):
    # You need to replace this with something useful
    experiment_dict = eas.experiment();
    counttop100 = {}
    countbot100 = {}
    goid_prob_top = {}
    goid_prob_bot = {}
#initialize dictionary of goids
    with open("go_info.txt", 'r') as target:
        target.readline();
        for line in target:
            lines = line.split();
            counttop100[lines[0]] = np.zeros(32) #goid counts in top 100
            countbot100[lines[0]] = np.zeros(32) #goid counts in top 100
            goid_prob_top[lines[0]] = np.zeros(32) #goid prob
            goid_prob_bot[lines[0]] = np.zeros(32) #goid prob
    #add values for goid
    for i in range(0, 33):
        sorted_genes = experiment_dict[i].sort(key=lambda tup: tup[1])
        top100 = sorted_genes[0:100]
        bot100 = sorted_genes[-100:0]
        #go hrough top 100, want list of goIds, count for top/bot100
        for j in range(0, 100):
            counttop100[ gene_to_go[ top100[j][0] ] ][i] += 1
            countbot100[ gene_to_go[ top100[j][0] ] ][i] += 1
            
        #hypergeom, what is the probability i got that many counts from top 100
        #top
        for j in counttop100:
        
            gene_per_go = len(go_to_gene[j])
            [ M, n, N] = [4767, gene_per_go, N];
            rv = scistat.hypergeom(M, n, N)
            x = np.arange(0, counttop100[j][i] + 1)
            survival_exp = rv.sf(x)
            goid_prob_top[j][i] = survival_exp

        for j in countbot100:
            gene_per_go = len(go_to_gene[j])
            [ M, n, N] = [4767, gene_per_go, N];
            rv = scistat.hypergeom(M, n, N)
            x = np.arange(0, countbot100[j][i] + 1)
            survival_exp = rv.sf(x)
            goid_prob_bot[j][i] = survival_exp

#for j in experiment_dict[i]:
            
        #    mainstuff[ gene_to_go[j[0]] ][i] += j[1]
#sort by exp values
#        mainstuff.sort(key=lambda tup: tup[1])
#take top 100
            

    heatmaptop = plt.pcolor(goid_prob_top);
    heatmapbot = plt.pcolor(goid_prob_bot);
    plt.show()

    positive_enrichment_scores = goid_prob_top;
    negative_enrichment_scores = goid_prob_bot;

    return positive_enrichment_scores,negative_enrichment_scores


# It would be useful to group experiments together. This function is one way to
# do that: for a given experiment, figure out which experiments are most similar
# and return them as a list (of integers)
#
# inputs:
# - the index for a single experiment (an int: 0, 1, ..)
# - a list or dictionary that maps from id to experiment data--this will be
#   the output from easier_stuff.experiment()
# - an int, N, to use as a parameter
#
# outputs:
# - a list of the N most similar experiments (determined however you like)
#
def similar_experiments(exp, exp_data, n=10):
    return None


# The more general version of the above function is to cluster the experiments.
# You should have heard something about clustering already, I hope. The idea for this
# function is to make heatmap of clustered experiments, save it to a file, and return
# the path to that file. Alternatively you can make whatever image you think will be
# useful.
#
# input:
# - a list or dictionary that maps from the id of an experiment (an int: 0, 1, ..)
#   to a list of (systematic name, fold-change value) tuples--this will be the output
#   from easier_stuff.experiment()
#
# output:
# - the path to a figure
#
# The function should plot a summary figure for all the experiments (whatever you like,
# but perhaps a clustering?), save the figure as an image, and return the path to that
# figure. Note: you should save the figure somewhere in the "bootcamp" folder but you
# should omit that name from the return value.
#
# e.g. plot_experiment_overview(exp_data) saves a figure to "bootcamp/static/a_figure.png"
#      and it returns the path "static/a_figures.png" as its output
#
def plot_experiment_overview(experiment_data):
    return None


# You can make your website fancier by creating a figure for each experiment
# We've set it up for you to use mpld3 for this.
# Read their website to get started: http://mpld3.github.io/index.html

# input:
# - a list of [(gene name, gene value) ... ]
#
# output:
# - a dictionary, created by the mpld3 module from a figure you've made (see below)
#
def plot_experiment(gene_data):
    mpld3_dict = None

    # When you've made your plot, convert it with the mpld3 library like so:
    # mpld3_dict = mpld3.fig_to_dict(fig)

    return mpld3_dict


# You can make your website extremely fancy with some networks. The idea is to
# create a network with two types of nodes: genes and go terms.
# - A gene is connected to every go term it is annotated with.
# - A go term is connected to every gene it annotates.
#
# inputs:
# - a goid or gene systematic name
# - a flag that is True when the previous input is a goid
# - an int n that describes how many steps in the network
#
# outputs:
# - a dictionary containing two keys: 'nodes' and 'links'
#   'nodes' : a list of node dictionaries, of the form:
#             {'id': goid or gene systematic name,
#               'name': go or gene name
#               'node_type': go aspect or 'gene'}
#   'links' : a list of edge dictionaries, of the form:
#             {'source': index of the source node,
#              'target': index of the target node}
#   where the indexes point to nodes in the 'nodes' list
#
#  e.g. go_network('GO:0006383') returns
#  { 'nodes': [{'id': u'GO:0006383',
#               'name': 'transcription from RNA polymerase III promoter',
#               'node_type': 'P'},
#              {'id': 'YAL001C', 'name': 'TFC3', 'node_type': 'gene'},
#              {'id': 'YBR123C', 'name': 'TFC1', 'node_type': 'gene'},
#              ...],
#    'links': [{'source': 0, 'target': 1},
#              {'source': 0, 'target': 2},
#              {'source': 0, 'target': 3}
#              ...]
#  }
#
def go_network(goid_or_gene, is_goid=True, n=2):
    return None

def main():
    calculate_enrichment();
    

if __name__ == "__main__":
    main();
