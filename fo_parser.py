from collections import deque
from resolution import resolve, process_cnf_input
class Resolver:
    def __init__(self, clauses):
        self.clauses = clauses

    def find_forall_variables(self, tree, forallvalues, skolem):
        if(tree == None):
            return
        if(tree.value=='forall'):
            forallvalues.append(tree.left.value)
        if(tree.value=='exists' and tree.left.value==skolem):
            return
        self.find_forall_variables(tree.left,forallvalues,skolem)
        self.find_forall_variables(tree.right,forallvalues,skolem)
    def remove_specific_node(self, root, target_node):
        if not root:
            return None
        if root == target_node:
            return root.right

        queue = [root]
        while queue:
            current = queue.pop(0)

            if current.left == target_node:
                current.left = target_node.right
                break

            if current.right == target_node:
                current.right = target_node.right
                break

            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)

        return root

    def skolemizer(self, clause, nodes):
        
        
        print('Variables to skolemize')
        for index, i in enumerate(nodes):
            if i.value=="exists":
                forallvalues = []
                print('Skolemizing',i.left.value)
                self.find_forall_variables(clause,forallvalues,i.left.value)
                print('''choose as a function of following variables. For example: to skolemize y as a f(x) enter f x''')
                print(forallvalues)

                skolem = input()
                skolem = skolem.split(' ')
                function = skolem[0]
                variable = skolem[1]

                replace = f'{function}({variable})'
                print(f'Replacing {i.left.value} with {replace}')
                
                i.replacer(i,i.left.value,replace)
                clause = self.remove_specific_node(clause,i)
        return clause    

class Tree:
    def __init__(self):
        self.value = None
        self.left = None
        self.right = None
    def __init__(self,value):
        self.value = value
        self.left = None
        self.right = None
    def appendLeft(self, leftChild):
        self.left = leftChild
    def appendRight(self, rightChild):
        self.right = rightChild
    def appendChild(self, child):
        if self.left==None:
            self.appendChild(self,child)
        else:
            self.appendChild(self,child)
    def printTree(self,root, inorder, inorder_nodes):
        if(root == None):
            return
        self.printTree(root.left,inorder,inorder_nodes)
        inorder.append(root.value)
        inorder_nodes.append(root)
        self.printTree(root.right,inorder,inorder_nodes)
    def replacer(self, node,value, replace):
        if(node==None):
            return
        if(value in node.value):
            node.value = node.value.replace(value,replace)
        self.replacer(node.left,value,replace)
        self.replacer(node.right,value,replace)
               
    
class TreeBuilder:
    def __int__():
        print('Tree Builder')
    def check_for_errors():
        pass
    def isOperator(self, i):
        if i in ['forall','exists','and','or']:
            return True
        else:
            return False
    def isOperand(self,i):
        if i not in ['(',')']:
            return True
        else:
            return False
    def build_tree(self,clause):
        s = clause.split(' ')
        
        
        operator = deque()
        operand = deque()

        for i in s:
            if self.isOperator(i):
                operator.append(i)
            elif self.isOperand(i):
                operand.append(i)
        
        while(len(operator)!=0):
            op = operator.pop()
            op1 = operand.pop()
            op1 = Tree(op1) if isinstance(op1,str) else op1
            op2 = operand.pop()
            op2 = Tree(op2) if isinstance(op2,str) else op2

            t1 = Tree(op)
            t1.appendLeft(op2)
            t1.appendRight(op1)

            operand.append(t1)

        if(len(operand)!=1):
            print('Error! Could not parse given clause')
        op1 = operand.pop()
        t1 = Tree(op1) if isinstance(op1,str) else op1
        return t1



if __name__ == "__main__":
    treeBuilder = TreeBuilder()
    welcome = """Welcome to first order logic resolution tool. Input FO logic formulae only in terms of forall, exists, and, or and negation. Input done when done with the FO logic formulae """
    print(welcome)
    clauses = []
    clause = ""
    while (True):
        clause = input()
        if clause=='done':
            break

        clauses.append(treeBuilder.build_tree(clause))
    print('Negate and Enter target theorem(s) Example: !p(x) and !q(x) should be input !p(x) \enter !q(x)')
    targets = []
    while(True):
        s = input()
        if s =="done":
            break
        target = treeBuilder.build_tree(s)
        targets.append(target)

    
    print('Skolemization')
    skolemized_clauses = []
    r = Resolver(clauses)
    for clause in clauses:
        inorder=[]
        inorder_nodes = []
        clause.printTree(clause,inorder,inorder_nodes)
        print(inorder)

        skolemized_clauses.append(r.skolemizer(clause, inorder_nodes))
    print('Here are the skolemized clauses:')
    r = Resolver(skolemized_clauses)
    new_clauses = []
    for clause in skolemized_clauses:
        inorder_nodes = []
        clause.printTree(clause, inorder=[], inorder_nodes=inorder_nodes)
        for node in inorder_nodes:
            if node.value == 'forall':
                clause = r.remove_specific_node(clause,node)
        
        new_clauses.append(clause)
    for clause in new_clauses:
        inorder=[]
        inorder_nodes = []
        clause.printTree(clause,inorder,inorder_nodes)
        print(' '.join(inorder))
    print('and target theorem(s)')
    for target in targets:

        inorder = []
        inorder_nodes = []
        target.printTree(target, inorder, inorder_nodes)
        print(' '.join(inorder))
    
    print('Unification')
    print('Iteratively choose clauses to unify on. Press \'done\' when done')
    while (True):
        print('choose variable and what to replace it with. For example: to replace x with a, enter x a. Press \'done\' when done')
        s =  input()
        if s== 'done':
            break
        s = s.split(' ')
        
        var= s[0]
        replace= s[1]
        for clause in new_clauses:
            clause.replacer(clause,var,replace)
            inorder=[]
            inorder_nodes=[]
            clause.printTree(clause, inorder, inorder_nodes)
            print(inorder)
    clauses_to_resolve = ""
    for clause in new_clauses:
        inorder=[]
        inorder_nodes=[]
        clause.printTree(clause, inorder, inorder_nodes)
        print(inorder)

        for i, value in enumerate(inorder):
            if value=='or':
                left = inorder[i-1]
                right = inorder[i+1]
                s = f"{{{left},{right}}}"
                clauses_to_resolve+=s
    for clause in targets:
        inorder=[]
        inorder_nodes=[]
        clause.printTree(clause, inorder, inorder_nodes)
        print(inorder)

        for i, value in enumerate(inorder):
            if len(inorder)==1:
                s = f"{{{value}}}"
                clauses_to_resolve+=s
                continue
            if value=='or':
                left = inorder[i-1]
                right = inorder[i+1]
                s = f"{{{left},{right}}}"
                clauses_to_resolve+=s
    #TO-DO: find clauses combined by and
    #check user skolemized equivlent to z3 skolemized
    #to cnf
    #send it to resolution.py resolve
    print('Clauses to resolve')
    print(clauses_to_resolve)
    out = process_cnf_input(clauses_to_resolve)
    resolve(out)






