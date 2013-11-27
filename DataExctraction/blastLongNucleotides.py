__author__ = 'Mark'
from os import listdir
import xlrd
from os import stat
import urllib2
import xml.etree.ElementTree as ET
import shlex
import re
import subprocess

def genNucleotideRoi(sequences):
    num = 0
    for (seq,name) in sequences:
        num += 1
        try:
            if stat("Protein FASTAs/"+name+".fasta")[6]==0:
                continue
            with open("Protein FASTAs/"+name+".fasta") as f:
                lines = f.readlines()[1:-1]
                text = ""
            for line in lines:
                text += line.strip()
            leftpos = text.find(seq)
            if leftpos == -1:
                continue
            rightpos = leftpos + len(seq)
            leftpos *= 3
            rightpos *= 3
            leftpos = max(0,leftpos-500)
            rightpos = min(len(text)*3,rightpos+500)
            u = urllib2.urlopen("http://www.uniprot.org/uniprot/"+name+".xml")
            localFile = open("tmp.xml", 'w')
            localFile.write(u.read())
            localFile.close()

            tree = ET.parse("tmp.xml")
            i = 0
            for atype in tree.findall(".//{http://uniprot.org/uniprot}dbReference"):
                if atype.get('type') == 'EMBL':
                    i = i + 1
                    if i == 2:
                        seqID = atype.get('id')
                        break
                    else:
                        continue

            nucleoName = name + "_" + seqID + ".fasta"

            with open("Nucleotides short FASTAs/"+nucleoName) as f:
                tmp = f.readlines()
                lines = tmp[1:-1]
                caption = tmp[0]
                text = ""
            for line in lines:
                text += line.strip()
            ROI = text[leftpos:rightpos]
            if len(ROI) == 0:
                continue
            file = open("Nucleitides FASTA ROIs/"+str(num)+".fasta",'w')
            file.write(caption+ROI)
            file.close()
            print str(num) + " OK"
        except:
            pass

def runLocalNucleoBlast():
    files = listdir("Nucleitides FASTA ROIs/")
    for i in range(len(files)-1):
        if stat("Nucleitides FASTA ROIs/"+files[i])[6]==0:
            continue
        for j in range(i+1,len(files)):
            if stat("Nucleitides FASTA ROIs/"+files[j])[6]==0:
                continue
            command = 'blastn -query "Nucleitides FASTA ROIs"/'+files[i]+' -subject "Nucleitides FASTA ROIs"/'+files[j]+" -task blastn"
            name1 = re.split('\.',files[i])[0]
            name2 = re.split('\.',files[j])[0]
            print name1 + " " + name2
            with open("results/blastNucleoShort/"+name1+"_"+name2+".txt",'w') as fout:
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
    #genNucleotideRoi(sequences)
    runLocalNucleoBlast()