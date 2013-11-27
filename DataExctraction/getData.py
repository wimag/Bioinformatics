__author__ = 'Mark'
import xlrd
import urllib2
import xml.etree.ElementTree as ET
import os.path
def downloadProtFasta(seqID):
    i = 0
    successID = []
    for id in seqID:
        i += 1
        try:
            u = urllib2.urlopen("http://www.uniprot.org/uniprot/"+id+".fasta")
            localFile = open("Protein FASTAs/"+id+".fasta", 'w')
            localFile.write(u.read())
            localFile.close()
            successID.append(id)
            localFile.close()

            u = urllib2.urlopen("http://www.uniprot.org/uniprot/"+id+".xml")
            localFile = open("tmp.xml", 'w')
            localFile.write(u.read())
            localFile.close()
            successID.append(id)
            localFile.close()

            tree = ET.parse("tmp.xml")
            i = 0
            for atype in tree.findall(".//{http://uniprot.org/uniprot}dbReference"):
                if atype.get('type') == 'EMBL':
                    i = i + 1
                    print atype.get('id') + " " + id
                    u = urllib2.urlopen("http://www.ebi.ac.uk/ena/data/view/"+atype.get('id')+"&display=fasta")
                    if i == 1:
                        localFile = open("Nucleotides FASTAs/"+id+".fasta", 'w')
                    else:
                        localFile = open("Nucleotides short FASTAs/"+id+"_"+atype.get('id')+".fasta", 'w')
                    localFile.write(u.read())
                    localFile.close()
                    successID.append(id)
                    localFile.close()


            print "Protein FASTA downloaded" + i
        except:
            pass

    return successID

if __name__ == "__main__":

    if not os.path.exists(r'Nucleotides FASTAs/'):
        os.makedirs(r'Nucleotides FASTAs/')

    if not os.path.exists(r'Nucleotides short FASTAs/'):
        os.makedirs(r'Nucleotides short FASTAs/')

    if not os.path.exists(r'Protein FASTAs/'):
        os.makedirs(r'Protein FASTAs/')

    if not os.path.exists(r'Nucleitides FASTA ROIs/'):
        os.makedirs(r'Nucleitides FASTA ROIs/')

    if not os.path.exists(r'results/blastProtsLong/'):
        os.makedirs(r'results/blastProtsLong/')

    if not os.path.exists(r'results/blastProtsShort/'):
        os.makedirs(r'results/blastProtsShort/')

    if not os.path.exists(r'results/blastNucleoShort/'):
        os.makedirs(r'results/blastNucleoShort/')

    rb = xlrd.open_workbook('trainingdata.xls',formatting_info=True)
    sheet = rb.sheet_by_index(0)

    sequences = []
    seqID = []
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        sequences.append(row[1])
        seqID.append(row[0])
    seqID = list(set(seqID))
    seqID = downloadProtFasta(seqID)
    print seqID
