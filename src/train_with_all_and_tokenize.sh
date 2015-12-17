treebankbasepath=$1
rawtextbasepath=$2
lang_short=( ar bg cs da de el en es et eu fa fi fr ga got grc he hi hr hu id it la nl no pl pt ro sl sv ta )
lang_short=( ar bg cs da de en es eu fa fi fr he hi hr id it nl no pl pt sl sv)
for v in 0 #1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22
do
    l_short=${lang_short[$v]}
    python2.7 generate_features.py --train_file $treebankbasepath/"$l_short"-ud-train.conllu.lex > "$l_short".all.train.tokf
    python2.7 generate_features.py  --train_file $treebankbasepath/"$l_short"-ud-all.conllu.lex --test_file $rawtextbasepath/bible/"$l_short" > "$l_short".bible.tokf
    python2.7 generate_features.py  --train_file $treebankbasepath/"$l_short"-ud-all.conllu.lex --test_file $rawtextbasepath/watchtower/"$l_short" > "$l_short".watchtower.tokf
    rungsted --train "$l_short".all.train.tokf -f $l_short.tok.mdl
    rungsted --test "$l_short".watchtower.tokf -i $l_short.tok.mdl
    rungsted --test "$l_short".bible.tokf -i $l_short.tok.mdl


    python3.4 generate_tokenized_file.py
 done
