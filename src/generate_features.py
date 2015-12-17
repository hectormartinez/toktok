import argparse
import unicodedata as ud
from collections import Counter, defaultdict


label_dict = {}
label_dict["B"]="1"
label_dict["I"]="2"
label_dict["E"]="3"


class FeatureInstance:
    def __init__(self):
        self.label = ""
        self.feats = defaultdict(str)
        self.instanceid = ""

    def __str__(self):
        return self.label+" "+self.instanceid+"|"+ " |".join([k+" "+self.feats[k] for k in self.feats.keys()])

    def _featnamelist(self,pref,n):
        namelist = []
        for i in range(n):
            namelist.append(pref+"_"+str(i))
        return namelist

    def _featnames(self,idx,windowsize): #"generates the name for w-2,,w+2 style features"
        names = []
        for x in range(windowsize*2+1):
            suffix = x-windowsize
            names.append(idx+"_"+(str(int(suffix))))
        return names

    def _feat_vw_name(self,string):
        return string.replace(':', '<COLON>').replace('|', '<PIPE>').replace(' ', '_')


    def stringwindow(self, stringlist, index, windowsize, name): #for [a,b,c,d,e], i=2 and windowsize=2, returns [a,b,c,d] with headers for each value
        paddedlist = ["^","_"] + stringlist + ["_","$"]
        index = index + windowsize
        values = paddedlist[(index-windowsize):index+windowsize+1]
        names = self._featnames(name, windowsize)
        result = []
        for n, v in zip(names, values):
            result.append(self._feat_vw_name(n+"="+v))
        return " ".join(result)

    def _feat_unicodata(self,glyph):
        udname = ud.name(glyph)
        v = ["name="+udname.replace(" ","_")]
        self.feats["unicode"]= " ".join(v)

    def _feat_dictionary(self,joinedsent,glyph_idx,wordfreqs,windowsize):
        nospacesentlength = len(joinedsent.replace(" ",""))
        joinedsent = joinedsent.lower()

        dictfeats = []
        longest = []
        longest_left = 0
        longest_right = 0

        for current_window_value in reversed(list(range(1,windowsize+1))):
            leftcontext =  joinedsent[:glyph_idx].replace(" ","")[-1*current_window_value:]
            rightcontext = joinedsent[glyph_idx+1:].replace(" ","")[:current_window_value]

            if longest_left == 0 and leftcontext+joinedsent[glyph_idx] in wordfreqs.keys() and glyph_idx >= current_window_value: #len(leftcontext+joinedsent[glyph_idx]) <= windowsize:
            #    dictfeats.append("left"+str(current_window_value))
                longest_left=current_window_value

            if longest_right == 0 and joinedsent[glyph_idx]+rightcontext in wordfreqs.keys():#: and glyph_idx + current_window_value <= nospacesentlength:
             #  dictfeats.append("right"+str(current_window_value))
               longest_right=current_window_value
        if longest_left > 0:
             dictfeats.append("longestleft="+str(longest_left))
        if longest_right > 0:
             dictfeats.append("longestright="+str(longest_right))

            #if ldictfeats:
            #    self.feats["ldict"]=" ".join(ldictfeats)
            #if rdictfeats:
            #    self.feats["rdict"]=" ".join(rdictfeats)
        self.feats["dict"]=" ".join(dictfeats)



    def _feat_prevsymbols(self,joinedsent,glyph_idx,glyph_list,windowsize,trigs=None):
        leftcontext =  joinedsent[:glyph_idx].replace(" ","")[-1*windowsize:]
        rightcontext = joinedsent[glyph_idx+1:].replace(" ","")[:windowsize]
        v = []

        # trig = ("^"+leftcontext)[-1]+joinedsent[glyph_idx]+(rightcontext+"$")[0]
        # if trig in trigs:
        #     v.append("tg="+str(trigs.index(trig)))

        for idl,l in enumerate(leftcontext):
            if leftcontext[idl] in glyph_list:
                v.append("l_"+str(idl)+"_"+str(glyph_list.index(leftcontext[idl])))
        for idr,r in enumerate(rightcontext):
            if rightcontext[idr] in glyph_list:
                v.append("r_"+str(idr)+"_"+str(glyph_list.index(rightcontext[idr])))
        self.feats["glyphsaround"]=" ".join(v)
        #print(leftcontext,rightcontext)
        #for size in range(1,windowsize+1):




def read_token_per_line_sentences(infile,column):
    sent = []
    for line in open(infile,encoding="utf-8").readlines():
        line = line.strip()
        if not line:
            yield sent
            sent = []
        elif line.startswith("#"):
            pass
        else:
            token = line.split("\t")[column]
            sent.append(token)
    if len(sent):
        yield sent


def sentence_feats(sentid,sent,BI_or_IE,wordfreqs,glyph_list,glyph_context,trigs=None):
    joinedsent = " "+" ".join(sent)+" " #joining and padding for extra comfort
    for ids, s in enumerate(joinedsent):
        fi = FeatureInstance()
        instanceid = "'"+str(sentid)+":"+str(ids)
        if s == " ":
            pass
        else:
            label = label_dict["I"]
            if BI_or_IE == "BI" and joinedsent[ids-1] == " ":
                label = label_dict["B"]
            elif BI_or_IE == "IE" and joinedsent[ids+1] == " ":
                label = label_dict["E"]
            fi.label = label
            fi.instanceid = instanceid
            fi._feat_unicodata(s)
            fi._feat_dictionary(joinedsent,ids,wordfreqs,windowsize=10)
            fi._feat_prevsymbols(joinedsent,ids,glyph_list,windowsize=glyph_context,trigs=trigs)
            print(fi)
    print()



def main():
    parser = argparse.ArgumentParser(description="""Toktok feature generator""")
    parser.add_argument('--train_file', help="token-per-line or conll6/9/u file")
    parser.add_argument('--test_file', help="token-per-line or conll6/9/u file")
    parser.add_argument('--column',default=1)
    parser.add_argument('--BI_or_IE',choices = ['BI','IE'], default="BI")
    parser.add_argument('--glyph_context',type=int,default=5)


    args = parser.parse_args()

    sentences = list(read_token_per_line_sentences(args.train_file,args.column))
    wordfreqs = Counter(word.lower() for sent in sentences for word in sent)
    l="".join(letter for word in wordfreqs.keys() for letter in word)
    #trigs=list(sorted(set([x+y+z for x,y,z in zip(l,l[1:],l[2:])])))


    glyph_list=sorted(set([letter for word in wordfreqs.keys() for letter in word]))

    if args.test_file:
        sentences = list(read_token_per_line_sentences(args.test_file,args.column))

    #print(wordfreqs)
    for sentid,sent in enumerate(sentences):
        sentence_feats(sentid,sent,args.BI_or_IE,wordfreqs,glyph_list,args.glyph_context)

if __name__ == "__main__":
    main()