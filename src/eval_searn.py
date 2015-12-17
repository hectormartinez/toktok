import argparse
def main():
    parser = argparse.ArgumentParser(description="""""")
    parser.add_argument('--preds')
    parser.add_argument('--feats')
    args = parser.parse_args()

    s_preds = []
    s_gold = []
    for line in open(args.preds).readlines():
        line = line.strip().split("  ")[0].replace(" ","")
        s_preds.append(line)
    acc = ""
    for line in open(args.feats).readlines():
        line = line.strip()
        if line:
            acc+=(line.split(" ")[0])
        else:
            s_gold.append(acc)
            acc = ""
    if acc:
        s_gold.append(acc)

    totalsymbols = 0
    totalmatches = 0
    for p,g in zip(s_preds,s_gold):
        if len(p) != len(g):
            print("error")
            print(p)
            print(g)
        else:
            totalsymbols+=len(p)
            totalmatches+= sum([p_i == g_i for p_i, g_i in zip(p,g)])

    print("acuracy=",totalmatches/totalsymbols)




if __name__ == "__main__":
    main()