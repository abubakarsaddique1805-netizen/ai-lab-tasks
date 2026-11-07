"""Lab 4 / Task 1: show first three A* expansions."""
from heapq import heappush,heappop
from search import ROUTES,ESTIMATE
queue=[(ESTIMATE['S'],0,'S')];best={'S':0}
for step in range(1,4):
    f,g,node=heappop(queue)
    print(f'Step {step}: {node}, g={g}, h={ESTIMATE[node]}, f={f}')
    for child,cost in ROUTES[node]:
        candidate=g+cost
        if candidate<best.get(child,float('inf')):
            best[child]=candidate
            heappush(queue,(candidate+ESTIMATE[child],candidate,child))
    print('Open list:',[(name,priority) for priority,_,name in sorted(queue)])
