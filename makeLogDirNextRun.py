import sys
import common
import os

file_name:str = sys.argv[1]
gene:int = 0
run:int = 0
loop_from:int = 0

#ループが確定したrun・gene・ループ元geneを読み取る。
run, gene, loop_from = common.readLoopFile(file_name)

dir = './stateLogs/{:08}'.format(run+1)
try:
    os.makedirs(dir, exist_ok=True)
except FileExistsError:
    pass

dir = common.state_log_dir + '{:08}'.format(run+1)
try:
    os.makedirs(dir, exist_ok=True)
except FileExistsError:
    pass
