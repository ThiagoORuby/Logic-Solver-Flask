# A Tree's node
from operator import truediv


class Node:

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def __str__(self):
        if self.data:
            return str(self.data)
 
class BinaryTree:

    def __init__(self, data = None):
        if data:
            node = Node(data)
            self.root = node
        else:
            self.root = None
    
    # Percurso em ordem simetrica esquerda-centro-direita
    # infix or inorder
    def simetric_traversal(self, node=None):
        if node is None:
            node = self.root
        if node.left:
            print('(', end = '')
            self.simetric_traversal(node.left)
        print(node, end='')
        if node.right:
            self.simetric_traversal(node.right)
            print(')', end = '')

class ExpressionTree:

    def isOperator(value):
        if (value == '∧' or
        value == "∨" or
        value == '¬' or
        value == '→'):
            return True
        return False

    # "(P∨H)∧¬H→P"
    def construct(self, exp):
        pass
    
    
if __name__ == "__main__":
    n1 = Node('P')
    n2 = Node('H')
    n3 = Node('∨')
    n4 = Node('∧')
    n5 = Node('¬')
    n6 = Node('H')
    n7 = Node('P')
    n8 = Node('→')
    
    n3.left = n1
    n3.right = n2
    n4.left = n3
    n4.right = n5
    n5.right = n6
    n8.left = n4
    n8.right = n7

    tree = BinaryTree()
    tree.root = n8

    tree.simetric_traversal()