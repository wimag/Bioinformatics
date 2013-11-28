__author__ = 'Mark'
import xlrd
import subprocess
import shlex
import re
from os import listdir
from os import stat
def blastShortSeqs(sequences):
    for i in range(len(sequences)-1):
        for j in range(i+1,len(sequences)):
            f1 = open("shortProt1.fasta","w")
            f2 = open("shortProt2.fasta","w")
            (seq1,inum) = sequences[i]
            (seq2,jnum) = sequences[j]
            f1.write(">" + str(inum) + "\n" + seq1)
            f2.write(">" + str(jnum) + "\n" + seq2)
            f1.close()
            f2.close()
            command = "blastp -query shortProt1.fasta -subject shortProt2.fasta -task blastp"
            with open("results/blastProtsShort/"+inum+"_"+jnum+".txt",'w') as fout:
                subprocess.check_call(shlex.split(command),stdout=fout)

def blastSeqs():
    files = listdir("Protein FASTAs/")
    for i in range(len(files)-1):
        if stat("Protein FASTAs/"+files[i])[6]==0:
            continue
        for j in range(i+1,len(files)):
            if stat("Protein FASTAs/"+files[j])[6]==0:
                continue
            command = 'blastp -query "Protein FASTAs"/'+files[i]+' -subject "Protein FASTAs"/'+files[j]+" -task blastp"
            name1 = re.split('\.',files[i])[0]
            name2 = re.split('\.',files[j])[0]
            #print name1 + " " + name2
            with open("results/blastProtsLong/"+name1+"_"+name2+".txt",'w') as fout:
                subprocess.check_call(shlex.split(command),stdout=fout)

if __name__ == "__main__":
    rb = xlrd.open_workbook('trainingdata.xls',formatting_info=True)
    sheet = rb.sheet_by_index(0)

    sequences = []
    seqID = []
    for rownum in range(1,sheet.nrows):
        row = sheet.row_values(rownum)
        sequences.append((row[1],row[0]))
        seqID.append(row[0])
    print(sequences)
    blastShortSeqs(sequences)
    blastSeqs()