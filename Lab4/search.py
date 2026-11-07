"""Lab 4: shared A* / UCS implementation."""
from heapq import heappush,heappop
ROUTES={'S':[('A',1),('B',4)],'A':[('C',2)],'B':[('G',5)],'C':[('G',3)],'G':[]}
ESTIMATE={'S':5,'A':4,'B':4,'C':2,'G':0}

def search(heuristic, verbose=False):
    frontier=[];heappush(frontier,(heuristic['S'],0,'S',['S']))
    best={'S':0};visited=[];expanded=[]
    while frontier:
        f,g,node,path=heappop(frontier)
        if g!=best[node]:continue
        visited.append(node)
        if node=='G':return path,g,visited,expanded
        expanded.append(node)
        for child,weight in ROUTES[node]:
            new_cost=g+weight
            if new_cost<best.get(child,float('inf')):
                best[child]=new_cost
                heappush(frontier,(new_cost+heuristic[child],new_cost,child,path+[child]))
        if verbose:
            print('Expanded',node,'g=',g,'h=',heuristic[node],'f=',f)
            print('Frontier',[(n,score) for score,_,n,_ in sorted(frontier)])
    return None,None,visited,expanded

def actual_cost(path):
    return sum(next(weight for child,weight in ROUTES[node] if child==nxt) for node,nxt in zip(path,path[1:]))
