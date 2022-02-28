import numpy as np
from scipy.optimize import minimize
from numpy import zeros
import math
#This program is to mimic the excel for kelly calculation for horse racing 
# From chapter 7 (計得精彩: 賽馬的統計及數學方法 )

#enter your guess here, it is like odds, but it is not normalized
your_line = [5, 2.5, 20, 10, 8]

# enter the odds from betting company
real_odd = [4,4,4,4,4]

total_amount = 10000

#======== computation part =======

# First normalize the odd
guess_total = sum([1.0/x for x in your_line])

adj_prob = [1.0/x / guess_total for x in your_line]

adj_odd = [1.0/x for x in adj_prob]

# Now we have the adj_odd and the real_odd, now we optimize the outcome
# The game is to bet which horse win the race.
# so the outcome for a winning hourse i is  (Total amount) + Bet[i] * real_odd[i] - (Money spend in betting)
# the formula is like sum i=0..n [ adj_prob[i] * (  (Total amount) + Bet[i] * real_odd[i] - (Money spend in betting) ) ]
# according to the kelly formula, we should maximize
#   first denote g[i] = adj_prob[i] * log(  (Total amount) + Bet[i] * real_odd[i] - (Money spend in betting) )
#
#   exp{ sum i=0..n [ g[i] ] }
#   
print("Debug")
print("Prob:" , adj_prob)
print("Odd:" , adj_odd)

def G(bet):
    gsum = 0
    sum_bet = sum(bet)
    for i in range(0, len(your_line)):
        gsum += adj_prob[i] * math.log(total_amount + bet[i] * real_odd[i] - sum_bet)

    return -math.exp(gsum)

print("Test G: ", G([714.2797, 2999.99, 0, 0, 0]))

def constraint_bet_non_negative(x):
    return x

cons=({'type':'ineq','fun':constraint_bet_non_negative} )

# solve
guess = zeros(len(your_line), float)
print("E", guess)
sol = minimize(G, guess, method='COBYLA',constraints=cons, options={"maxiter": 5000}) 

print("Result ", sol, "G: ",G(sol.x))
