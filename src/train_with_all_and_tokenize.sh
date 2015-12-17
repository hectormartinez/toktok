treebankbasepath=$1
rawtextbasepath=$2
lang_short=(  fa en es et eu fi fr ga ar bg cs da de el  got grc he hi hr hu id it la nl no pl pt ro sl sv ta )
#lang_short=( ar bg cs da de en es eu fa fi fr he hi hr id it nl no pl pt sl sv)
for v in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22
do
    l_short=${lang_short[$v]}
    python generate_features.py --train_file $treebankbasepath/"$l_short"-ud-train.conllu.lex --debug > "$l_short".all.train.tokf
    python generate_features.py  --train_file $treebankbasepath/"$l_short"-ud-all.conllu.lex --debug --to_tok $rawtextbasepath/bible/"$l_short" > "$l_short".bible.tokf
    python generate_features.py  --train_file $treebankbasepath/"$l_short"-ud-all.conllu.lex --debug --to_tok $rawtextbasepath/watchtower/"$l_short" > "$l_short".watchtower.tokf
    rungsted --train "$l_short".all.train.tokf -f $l_short.tok.mdl
    rungsted --test "$l_short".watchtower.tokf -i $l_short.tok.mdl --predictions $l_short".watchtower.tpred"
    rungsted --test "$l_short".bible.tokf -i $l_short.tok.mdl --predictions $l_short".bible.tpred"
    python generate_tokenized_file.py --preds $l_short".bible.tpred" --feats "$l_short".bible.tokf > bible/"$l_short".dt
    python generate_tokenized_file.py --preds $l_short".watchtower.tpred" --feats "$l_short".watchtower.tokf > watchtower/"$l_short".dt

 done
