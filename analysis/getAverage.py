__author__ = 'Mark'
from os import listdir
from os import stat
import xlwt
import re
#get stats of long prots alignment
def getLongProtsStats():
    files = listdir("../DataExctraction/results/blastProtsLong/")
    hits = []
    for file in files:
        path = "../DataExctraction/results/blastProtsLong/" + file;
        if stat(path)[6]==0:
            continue
        with open(path) as f:
            lines = f.readlines()[14:-1]

        for line in lines:
            if line.find('%') == -1:
                continue
            hits.append(int(re.split('\(|\)| |%',line)[5]))
            break
        print file+ " success"
    createXls(hits,"longProtsHitPercentage.xls")


#create excel table
def createXls(hits,name):
    stats = [0]*101
    for x in hits:
        stats[x] += 1
    wb = xlwt.Workbook()
    ws = wb.add_sheet('data')
    for i in range(0,101):
        ws.write(i, 0, i)
        ws.write(i, 1, stats[i]);
    wb.save(name)

#get stats of short prots alignment
def getShortProtsStats():
    files = listdir("../DataExctraction/results/blastProtsShort/")
    hits = []
    for file in files:
        path = "../DataExctraction/results/blastProtsShort/" + file;
        if stat(path)[6]==0:
            continue
        with open(path) as f:
            lines = f.readlines()[5:-1]

        for line in lines:
            if line.find('%') == -1:
                continue
            hits.append(int(re.split('\(|\)| |%',line)[5]))
            break
        print file+ " success"
    createXls(hits,"shortProtsHitPercentage.xls")


if __name__ == "__main__":
    #getLongProtsStats()
    getShortProtsStats()

