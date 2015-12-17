import argparse
import re
import unicodedata as ud
def main():
    parser = argparse.ArgumentParser(description="""""")
    parser.add_argument('--preds')
    parser.add_argument('--feats')
    parser.add_argument('--s/t',default="t")
    args = parser.parse_args()

    nam=re.compile("name=([\w_]+)")
    acc=""
    for linepred, linefeats in zip(open(args.preds,encoding="utf-8").readlines(),open(args.feats,encoding="utf-8").readlines()):
        linepred = linepred.strip()
        if linepred:
            linepred = linepred.split()
            if nam.search(linefeats).group(0):
                try:
                    ud_name = nam.search(linefeats).group(0).replace("name=","").replace("_"," ")
                except:
                    ud_name = "HYPHEN-MINUS"
            pred = linepred[2][2:-1] #b'2' --> 2
            if pred == "1":
                acc+=" "
            try:
                acc+=ud.lookup(ud_name)
            except:
                acc+="-"
        else:
            #"end of line"
            for x in acc.split(" "):
                print(x)
            print()
            #print(acc.strip())
            acc=""
    if acc:
        for x in acc.split(" "):
            print(x)
        print()





if __name__ == "__main__":
    main()