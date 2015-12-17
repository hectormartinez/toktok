

treebankbasepath=$1
lang_short=( ar bg cs da de el en es et eu fa fi fr ga got grc he hi hr hu id it la nl no pl pt ro sl sv ta )
lang_long=( ar bg cs da de el en es et eu fa fi fr ga got grc he hi hr hu id it la nl no pl pt ro sl sv ta)
for v in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22
do
#echo "${lang_long[$v]} ${lang_short[$v]}"

l_long=${lang_long[$v]}
l_short=${lang_short[$v]}
#qf="--quadratic u:"

    python generate_features.py  --train_file $treebankbasepath/"$l_short"-ud-train.conllu.lex --test_file $treebankbasepath/"$l_short"-ud-test.conllu.lex > "$l_short".test.tokf
    python generate_features.py  --train_file $treebankbasepath/"$l_short"-ud-train.conllu.lex --test_file $treebankbasepath/"$l_short"-ud-dev.conllu.lex > "$l_short".dev.tokf
    python generate_features.py --train_file $treebankbasepath/"$l_short"-ud-train.conllu.lex > "$l_short".train.tokf
    acc_dev=`rungsted --train "$l_short".train.tokf --test "$l_short".dev.tokf 2>&1|grep Accuracy`
    acc_test=`rungsted --train "$l_short".train.tokf --test "$l_short".test.tokf 2>&1|grep Accuracy`
    echo "$l_long $contextsize $acc_dev $acc_test"
done
