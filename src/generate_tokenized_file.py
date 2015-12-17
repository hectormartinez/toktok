import argparse
def main():
    parser = argparse.ArgumentParser(description="""""")
    parser.add_argument('--preds')
    parser.add_argument('--feats')
    args = parser.parse_args()

    for linepred, linefeats in zip(open(args.preds),open(args.feats))[:10]:
        print(linepred,linefeats)




if __name__ == "__main__":
    main()