import sys
import common

file_name:str = sys.argv[1]
gene:int = 0
run:int = 0
loop_from:int = 0

#ループが確定したrun・gene・ループ元geneを読み取る。
run, gene, loop_from = common.readLoopFile(file_name)
print ('LifeGameBot run:{} is gone.'.format(run))
if(gene == loop_from): #geneとloop_fromが等しい→frozen
    print ('Space is frozen at gene:{}.'.format(gene))
else:
    print ('Loop between gene:{} and gene:{}.'.format(loop_from, gene))