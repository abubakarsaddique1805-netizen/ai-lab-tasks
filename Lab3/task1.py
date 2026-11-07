"""Lab 3 / Task 1: breadth-first and depth-first graph search."""
from collections import deque
GRAPH = {'A':['B','C'], 'B':['D','E'], 'C':['F'], 'D':[], 'E':['G'], 'F':[], 'G':[]}

def breadth_first(start='A', goal='G'):
    queue = deque([(start,[start])]); discovered = {start}; order=[]
    while queue:
        node, path = queue.popleft(); order.append(node)
        print('BFS visit',node,'queue', [item[0] for item in queue])
        if node == goal: return path, order
        for neighbor in GRAPH[node]:
            if neighbor not in discovered:
                discovered.add(neighbor);queue.append((neighbor,path+[neighbor]))
    return None, order

def depth_first(start='A',goal='G'):
    stack=[(start,[start])]; visited=set(); order=[]
    while stack:
        node,path=stack.pop()
        if node in visited:continue
        visited.add(node);order.append(node)
        print('DFS visit',node,'stack',[item[0] for item in stack])
        if node==goal:return path,order
        for neighbor in reversed(GRAPH[node]):
            if neighbor not in visited:stack.append((neighbor,path+[neighbor]))
    return None,order

if __name__=='__main__':
    for label,fn in [('BFS',breadth_first),('DFS',depth_first)]:
        path,order=fn();print(label,'path:',path,'order:',order)
        assert path == ['A','B','E','G']
