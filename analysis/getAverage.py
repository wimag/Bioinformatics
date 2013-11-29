__author__ = 'Mark'
from os import listdir
from os import stat
import xlwt
import re
#get stats of long prots alignment
def getLongProtsStats():
    files = listdir("../DataExctraction/results/blastProtsLong/")
    hits = []
    longStrs = []
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

        align = ""
        for x in range(len(lines)-1):
            if lines[x].find("Query  ") != -1:
                line = lines[x+1]
                align += line[12:62]
        longStrs.append(getLongestMatch(align))
        print file+ " success"
    createXls(hits,"longLongProtsHitPercentage.xls")


#create excel table
def createXls(hits,name):
    stats = [0]*1001
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
    longStrs = []
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
        align = ""
        for x in range(len(lines)-1):
            if lines[x].find("Query  ") != -1:
                line = lines[x+1]
                align += line[12:62]
        longStrs.append(getLongestMatch(align))
        print file + " success"
    createXls(hits,"shortProtsHitPercentage.xls")
    createXls(longStrs,"shortProtsMatchLens.xls")

#get longest match from alignment results
def getLongestMatch(s):
    ans = 0
    for i in range(len(s)):
        cur = 0
        for j in range(i,len(s)):
            if s[j] == ' ':
                break
            cur += 1
        ans = max(cur,ans)
    return ans
if __name__ == "__main__":
    getLongProtsStats()
    getShortProtsStats()

