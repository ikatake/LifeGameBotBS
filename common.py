
def readStateFile(file_path:str)->tuple:
    with open(file_path, mode='r') as f:
        states:str = ''
        n_line:int = 0
        s:str = ''
        for s in f:
            if(n_line < 10):
                states += s.rstrip('\r\n')
            elif(s.split('\t')[0] == 'run'):
                run:int = int(s.split('\t')[1])
            elif(s.split('\t')[0] == 'step'):
                step:int = int(s.split('\t')[1])
            n_line += 1
    #print('states' + states + '\nrun' + str(run) + '\nstep' +str(step))
    return states, run, step

def readLoopFile(file_path:str)->tuple:
    run:int = 0
    step:int = 0
    loop_from:int = 0
    with open(file_path, mode='r') as f:
        s:str = ''
        for s in f:
            #print('[DBGmakeGifMaker.py]' + s ,end='')
            if(s.split('\t')[0] == 'run'):
                run = int(s.split('\t')[1])
            elif(s.split('\t')[0] == 'step'):
                step = int(s.split('\t')[1])
            elif(s.split('\t')[0] == 'loop_from'):
                loop_from = int(s.split('\t')[1])
    return run, step, loop_from

state_log_dir:str = "/home/ikatake/www/wetsteam/LifeGameBotBS/stateLogs/"