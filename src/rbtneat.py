# Represents an input and output node
class Node():
    def __init__(self, node_id, value):
        self.node_id = node_id
        self.value = value

    def __str__(self):
        return "Id: " + str(self.node_id) + "\nValue:" + str(self.value) + "\n"
# Represents a connection node
class ConnNode():
    def __init__(self, innovation):
        self.innovation = innovation

# Represents a red black tree.
class RBTree():
    def __init__(self, conn_node):
        self.red = False
        self.key = conn_node.innovation
        self.left = None
        self.right = None
        self.parent = None
        self.conn_node = conn_node

    def __str__(self):
        return "Red: " + str(self.red) + "\nKey: " + str(self.key) + "\nLeft: " + str(self.left) + "\nRight: " + str(self.right) + "\n"

    def add_right(self, rightTree):
        self.right = rightTree

    def add_left(self, leftTree):
        self.left = leftTree

    def insert(self, conn_node):
        in_tree = RBTree(conn_node)
        in_tree.red = True
        if self.key > in_tree.key:
            if self.left == None:
                in_tree.parent = self
                self.left = in_tree
                if self.red:
                    self.correction(conn_node)
            else:
                self.left.insert(conn_node)
        else:
            if self.right == None:
                in_tree.parent = self
                self.right = in_tree
                if self.red:
                    self.correction(conn_node)
            else:
                self.right.insert(conn_node)
    def correction(self):
        if self.parent.right.red & self.parent.left.red:
            self.parent.right.red = False
            self.parent.left.red = False
            self.parent.red = True
node1 = Node(2,3.3)
print node1

con_node1 = ConnNode(1)
con_node2 = ConnNode(2)
con_node3 = ConnNode(3)

tree1 = RBTree(con_node1)
tree1.insert(con_node3)
tree1.insert(con_node2)
print tree1
