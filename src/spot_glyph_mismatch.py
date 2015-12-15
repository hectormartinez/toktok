import unicodedata as ud
import argparse
from collections import Counter

def readwords(infile, column):
    w = ""
    for line in open(infile).readlines():
        line = line.strip().split("\n")[0]
        w+=line
    return w


def main():
    parser = argparse.ArgumentParser(description="""Toktok feature generator""")
    parser.add_argument('--fileA', help="token-per-line or conll6/9/u file")
    parser.add_argument('--fileB', help="token-per-line or conll6/9/u file")
    parser.add_argument('--lang',)
    parser.add_argument('--columnA',default=0)
    parser.add_argument('--columnB',default=1)

    args = parser.parse_args()

    textA = readwords(args.fileA,args.columnA)
    textB = readwords(args.fileB,args.columnB)
    #print(textA)
    #print(textB)
    countA = Counter(textA)
    countB = Counter(textB)

    #print(countA)
    #print(countB)
    print(len(countA))
    print(len(countB))

    fout = open(args.lang+".only_in_a",mode="w")
    for sA in sorted(set(countA.keys()).difference(set(countB.keys()))):
        try:
            lineout = "\t".join([sA,ud.name(sA),str(countA[sA])])+"\n"
        except:
            lineout = "\t".join([sA,"NAME NOT FOUND",str(countA[sA])])+"\n"
        fout.write(lineout)

    fout.close()
    fout=open(args.lang+".only_in_b",mode="w")
    for sB in sorted(set(countB.keys()).difference(set(countA.keys()))):
        try:
            lineout = "\t".join([sB,ud.name(sB),str(countB[sB])])+"\n"
        except:
            lineout = "\t".join([sB,"NAME NOT FOUND",str(countB[sB])])+"\n"
        fout.write(lineout)
    fout.close()


if __name__ == "__main__":
    main()