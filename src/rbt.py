
class Node:
    def __init__(self, key=None, value=None, color= False):
        self.key = key
        self.value = value
        self.left = self.right = self.parent = None
        self.color = color

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def search(self,key):
        if self.key is None or self.key == key:
            return self
        if key < self.key:
            return self.left.search(key)
        else:
            return self.right.search(key)

    def keys(self):
        keys = []
        if self.key is None:
            return keys
        else:
            keys.append(self.key)
            if self.left is not None:
                keys.extend(self.left.keys())
            if self.right is not None:
                keys.extend(self.right.keys())
            return keys

    def values(self):
        values = []
        if self.value is None:
            return values
        else:
            values.append(self.value)
            if self.left is not None:
                values.extend(self.left.values())
            if self.right is not None:
                values.extend(self.right.values())
            return values

    def items(self):
        return zip(self.keys(), self.values())

class RBTree:
    def __init__(self):
        self.sentinel = Node()
        self.root = self.sentinel
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.sentinel:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.sentinel:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.sentinel:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == self.sentinel:
            self.root = x
        elif y == y.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        x.right = y
        y.parent = x

    def insert(self, z):
        y = self.sentinel
        x = self.root
        while x != self.sentinel:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == self.sentinel:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = self.sentinel
        z.right = self.sentinel
        z.color = True
        self.fixup_insert(z)

    def fixup_insert(self,z):
        while z.parent.color == True:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == True:
                    z.parent.color = False
                    y.color = False
                    z.parent.parent.color = True
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = False
                    z.parent.parent.color = True
                    self.right_rotate(z.parent.parent)
            else:
                if z.parent == z.parent.parent.right:
                    y = z.parent.parent.left
                    if y.color == True:
                        z.parent.color = False
                        y.color = False
                        z.parent.parent.color = True
                        z = z.parent.parent
                    else:
                        if z == z.parent.left:
                            z = z.parent
                            self.right_rotate(z)
                        z.parent.color = False
                        z.parent.parent.color = True
                        self.left_rotate(z.parent.parent)
        self.root.color = False

    def transplant(self, u, v):
        if u.parent == self.sentinel:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def search(self, key):
        if self.root == self.sentinel:
            return self.root
        else:
            return self.root.search(key)

    def minimum(self, z):
        minimum = self.search(z.key)
        while minimum.left != self.sentinel:
            minimum = minimum.left
        return minimum

    def maximum(self, z):
        maximum = self.search(z.key)
        while maximum.right != self.sentinel:
            maximum = maximum.right
        return maximum

    def delete(self,z):
        y = z
        y_original_color = y.color
        if z.left == self.sentinel:
            x = z.right
            self.transplant(z,z.right)
        elif z.right == self.sentinel:
            x = z.left
            self.transplant(z,z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(z,y)
                y.right = z.right
                y.right.parent = y
            self.transplant(z,y)
            y.left = z.left
            y.left.p = y
            y.color = z.color
        if y_original_color == False:
            self.fixup_delete(x)

    def fixup_delete(self,x):
        while x != self.root and x.color == False:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == True:
                    w.color = False
                    x.parent.color = True
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == False and w.right.color == False:
                    w.color = True
                    x = x.parent
                elif w.right.color == False:
                    w.left.color = False
                    w.color = True
                    self.right_rotate(w)
                    w = x.parent.right
                w.color = x.parent.color
                x.parent.color = False
                w.right.color = False
                self.left_rotate(x.parent)
                x = self.root
            else:
                w = x.parent.left
                if w.color == True:
                    w.color = False
                    x.parent.color = True
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == False and w.left.color == False:
                    w.color = True
                    x = x.parent
                elif w.left.color == False:
                    w.right.color = False
                    w.color = True
                    self.right_rotate(w)
                    w = x.parent.right
                w.color = w.parent.color
                w.parent.color = False
                w.left.color = False
                self.left_rotate(x.parent)
                x = self.root
            x.color = False
                
    def keys(self):
        if self.root != self.sentinel:
            return self.root.keys()

    def values(self):
        if self.root != self.sentinel:
            return self.root.values()

    def items(self):
        if self.root != self.sentinel:
            return self.root.items()
            
    def __str__(self):
        if self.root == self.sentinel:
            return str(self.root)
        else:
            output = "Sentinel: " + str(self.sentinel) + "\n"
            output = output + "Root: " + str(self.root) + "\n"
            if self.root.left != self.sentinel:
                output = output + "Left: " + str(self.root.left) + "\n"
            if self.root.right != self.sentinel:
                output = output + "Right: " + str(self.root.right) + "\n"
        return output

    


## Testing of the RBTree Implementation
T = RBTree()
node1 = Node(1,1)
node2 = Node(2,2)
node3 = Node(3,3)
node4 = Node(4,4)
node5 = Node(5,5)
node6 = Node(6,6)
node7 = Node(7,7)
node8 = Node(8,8)
node9 = Node(9,9)


# T.insert(node1)
# T.insert(node2)
# T.insert(node3)
# T.insert(node4)
# T.insert(node5)
# T.insert(node6)
# T.insert(node7)
# T.insert(node8)
# T.insert(node9)

# print(T)

# print("node 4\n")
# print(T.root)

# print("node 2\n")
# print(T.root.left)

# print("node 6\n")
# print(T.root.right)

# print("node 1\n")
# print(T.root.left.left)

# print("node 3\n")
# print(T.root.left.right)

# print(T.root.right.left)
# print(T.root.right.right)
# print(T.root.right.right.left)
# print(T.root.right.right.right)

# print("Keys: ")
# print(T.keys())

# print("Values: ")
# print(T.values())

# print("Minimum :")
# print(T.minimum(T.root.right))

# print("Maximum :")
# print(T.maximum(T.root.right))
