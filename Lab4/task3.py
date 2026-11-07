"""Lab 4 / Task 3: observe the effect of an overestimated heuristic."""
from search import search,ESTIMATE,actual_cost
changed=dict(ESTIMATE);changed['C']=10
for title,heuristic in [('Admissible example',ESTIMATE),('Overestimated C',changed)]:
    route,cost,visited,expanded=search(heuristic)
    print(title,':',route,'total=',cost,'expanded=',expanded)
    assert actual_cost(route)==cost
assert search(ESTIMATE)[1]==6
assert search(changed)[1]==9
print('True remaining cost at C is 3, so h(C)=10 overestimates it.')
