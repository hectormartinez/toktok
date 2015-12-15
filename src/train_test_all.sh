

treebankbasepath=$1
lang_short=(en sv bg la el pl da nl et id hu fi)
lang_long=(English Swedish Bulgarian Latin Greek Polish Danish Dutch Estonian Indonesian Hungarian Finnish)
for v in 0 1 2 3 4 5 6 7 8 9 10
do
#echo "${lang_long[$v]} ${lang_short[$v]}"

l_long=${lang_long[$v]}
l_short=${lang_short[$v]}
#qf="--quadratic u:"

    python generate_features.py  --train_file $treebankbasepath/UD_$l_long/"$l_short"-ud-train.conllu --test_file $treebankbasepath/UD_$l_long/"$l_short"-ud-test.conllu > "$l_short".test.tokf
    python generate_features.py  --train_file $treebankbasepath/UD_$l_long/"$l_short"-ud-train.conllu --test_file $treebankbasepath/UD_$l_long/"$l_short"-ud-dev.conllu > "$l_short".dev.tokf
    python generate_features.py --train_file $treebankbasepath/UD_$l_long/"$l_short"-ud-train.conllu > "$l_short".train.tokf
    acc_dev=`rungsted --train "$l_short".train.tokf --test "$l_short".dev.tokf 2>&1|grep Accuracy`
    acc_test=`rungsted --train "$l_short".train.tokf --test "$l_short".test.tokf 2>&1|grep Accuracy`
    echo "$l_long $contextsize $acc_full $acc_keep_r $acc_keep_l"
done
