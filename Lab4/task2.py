"""Lab 4 / Task 2: A* versus zero-heuristic uniform cost search."""
from search import search,ESTIMATE,actual_cost
for title,heuristic in [('A-star',ESTIMATE),('Uniform cost',{node:0 for node in ESTIMATE})]:
    route,cost,visited,expanded=search(heuristic)
    print(title,'route=',route,'cost=',cost,'expanded=',expanded,'count=',len(expanded))
    assert cost==actual_cost(route)==6
