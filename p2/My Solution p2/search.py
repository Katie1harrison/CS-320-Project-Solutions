class Node():
    def __init__(self, key):
        # print(key)
        # print(type(key))
        self.key = key
        self.values = []
        self.left = None
        self.right = None
    def __len__(self):
        size = len(self.values)
        if self.left != None:
            size += len(self.left)
        if self.right != None:
             size += len(self.right)
        return size
    def lookup(self,key):
        if key == self.key:
            return self.values
        elif key < self.key and self.left != None:
            return self.left.lookup(key)
        elif key > self.key and self.right != None:
            return self.right.lookup(key)
        else:
            return []
    def __getitem__(self,key):
        return self.lookup(key)
    
    def better_dump(self, prefix="", suffix=""):
        print(prefix, self.key, suffix)
        if self.left != None:
            self.left.better_dump(prefix+"\t", "(LEFT)")
        if self.right != None:
            self.right.better_dump(prefix+"\t", "(RIGHT)")


        
        
class BST():
    def __init__(self):
        self.root = None

    def add(self, key, val):
        if self.root == None:
            self.root = Node(key)

        curr = self.root
        while True:
            if key < curr.key:
                # go left
                if curr.left == None:
                    curr.left = Node(key)
                curr = curr.left
            elif key > curr.key:
                 # go right
                if curr.right == None:
                    curr.right = Node(key)
                curr = curr.right
            else:
                # found it!
                assert curr.key == key
                break

        curr.values.append(val)
    def __dump(self, node):
        if node == None:
            return
        self.__dump(node.right)            # 1
        print(node.key, ":", node.values)  # 2
        self.__dump(node.left)            # 3

    def dump(self):
        self.__dump(self.root)
          
    def lookup(self,key):
        return self.root.lookup(key)
    
    def __getitem__(self,key):
        return self.lookup(key)
    
    
        
t = BST()
t.add("B", 3)
assert len(t.root) == 1
t.add("A", 2)
assert len(t.root) == 2
t.add("C", 1)
assert len(t.root) == 3
t.add("C", 4)
assert len(t.root) == 4
  
    