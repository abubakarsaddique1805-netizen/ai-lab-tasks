"""Lab 5 / Task 3: sibling order changes pruning, not game value."""
from task2 import LEAVES,minimax,alpha_beta

def exchange_at_level(leaves,level):
    if level<1 or level>3:raise ValueError('Level must be 1, 2, or 3')
    width=len(leaves)//(2**level)
    reordered=[]
    for position in range(0,len(leaves),width*2):
        left=leaves[position:position+width]
        right=leaves[position+width:position+2*width]
        reordered.extend(right+left)
    return reordered

if __name__=='__main__':
    variants=[('Given order',LEAVES)]
    variants.extend((f'Swapped level {level}',exchange_at_level(LEAVES,level)) for level in [1,2,3])
    for title,values in variants:
        base=minimax(values);pruned=alpha_beta(values)
        assert base[0]==pruned[0]==5
        print(title,'leaves=',values,'minimax=',base,'alpha-beta=',pruned)
