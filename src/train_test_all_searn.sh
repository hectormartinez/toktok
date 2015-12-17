

featsbasepath=$1
lang_short=( ar bg cs da de el en es et eu fa fi fr ga got grc he hi hr hu id it la nl no pl pt ro sl sv ta )
lang_long=( ar bg cs da de el en es et eu fa fi fr ga got grc he hi hr hu id it la nl no pl pt ro sl sv ta)
for v in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22
do
#echo "${lang_long[$v]} ${lang_short[$v]}"

l_long=${lang_long[$v]}
l_short=${lang_short[$v]}
#qf="--quadratic u:"

    echo $l_short
    #python generate_features.py  --train_file $treebankbasepath/"$l_short"-ud-train.conllu.lex --test_file $treebankbasepath/"$l_short"-ud-test.conllu.lex > "$l_short".test.tokf
    #python generate_features.py  --train_file $treebankbasepath/"$l_short"-ud-train.conllu.lex --test_file $treebankbasepath/"$l_short"-ud-dev.conllu.lex > "$l_short".dev.tokf
    #python generate_features.py --train_file $treebankbasepath/"$l_short"-ud-train.conllu.lex > "$l_short".train.tokf
    /home/alonso/tool/vowpal_wabbit/vowpalwabbit/vw -d $featsbasepath/$l_short.train.tokf -f $featsbasepath/$l_short.tok.mdl --search 2 --search_task sequence
    /home/alonso/tool/vowpal_wabbit/vowpalwabbit/vw  -t -d $featsbasepath/$l_short.test.tokf  -i $featsbasepath/$l_short.tok.mdl -p $featsbasepath/$l_short.test.tpred
    python eval_searn.py --pred $featsbasepath/$l_short.test.pred --feats $featsbasepath/$l_short.test.tokf
    /home/alonso/tool/vowpal_wabbit/vowpalwabbit/vw  -t -d $featsbasepath/$l_short.dev.tokf  -i $featsbasepath/$l_short.tok.mdl -p $featsbasepath/$l_short.dev.tpred
    python eval_searn.py --pred $featsbasepath/$l_short.test.pred --feats $featsbasepath/$l_short.dev.tokf
done
#!/usr/bin/env bash