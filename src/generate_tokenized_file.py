import argparse
import re
import unicodedata as ud
def main():
    parser = argparse.ArgumentParser(description="""""")
    parser.add_argument('--preds')
    parser.add_argument('--feats')
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
                    ud_name = "-"
            pred = linepred[2][2:-1] #b'2' --> 2
            if pred == "1":
                acc+=" "
            acc+=ud.lookup(ud_name)
        else:
            #"end of line"
            print(acc.strip())
            acc=""
    if acc:
        print(acc.strip())





if __name__ == "__main__":
    main()