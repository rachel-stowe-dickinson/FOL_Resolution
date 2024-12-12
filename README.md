This is a tool for verifying resolution proofs in first order logic.

The tool uses a simple Python user interface to complete the steps of a resolution proof. The program first collects FOL formulae from the 
user that are in CNF and prenex normal form. The user can then skolemize any formulae that contain quantifiers. Finally, the proof can be 
conducted through a series of resolution and/or unification steps until the user is satisfied with the result. The proof's output will be 
saved to a JSON file.

Run the file fo_parser.py to begin using the tool.

EXAMPLE
Given the following premises,
1. ForAll x. (Q(x) -> Exists y. P(y))
2. ForAll x. (Q(x) -> R(x))
3. Forall x. (R(x) -> !Q(x))
4. Q(a)
Prove
5. Exists x. P(x)

After starting the program, input the premises and the negated target formula in CNF and prenex normal form:
forall x exists y !q(x) or p(y)
forall x !q(x) or r(x)
forall x !r(x) or !q(x)
q(a)
forall x !p(x)
done

The program will prompt the user to skolemize clause 1. To replace y with f(x), enter:
f x

The program will now output the following quantifier-free clauses:
!q(x) or p(f(x))
!q(x) or r(x)
!r(x) or !q(x)
q(a)
!p(x)

Now the program will begin prompting the user to complete resolution/unification steps.
The clauses are numbered as follows:
1:{!q(x), p(f(x))} 2:{!q(x), r(x)} 3:{!q(x), !r(x)} 4:{q(a)} 5:{!p(x)}

To unify clauses 2 and 4 by replacing x with a, enter:
2 4 x=a
Now, the clauses are:
1:{!q(x), p(f(x))} 2:{!q(x), r(x)} 3:{!q(x), !r(x)} 4:{q(a)} 5:{!p(x)} 6:{r(a)}

To unify clauses 3 and 4 by replacing x with a, enter:
3 4 x=a
Now, the clauses are:
1:{!q(x), p(f(x))} 2:{!q(x), r(x)} 3:{!q(x), !r(x)} 4:{q(a)} 5:{!p(x)} 6:{r(a)} 7:{!r(a)}

To resolve clauses 6 and 7 on r(a), enter:
6 7 r(a)
Now, the clauses are:
1:{!q(x), p(f(x))} 2:{!q(x), r(x)} 3:{!q(x), !r(x)} 4:{q(a)} 5:{!p(x)} 6:{r(a)} 7:{!r(a)} 8:{}

Since an empty clause has been reached, the resolution proof can be ended by entering:
done

The user will then be prompted to save the results of the proof in a JSON file.




This project was a collaborative effort by Rachel Dickinson and Aarthy Kesavan Padmanaban. Inspiration for the resolution portion of the
project was taken from the following repository by Adithya Murali: https://github.com/muraliadithya/logictools.
