"""Lab 3 / Task 3: cheapest route (UCS) versus fewest hops (BFS)."""
import heapq
from collections import deque
EDGES={'A':[('B',1),('C',2)],'B':[('D',4),('E',1)],'C':[('F',2),('G',10)],'D':[],'E':[('G',1)],'F':[],'G':[]}

def uniform_cost(start='A',goal='G'):
    heap=[(0,start,[start])];best={start:0};expanded=[]
    while heap:
        total,node,path=heapq.heappop(heap)
        if total!=best[node]:continue
        expanded.append(node)
        if node==goal:return path,total,expanded
        for child,weight in EDGES[node]:
            candidate=total+weight
            if candidate<best.get(child,float('inf')):
                best[child]=candidate;heapq.heappush(heap,(candidate,child,path+[child]))
    return None,None,expanded

def shortest_hops(start='A',goal='G'):
    queue=deque([(start,[start])]);seen={start}
    while queue:
        node,path=queue.popleft()
        if node==goal:return path
        for child,_ in EDGES[node]:
            if child not in seen:
                seen.add(child);queue.append((child,path+[child]))

def route_cost(path):
    return sum(next(weight for child,weight in EDGES[node] if child==nxt) for node,nxt in zip(path,path[1:]))

if __name__=='__main__':
    route,cost,visited=uniform_cost();bfs=shortest_hops()
    print('UCS:',route,'cost:',cost,'visited:',visited)
    print('BFS:',bfs,'hops:',len(bfs)-1,'cost:',route_cost(bfs))
    assert cost==route_cost(route)==3 and route_cost(bfs)==12
