# event_agreements.py
# Andrew S. Lang
# Created: 02APR2018
# Last Modified: 02APR2018

# This script will take two input spliced-genes*.tsv file, generated by sig_events_genes.py and will compare
# that TSV to another TSV file, identifying any genes where splicing events are present in both files. This 
# will allow me to identify those splicing events common between different sexes, treatments, or tissues. 
# i.e. comparing spliced_genes-female_hypothalamus_control_female_hypothalamus_stress.tsv to 
# spliced_genes-male_hypothalamus_control_male_hypothalamus_stress.tsv will allow me to identifiy any splicing
# events that are significant between control-stress comparisons in both sexes.

import re
import sys
import gzip

def abbreviate(sample):

    samp_name  = sample.split("_")                              # Generating abbreviations for sample info
    sex1 = samp_name[0][:1].upper()                             # i.e. female_gonad_control-female_gonad_stress
    tiss1 = samp_name[1][:1].upper()                            # will become FGC-FGS
    trt1 = samp_name[2][:1].upper()
    sex1_2 = samp_name[3][:1].upper()
    tiss1_2 = samp_name[4][:1].upper()
    trt1_2 = samp_name[5][:1].upper()
    abbrev1 = sex1 + tiss1 + trt1 + "-" + sex1_2 + tiss1_2 + trt1_2

    return abbrev1

def sig_ev(fname1, fname2):
    file1 = open(fname1, 'r')
    file2 = open(fname2, 'r')

    samp1 = file1.readline().rstrip().split("\t")[1]            # extracting sample name from first line of file
    samp2 = file2.readline().rstrip().split("\t")[1]            # and doing the same for the second file

    samp1_abbrev = abbreviate(samp1)                            # generating abbreviations for diff files
    samp2_abbrev = abbreviate(samp2)

    outfile_name = "shared-" + samp1_abbrev + "_" + samp2_abbrev + ".tsv"
    outfile = open(outfile_name, "w")

    gene_Dict1 = {}
    gene_Dict2 = {}
    shared_genes = ""

    for line in file1:                                          # generating dictionary for genes in first file
        column = line.rstrip().split("\t")                      # where the values are PSI and LOCI
        geneID = column[0]
        psi = column[1]
        loci = column[2]
        gene_Dict1[geneID] = [psi,loci]

    for line in file2:
        column = line.rstrip().split("\t")
        geneID = column[0]
        psi = column[1]
        loci = column[2]
        gene_Dict2[geneID] = [psi,loci] 

    for gene in gene_Dict1.keys():                              # Comparing the keys in the two dictionaries and
        if gene in gene_Dict2.keys():                           # writing any commonalities to outputfile
            shared_genes += gene + "\t" + str(gene_Dict1[gene][0]) + "\t" + str(gene_Dict2[gene][0]) + "\t" + str(gene_Dict1[gene][1]) + "\t" + str(gene_Dict2[gene][1]) + "\n"
        else: 
            continue

    outfile.write("GENE_ID\t" + samp1_abbrev + "\t" + samp2_abbrev + "\tLoci1\tLoci2\t" + "\n" + shared_genes)
    outfile.close()

if __name__ == '__main__':
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    sig_ev(filename1, filename2)
