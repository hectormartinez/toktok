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
        print(linepred,linefeats)
        linepred = linepred.strip()
        if linepred:
            if nam.search(linefeats).group(0):
                ud_name = nam.search(linefeats).group(0).replace("name=","")
            pred = linepred[2][2:-1] #b'2' --> 2
            if pred == "1":
                acc=" "
            acc+=ud.lookup(ud_name)
        else:
            #"end of line"
            print(acc)
            acc=""
    if acc:
        print(acc)





if __name__ == "__main__":
    main()