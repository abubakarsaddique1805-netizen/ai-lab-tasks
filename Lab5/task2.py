"""Lab 5 / Task 2: minimax and alpha-beta, with leaf evaluation counters."""
LEAVES=[3,5,2,9,3,5,2,9]

def validate(values):
    n=len(values)
    if n==0 or n & (n-1):raise ValueError('Require a nonempty power-of-two leaf list')
    return n.bit_length()-1

def minimax(values):
    depth=validate(values);evaluations=0
    def visit(level,index,max_player):
        nonlocal evaluations
        if level==depth:
            evaluations+=1;return values[index]
        first=visit(level+1,index*2,not max_player)
        second=visit(level+1,index*2+1,not max_player)
        return max(first,second) if max_player else min(first,second)
    return visit(0,0,True),evaluations

def alpha_beta(values):
    depth=validate(values);evaluations=0
    def visit(level,index,max_player,alpha,beta):
        nonlocal evaluations
        if level==depth:
            evaluations+=1;return values[index]
        best=float('-inf') if max_player else float('inf')
        for child in [index*2,index*2+1]:
            score=visit(level+1,child,not max_player,alpha,beta)
            if max_player:
                best=max(best,score);alpha=max(alpha,best)
            else:
                best=min(best,score);beta=min(beta,best)
            if alpha>=beta:break
        return best
    return visit(0,0,True,float('-inf'),float('inf')),evaluations

if __name__=='__main__':
    print('Leaves:',LEAVES)
    print('Minimax (value, leaves checked):',minimax(LEAVES))
    print('Alpha-beta (value, leaves checked):',alpha_beta(LEAVES))
    assert minimax(LEAVES)[0]==alpha_beta(LEAVES)[0]==5
