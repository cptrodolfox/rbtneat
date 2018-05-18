
class Node():
    def __init__(self, key=None, value=None, color= False):
        self.key = key
        self.value = value
        self.left = self.right = self.parent = None
        self.color = color

    def __str__(self):
        return str(self.__dict__)

    # def __eq__(self, other):
    #     return self.__dict__ == other.__dict__

    def search(self,key):
        if self.key is None:
            return None
        if self.key == key:
            return self
        if key < self.key:
            return self.left.search(key)
        else:
            return self.right.search(key)

    def get(self,key):
        if self.key is None:
            return None
        if self.key == key:
            return self.value
        if key < self.key:
            return self.left.get(key)
        else:
            return self.right.get(key)

    def keys(self):
        keys = []
        cur = self.firstNode()
        while cur.key is not None:
            keys.append(cur.key)
            # print("-----------------------------------")
            # print(cur)
            # print("-----------------------------------")
            cur = self.nextNode(cur)
        return keys

    def firstNode(self):
        cur = self
        while cur.left.key is not None:
            cur = cur.left
        return cur
    
    def nextNode(self, prev):
        cur = prev
        if cur.right.key is not None:
            cur = prev.right
            # print("-----------------------------------")
            # print("if cur")
            # print(cur)
            # print("-----------------------------------")
            while cur.left.key is not None:
                cur = cur.left
            return cur
        while 1:
            cur = cur.parent
            # print("-----------------------------------")
            # print("while cur")
            # print(cur)
            # print("-----------------------------------")
            if not cur:
                return Node()
            if cur.key >= prev.key:
                return cur

    def values(self):
        values = []
        cur = self.firstNode()
        while cur.key is not None:
            values.append(cur.value)
            cur = self.nextNode(cur)
        return values

class RBTreeIter(object):

    def __init__ (self, tree):
        self.tree = tree
        self.index = -1  # ready to iterate on the next() call
        self.node = None
        self.stopped = False

    def __iter__(self):
        """ Return the current item in the container
        """
        return self.node.value

    def __next__(self):
        """ Return the next item in the container
            Once we go off the list we stay off even if the list changes
        """
        if self.stopped or (self.index + 1 >= self.tree.__len__()):
            self.stopped = True
            raise StopIteration
        #
        self.index += 1
        if self.index == 0:
            self.node = self.tree.firstNode()
        else:
            self.node = self.tree.nextNode (self.node)
        return self.node.value

class RBTree:
    def __init__(self):
        self.sentinel = Node()
        self.sentinel.left = self.sentinel.right = self.sentinel
        self.root = self.sentinel
        self.count = 0

    def __len__(self):
        return self.count

    # def __iter__(self):
    #     return RBTreeIter(self)
    
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.sentinel:
            y.left.parent = x
        if y != self.sentinel:
            y.parent = x.parent
        if x.parent:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        else:
            self.root = y
            
        y.left = x
        if x != self.sentinel:
            x.parent = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.sentinel:
            x.right.parent = y
        if x != self.sentinel:
            x.parent = y.parent
        if y.parent:
            if y == y.parent.right:
                y.parent.right = x
            else:
                y.parent.left = x
        else: 
            self.root = x

        x.right = y
        if y != self.sentinel:
            y.parent = x

    def insert(self, key, value):
        self.delete(self.search(key))
        parent = None
        cur = self.root
        # print("-------------------------------------------------")
        # print("root: ")
        # print(cur)
        # print("-------------------------------------------------")
        while cur != self.sentinel:
            parent = cur
            if key < cur.key:
                cur = cur.left
            else:
                cur = cur.right
        x = Node(key, value)
        x.left = x.right = self.sentinel
        x.parent = parent
        x.color = True

        self.count = self.count + 1 

        if parent:
            if key < parent.key:
                parent.left = x
            else:
                parent.right = x
        else:
            self.root = x
        # print("-------------------------------------------------")
        # print("x: ")
        # print(x)    
        # print("-------------------------------------------------")
        self.fixup_insert(x)

    def fixup_insert(self,z):
        while z != self.root and z.parent.color == True:
            # print("----------------------------------------------------")
            # print(z.parent)
            # print(z.parent.parent)
            # print(z.parent.parent.left)
            # print("----------------------------------------------------")
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
                # if z.parent == z.parent.parent.right:
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
        if self.root != self.sentinel:
            return self.root.search(key)
        else:
            return None

    def firstNode(self):
        cur = self.root
        while cur.left.key is not None:
            cur = cur.left
        return cur

    def nextNode(self, prev):
        """returns None if there isn't one"""
        cur = prev
        if cur.right.key is not None:
            cur = prev.right
            while cur.left is not None:
                cur = cur.left
            return cur
        while 1:
            cur = cur.parent
            if not cur:
                return Node()
            if cur.key >= prev.key:
                return cur

    def get(self, key):
        if self.root != self.sentinel:
            return self.root.get(key)
        else:
            return None 

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
        
        if not z or z == self.sentinel:
            return    

        if z.left == self.sentinel or z.right == self.sentinel:
            y = z
        else:
            y = z.right
            while y.left != self.sentinel:
                y = y.left

        if y.left != self.sentinel:
            x = y.left
        else:
            x = y.right

        x.parent = y.parent
        if y.parent:
            if y == y.parent.left:
                y.parent.left = x
            else:
                y.parent.right = x
        else:
            self.root = x

        if y != z:
            z.key = y.key
            z.value = y.value

        if y.color == False:
            self.fixup_delete(x)

        del y
        self.count = self.count - 1

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
                else:
                    if w.right.color == False:
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
                else:
                    if w.left.color == False:
                        w.right.color = False
                        w.color = True
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = w.parent.color
                    w.parent.color = False
                    w.left.color = False
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = False
                
    def keys(self):
        return self.root.keys()

    def values(self):
        return self.root.values()

    def items(self):
        return zip(self.keys(), self.values())
            
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

    


# Testing of the RBTree Implementation
# T = RBTree()

# T.insert(1,1)
# T.insert(2,2)
# T.insert(3,3)
# T.insert(4,4)
# T.insert(5,5)
# T.insert(6,6)
# T.insert(7,7)
# T.insert(8,8)
# T.insert(9,9)

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
