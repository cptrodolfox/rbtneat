class Node():
    def __init__(self, node_id, value):
        self.node_id = node_id
        self.value = value

    def __str__(self):
        return "Id: " + str(self.node_id) + "\nValue:" + str(self.value) + "\n"

node1 = Node(2,3.3)
print node1
