"""Lab 3 / Task 2: depth-limited and iterative deepening search."""
from task1 import GRAPH

def depth_limited(current,goal,remaining,trail=()):
    path=trail+(current,)
    if current==goal:return 'FOUND',list(path)
    if remaining==0:return 'CUTOFF',None
    had_cutoff=False
    for child in GRAPH[current]:
        if child in path:continue
        status,result=depth_limited(child,goal,remaining-1,path)
        if status=='FOUND':return status,result
        if status=='CUTOFF':had_cutoff=True
    return ('CUTOFF' if had_cutoff else 'FAILURE'),None

def iterative_deepening(start,goal,max_depth):
    for depth in range(max_depth+1):
        status,path=depth_limited(start,goal,depth)
        print('IDDFS depth',depth,'=>',status,path)
        if status=='FOUND':return path
        if status=='FAILURE':break
    return None

if __name__=='__main__':
    for limit in [1,2,3,4]:print('DLS',limit,depth_limited('A','G',limit))
    assert iterative_deepening('A','G',4)==['A','B','E','G']
