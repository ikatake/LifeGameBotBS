import sys
import common

file_name:str = sys.argv[1]
step:int = 0
run:int = 0
loop_from:int = 0

#ループが確定したrun・step・ループ元stepを読み取る。
run, step, loop_from = common.readLoopFile(file_name)
print ('LifeGameBot run:{} is gone.'.format(run))
if(step == loop_from): #stepとloop_fromが等しい→frozen
    print ('Space is frozen at step:{}.'.format(step))
else:
    print ('Loop between step:{} and step:{}.'.format(loop_from, step))