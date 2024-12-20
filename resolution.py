import argparse
import os
import json

#################################### RESOLUTION ITP ######################################


clause_counter = 0
# Maps ID numbers to clauses. Higher numbers are created later.
clausedict = dict()
# Maps clause IDs to parent IDs and the literal on which they were resolved
# Leaf clauses don't have parents and are therefore not indexed here.
parentdict = dict()
# Current clauses in the resolution represented by ID numbers
curr_clauses = []
# String documentation of each step for output
steps = []


# ITP Resolution Checker functions
def end_checker():
    global clause_counter, clausedict, parentdict, curr_clauses
    print("Enter the name of the file where you want to save your proof. If you press Enter, it will be saved to proof.json")
    filename = input().strip()
    if filename == "":
        filename = "proof.json"
    with open(filename, 'w') as fh:
        contents = {"final_clauses": curr_clauses,
                    "clausedict": {k:list(v) for k,v in clausedict.items()},
                    "parentdict": parentdict}
        json.dump(contents, fh)
    
    print("\nHere are the results of your proof:")
    for s in steps:
        print(s)
    return


def backtrack():
    global clause_counter, clausedict, parentdict, curr_clauses, steps
    # Latest clause is the one with the highest number, if at all there is one
    latest_clause = max(curr_clauses)
    # If latest clause is already a leaf, then there is nothing to backtrack
    if latest_clause not in parentdict:
        print("Nothing to backtrack")
        return
    # Remove latest clause from the data structures
    parent1, parent2, _ = parentdict[latest_clause]
    del clausedict[latest_clause]
    del parentdict[latest_clause]
    curr_clauses = [clid for clid in curr_clauses if clid != latest_clause]
    # Remove latest step from output
    last_step = len(steps)-1
    steps.pop(last_step)
    steps.pop(last_step-1)
    return

#Attempt to do a step of unification
def unification_step(clause1, clause2, clid1, clid2, literals):    
    global clause_counter, clausedict, parentdict, curr_clauses

    # Check if literals to resolve belong to both clauses and are negated in one of them
    base_literals = []
    negated_literals = []
    for i in range(len(literals)):
        base_literal = literals[i][1:] if literals[i].startswith('!') else literals[i]
        negated_literal = '!' + base_literal
        base_literals.append(base_literal)
        negated_literals.append(negated_literal)
        if not((base_literal in clause1 and negated_literal in clause2) or (base_literal in clause2 and negated_literal in clause1)):
            print("One of the clauses must contain the literal you provided and the other clause must contain its negation")
            return
    
    # Compute resolvent
    resolvent = set(lit for lit in list(clause1) + list(clause2) if lit not in base_literals and lit not in negated_literals)
    # Determine if resolvent is new and nontrivial
    if any(resolvent == clausedict[clid] for clid in curr_clauses):
        print("Resolution resulted in redundant clause")
        return
    if any('!' + lit in resolvent for lit in resolvent):
        print("Resolution resulted in trivial clause")
        return
    
    #print(resolvent)
    # Index new resolvent and add it to the list of current clauses
    clause_counter += 1
    clausedict[clause_counter] = resolvent
    parentdict[clause_counter] = [clid1, clid2, base_literal]
    # NOTE: If the list becomes too large, this operation is inefficient. Consider using collections.dequeue
    curr_clauses.insert(len(curr_clauses), clause_counter)
    

# Attempts to do one step of resolution
# If resolution step does not make sense (e.g., clause numbers or literals make no sense), then it acts as a no op.
def proof_step(cl_index1, cl_index2, literal):    
    global clause_counter, clausedict, parentdict, curr_clauses

    if (not (1 <= cl_index1 <= len(curr_clauses))) or (not (1 <= cl_index2 <= len(curr_clauses))):
        print(f"Clause numbers must correspond to existing clauses [1-{len(curr_clauses)}]")
        return

    clid1 = curr_clauses[cl_index1-1]
    clid2 = curr_clauses[cl_index2-1]
    # Check if clause ids make sense
    if clid1 not in clausedict:
        print(f"Number {clid1} does not correspond to any clause")
        return
    if clid2 not in clausedict:
        print(f"Number {clid2} does not correspond to any clause")
        return
    # get the corresponding clauses
    clause1 = clausedict[clid1]
    clause2 = clausedict[clid2]
    
    # Check if literal to resolve belongs to both clauses and is negated in one of them
    base_literal = literal[1:] if literal.startswith('!') else literal
    negated_literal = '!' + base_literal
    if not((base_literal in clause1 and negated_literal in clause2) or (base_literal in clause2 and negated_literal in clause1)):
        print("One of the clauses must contain the literal you provided and the other clause must contain its negation")
        return
    
    # Compute resolvent
    resolvent = set(lit for lit in list(clause1) + list(clause2) if lit != base_literal and lit != negated_literal)
    # Determine if resolvent is new and nontrivial
    if any(resolvent == clausedict[clid] for clid in curr_clauses):
        print("Resolution resulted in redundant clause")
        return
    if any('!' + lit in resolvent for lit in resolvent):
        print("Resolution resulted in trivial clause")
        return
    
    #print(resolvent)
    # Index new resolvent and add it to the list of current clauses
    clause_counter += 1
    clausedict[clause_counter] = resolvent
    parentdict[clause_counter] = [clid1, clid2, base_literal]
    # NOTE: If the list becomes too large, this operation is inefficient. Consider using collections.dequeue
    curr_clauses.insert(len(curr_clauses), clause_counter)
    


# Helper functions
def initialize(formula):
    global clause_counter, clausedict, parentdict, curr_clauses, steps
    if curr_clauses != []:
        print("Something is wrong with the program. Exit (Ctrl+C) now.")
        return
    for cl in formula:
        clause_counter += 1
        clausedict[clause_counter] = cl
        curr_clauses.append(clause_counter)
    actual_clauses = [clausedict[j] for j in curr_clauses]
    steps.append(f"""{' '.join([f"{i+1}:{'{'+ ', '.join(sorted(list(cl))) + '}' if cl else '{}'}" for i,cl in enumerate(actual_clauses)])}""")

    


def print_state():
    global clause_counter, clausedict, parentdict, curr_clauses
    actual_clauses = [clausedict[j] for j in curr_clauses]
    print("\nClauses:")
    print(f"""{' '.join([f"{i+1}:{'{'+ ', '.join(sorted(list(cl))) + '}' if cl else '{}'}" for i,cl in enumerate(actual_clauses)])}""")

def find_literal(clause1, clause2):
    
    #look for literals in clause1
    
    for every in clause1:
        if '!'+every in clause2:
            return every
    #look for literals in clause2 and their negation in clause1
    
    for every in clause2:
        if '!'+every in clause1:
            return every
    return None

def find_literals(clause1, clause2):
    literals = []
    #look for literals in clause1
    for every in clause1:
        if '!'+every in clause2:
            literals.append(every)
    #look for literals in clause2 and their negation in clause1
    for every in clause2:
        if '!'+every in clause1:
           literals.append(every)
    if len(literals) > 0:
        return literals
    return None

#unification step
def unify():
    global clause_counter, clausedict, parentdict, curr_clauses, steps
    print("\n**UNIFICATION STEP**\
            \nApply unification by providing clause numbers and the variables on which you want to unify, e.g.\
            \n1:{p(x,y), q(x)} 2:{!p(a,b)}\
            \n>> 1 2 x=a y=b\
            \n1:{p(x,y), q(x)} 2:{!p(a,b)} 3:{q(a)}\
            \nEnter 'b' to go back.")
    print_state()
    try:
        command = input(">> ").strip()    
        if command == 'b':
            return   
    except KeyboardInterrupt:
        exit(0)
    except (AssertionError, ValueError):
        print("Invalid Command")
    params = command.split()
    assert len(params) >=3
    clause1_index = int(params[0])
    clause2_index = int(params[1])
    uni_vars = []
    uni_subs = []
    for i in range(2,len(params)):
        uni_var, uni_sub = params[i].split("=")
        uni_vars.append(uni_var)
        uni_subs.append(uni_sub)

    if (not (1 <= clause1_index <= len(curr_clauses))) or (not (1 <= clause2_index <= len(curr_clauses))):
        print(f"Clause numbers must correspond to existing clauses [1-{len(curr_clauses)}]")
        return

    clid1 = curr_clauses[clause1_index-1]
    clid2 = curr_clauses[clause2_index-1]
    # Check if clause ids make sense
    if clid1 not in clausedict:
        print(f"Number {clid1} does not correspond to any clause")
        return
    if clid2 not in clausedict:
        print(f"Number {clid2} does not correspond to any clause")
        return
    # get the corresponding clauses
    clause1 = clausedict[clid1]
    clause2 = clausedict[clid2]

    for i in range(len(uni_vars)):
        clause1 = set([x.replace(uni_vars[i],uni_subs[i]) for x in clause1])
        clause2 = set([x.replace(uni_vars[i],uni_subs[i]) for x in clause2])

    literals = find_literals(clause1, clause2)
    if literals is None:
        print("Unification step did not result in clauses that can be resolved")
        return
    print('Resolving on :',literals)
    unification_step(clause1, clause2, clid1, clid2, literals)
    steps.append(command)
    actual_clauses = [clausedict[j] for j in curr_clauses]
    steps.append(f"""{' '.join([f"{i+1}:{'{'+ ', '.join(sorted(list(cl))) + '}' if cl else '{}'}" for i,cl in enumerate(actual_clauses)])}""")    
        
    
def res():
    print("""
**RESOLUTION STEP**
Apply resolution rules by providing clause numbers and the function on which you want to resolve, e.g.
1:{p(x), p(y)} 2:{!p(x), p(z)}
>> 1 2 p(x)
1:{p(x), p(y)} 2:{!p(x), p(z)} 3:{p(y), p(z)}
Enter 'b' to go back.""")
    print_state()
    try:
        command = input(">> ").strip()    
        if command == 'b':
            return   
    except KeyboardInterrupt:
        exit(0)
    except (AssertionError, ValueError):
        print("Invalid Command")
    params = command.split()
    assert len(params) == 3
    clause1, clause2, literal = int(params[0]), int(params[1]), params[2]
    proof_step(clause1, clause2, literal)
    steps.append(command)
    actual_clauses = [clausedict[j] for j in curr_clauses]
    steps.append(f"""{' '.join([f"{i+1}:{'{'+ ', '.join(sorted(list(cl))) + '}' if cl else '{}'}" for i,cl in enumerate(actual_clauses)])}""")    


# Main resolution checker interface
def resolve(formula):
    welcome_message = """
Enter 'resolve' to perform a resolution step.
Enter 'unify' to perform a unification step.
Enter 'back' to backtrack, and 'done' to indicate that you have saturated resolution steps.""" 
   
    initialize(formula)    

    while True:
        print_state()
        print(welcome_message)
        try:
            command = input(">> ").strip()
            if command == "done":
                end_checker()
                break
            elif command == "back":
                backtrack()
            elif command == "help":
                print(welcome_message)
            elif command == "unify":
                unify()
            elif command == "resolve":
                res()      
            else:
                print("Please enter 'resolve', 'unify', 'back', or 'done'.")
        except KeyboardInterrupt:
            exit(0)
        except (AssertionError, ValueError):
            print("Invalid Command")


#################################### PROOF OBJECT CHECKER ######################################

# Reads the proof object from the file and checks if it represents a valid resolution proof of the given formula
def check_proof(formula, proof_file):
    # Read contents of proof file
    with open(proof_file, 'r') as fh:
        contents = json.load(fh)
    final_clauses = contents['final_clauses']
    clause_dict = contents['clausedict']
    clause_dict = {int(k): set(v) for k,v in clause_dict.items()}
    parent_dict = contents['parentdict']
    parent_dict = {int(k): v for k,v in parent_dict.items()}
    
    actual_clauses = [clause_dict[clid] for clid in final_clauses]

    if set() in actual_clauses:
        is_sat = False
    else:
        is_sat = True

    # Check 1: Either empty set should be in the final list of clauses, or they should all be saturated
    try:
        if set() not in actual_clauses:
            # Check for saturation
            # Get all base_literals
            base_literals = set(lit for cl in actual_clauses for lit in cl if not lit.startswith('!'))
            # For each base literal check pairs of clauses and see if they could have been resolved on that literal
            for base_lit in base_literals:
                negated_lit = '!'+base_lit
                for cl1 in actual_clauses:
                    for cl2 in actual_clauses:
                        # If these clauses cannot be resolved on this base literal, skip
                        if cl1 == cl2 or not ((base_lit in cl1 and negated_lit in cl2) or \
                                              (base_lit in cl2 and negated_lit in cl1)):
                            continue
                        # Resolve cl1 and cl2 and set result to None if resolvent is trivial
                        resolvent = set(lit for lit in list(cl1) + list(cl2) if lit != base_lit and lit != negated_lit)
                        resolvent = None if any('!' + lit in resolvent for lit in resolvent) else resolvent
                        # If nontrivial and non-redundant resolvent exists, then signal issue
                        if resolvent is not None and resolvent not in actual_clauses:
                            print(f"Clauses not saturated.")# Example: Can resolve {cl1} and {cl2} on {base_lit}")
                            # Raising an exception to break out of all loops at once.
                            # TODO: better to wrap into a function and use a return statement to make this cleaner.
                            raise ValueError
    except ValueError:
        return

    # Check 2: Check that climbing parent_dict actually leads to the original formula
    # Check for accuracy of the relevant parentdict entries along the way
    try:
        worklist = final_clauses
        leaf_clauses = []
        while worklist != []:
            elem, *rest = worklist
            if elem not in parent_dict:
                # Already a leaf
                leaf_clauses.append(elem)
                worklist = rest
            else:
                parent1, parent2, reslit = parent_dict[elem]
                # Check whether resolvent is correct. This check is optional: it can be removed.
                negated_reslit = '!' + reslit
                pcl1, pcl2 = clause_dict[parent1], clause_dict[parent2]
                if not ((reslit in pcl1 and negated_reslit in pcl2) or (reslit in pcl2 and negated_reslit in pcl1)):
                    print("clausedict entry is corrupted (code: improper resolution)")
                    raise ValueError
                resolvent = set(lit for lit in list(pcl1) + list(pcl2) if lit != reslit and lit != negated_reslit)
                if resolvent != clause_dict[elem]:
                    print("clausedict entry is corrupted (code: incorrect resolvent)")
                    raise ValueError
                # Add parents to the worklist
                worklist = rest + [parent1, parent2]
        # Once the worklist is empty, must make sure leaf clauses are the same as the original formula
        actual_leaf_clauses = [clause_dict[clid] for clid in leaf_clauses]
        if not all(cl in formula for cl in actual_leaf_clauses) and not all(cl in actual_leaf_clauses for cl in formula):
            print("Certificate does not represent a proof of the given formula")
            raise ValueError
    except ValueError:
        return

    # If all checks pass, we're in business!
    print(f"Proof object checks out! Formula is {'sat' if is_sat else 'unsat'}")



################################ FRONT END ###########################################

def format_error(string, pos, msg):
    print("Format error: "+ msg+"\n"+string+"\n"+" "*pos + "^")
    raise ValueError


def process_cnf_input(formula):
    # Process the formula into a list of sets of strings and check the format as you go along
    # If no error is caught, then formula has been processed correctly
    clauses = []
    curr_clause = None
    curr_ident = None
    expect = "lbrace"
    for i,c in enumerate(formula):
        if c.isspace() and expect != "ident":
            continue
        elif expect == "lbrace":
            if c == '{':
                curr_clause = []
                expect = 'ident'
            else:
               format_error(formula, i, "Expected {")
        elif expect == "ident":
            if curr_ident == None:
                curr_ident = ""
            if c == ';' or c == '}':
                if curr_ident == "":
                    format_error(formula, i, "Literal cannot be empty")
                curr_clause.append(curr_ident)
                curr_ident = None
                if c == '}':
                    clauses.append(curr_clause)
                    curr_clause = None
                    expect = "lbrace"
            elif c == '{':
                format_error(formula, i, "Unexpected {")
            elif c.isspace():
                if curr_ident == "":
                    continue
                else:
                    curr_clause.append(curr_ident)
                    curr_ident = None
                    expect = "ident_end"
            else:
                if curr_ident != "" and c == "!":
                    format_error(formula, i, "Must use negation symbol ! only at the beginning of the literal")
                curr_ident = curr_ident + c
        elif expect == "ident_end":
            if c == ';':
                assert curr_ident is None, "Code not behaving as expected. Lord save you." # Should always hold, just here for safety check
                expect = "ident"
            elif c == '}':
                clauses.append(curr_clause)
                curr_clause = None
                expect = "lbrace"
            else:
                format_error(formula, i, "Begin next literal with comma or close clause with } here")
        else:
            format_error(formula, i, "Unexpected")
    # End of processing loop
    # After all this it's possible that the string is in correct format, just partial
    if curr_ident is not None or curr_clause is not None:
        format_error(formula, i+1, "Formula Incomplete")
  
    # Remove duplicate literals
    clauses = [set(cl) for cl in clauses]
    # Duplicate literals are already removed because a clause is a set
    # Remove duplicate clauses
    clauses = [cl for i,cl in enumerate(clauses) if cl not in clauses[:i]]
    # Remove clauses that contain both a literal and its negation
    normalized_formula = []
    for cl in clauses:
        if any('!' + lit in cl for lit in cl):
            continue
        else:
            normalized_formula.append(cl)
    return normalized_formula



if __name__ == "__main__":
    argparser = argparse.ArgumentParser("""Resolution prover. Can be used to either interactively do a proof or to check a saved proof.

You don't need any arguments to this script for the proof mode.

For checking mode you need to call the script like so (the single quotes are important!):
python3 resolution.py --formula '{x, y} {!x, !y}' --proof '/path/to/proof.json'
Use the help menu to understand the required inputs for checking a proof.""")

    argparser.add_argument('--formula', help= "Formula in CNF. Example: {x, y, z} {!x, y, z}. ! Denotes a negated literal")
    argparser.add_argument('--proof', metavar= 'FILE', help= "Path to JSON containing the saved proof")
    args = argparser.parse_args()
    
    mode = None
    if args.formula is None and args.proof is None:
        mode = "prove"
    else:
        mode = "check"
   
    if mode == "check":
        if args.formula is None:
            print("Formula argument cannot be empty")
            raise ValueError
        normalized_formula = process_cnf_input(args.formula)
        if args.proof is None or not os.path.isfile(args.proof):
            print("Path to proof file is not valid")
            raise ValueError
        check_proof(normalized_formula, args.proof)
    else:
        # proving mode
        print("Enter the formula in CNF\nExample: {x, y, z} {!x, y, z}. ! Denotes a negated literal")
        success = False
        while not success:
            try:
                formula = input()
                normalized_formula = process_cnf_input(formula)
                success = True
            except KeyboardInterrupt:
                exit(0)
            except ValueError:
                print("Try to input the CNF formula again:")
        #print(normalized_formula)
        #exit(0)
        # Call the resolution ITP
        resolve(normalized_formula)
