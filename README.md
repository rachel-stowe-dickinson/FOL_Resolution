This is a tool for verifying resolution proofs in first order logic.

The tool uses a simple Python user interface to complete the steps of a resolution proof. The program first collects FOL formulae from the 
user that are in CNF and prenex normal form. The user can then skolemize any formulae that contain quantifiers. Finally, the proof can be 
conducted through a series of resolution and/or unification steps until the user is satisfied with the result. The proof's output will be 
saved to a JSON file.

Run the file `fo_parser.py` to begin using the tool.

<ins>EXAMPLE</ins>

Given the following premises,
1. $\forall x,y. (Q(x) \implies \exists z. P(y,z))$
2. $\forall x. (Q(x))$

Prove:

3. $\exists a,b. P(a,b)$

   

After starting the program, input the premises and the negated target formula in CNF and prenex normal form:
```
forall x,y exists z !q(x) or p(y,z)
forall x q(x)
forall a,b !p(a,b)
done
```

The program will prompt the user to skolemize clause 1. To replace z with f(x,y), enter:
```
f x,y
```

The program will now output the following quantifier-free clauses:
```
!q(x) or p(y,f(x,y))
q(x)
!p(a,b)
```

Now the program will begin prompting the user to complete resolution/unification steps.
The clauses are numbered as follows:
```
1:{!q(x), p(y,f(x,y))} 2:{q(x)} 3:{!p(a,b)}
```

To resolve clauses 1 and 2 on q(x), enter:
```
resolve
```
Then,
```
1 2 q(x)
```

Now, the clauses are:
```
1:{!q(x), p(y,f(x,y))} 2:{q(x)} 3:{!p(a,b)} 4:{p(y,f(x,y))}
```

To unify clauses 3 and 4 by replacing a with y and b with f(x,y), enter:
```
unify
```
Then,
```
>> 3 4 a=y b=f(x,y)
```
Now, the clauses are:
```
1:{!q(x), p(y,f(x,y))} 2:{q(x)} 3:{!p(a,b)} 4:{p(y,f(x,y))} 5:{}
```

Since an empty clause has been reached, the resolution proof can be ended by entering:
```
done
```

The user will then be prompted to save the results of the proof in a JSON file. 
Additionally, the steps of the proof will be printed out as follows:
```
1:{!q(x), p(y,f(x,y))} 2:{q(x)} 3:{!p(a,b)}
1 2 q(x)
1:{!q(x), p(y,f(x,y))} 2:{q(x)} 3:{!p(a,b)} 4:{p(y,f(x,y))}
3 4 a=y b=f(x,y)
1:{!q(x), p(y,f(x,y))} 2:{q(x)} 3:{!p(a,b)} 4:{p(y,f(x,y))} 5:{}
```


This project was a collaborative effort by Rachel Dickinson and Aarthy Kesavan Padmanaban. Inspiration for the resolution portion of the
project was taken from the following repository by Adithya Murali: https://github.com/muraliadithya/logictools.
