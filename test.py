# Test z3 tactics
from z3 import *

'''x = Int('x')
y = Int('y')
cool = Int('cool')
likes = Function('likes', IntSort(), IntSort(), BoolSort())
is_a = Function('is_a', IntSort(), IntSort(), BoolSort())

phi = And(likes(x, cool), is_a(y, cool))
goal = likes(x, y)'''

p = Function('p', IntSort(), BoolSort())
q = Function('q', IntSort(), BoolSort())
r = Function('r', IntSort(), IntSort(), BoolSort())
x,y = Ints('x y')

#phi = ForAll([x,y], Implies(Or(p(x), q(y)), r(x,y)))
phi = ForAll(x, Exists(y, And(Or(Not(p(x)), q(y)), r(x,y))))

# Simplify original formula (Remove implication, etc)
simp = Tactic('simplify')
phi = simp(phi).as_expr()
print("Simplified:", phi)

# Skolemize
snf = Tactic('snf')
phi = snf(phi).as_expr()
print("Skolemized:", phi)

# Remove ForAll quantifiers if in formula
if not type(phi) == BoolRef:
    if phi.is_forall():
        # How do we prevent this from spitting out Var(0) instead of x?
        phi = phi.body()
        print("Elim ForAll:", phi)

# Convert to CNF
cnf = Tactic('tseitin-cnf')
print("CNF:", cnf(phi))





