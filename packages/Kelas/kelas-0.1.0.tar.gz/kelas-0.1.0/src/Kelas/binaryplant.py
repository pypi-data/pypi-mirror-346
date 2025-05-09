def Quicksort():
    print("""FUNCTION quicksort(array)
IF length(array) ≤ 1 THEN
RETURN array
END IF
pivot ← array[length(array)/2]
left ← [x FOR x IN array IF x < pivot]
middle ← [x FOR x IN array IF x = pivot]
right ← [x FOR x IN array IF x > pivot]
RETURN concatenate(quicksort(left), middle, quicksort(right))
END FUNCTION
""")
    
def Krushal_find():
    print("""CLASS Graph
ATTRIBUTES:
V: integer (number of vertices)
edges: list of (u, v, weight) tuples
METHOD kruskal():
result ← empty list
sort edges by weight
parent ← array where parent[i] = i
rank ← array of zeros
FOR EACH edge IN edges:
u_root ← find(parent, edge.u)
v_root ← find(parent, edge.v)
IF u_root ≠ v_root THEN
ADD edge TO result
union(parent, rank, u_root, v_root)
END IF
END FOR
RETURN result
END METHOD
METHOD find(parent, i):
WHILE parent[i] ≠ i:
i ← parent[i]
END WHILE
RETURN i
END METHOD
METHOD union(parent, rank, x, y):
x_root ← find(parent, x)
y_root ← find(parent, y)
IF rank[x_root] < rank[y_root]:
parent[x_root] ← y_root
ELSE IF rank[x_root] > rank[y_root]:
parent[y_root] ← x_root
ELSE:
parent[y_root] ← x_root
rank[x_root] ← rank[x_root] + 1
END IF
END METHOD
END CLASS
""")
    
def QuickFind():
    print("""CLASS QuickFind
ATTRIBUTES:
id: array of integers
CONSTRUCTOR(size):
id ← array where id[i] = i for all i in 0..size-1
END CONSTRUCTOR
METHOD find(p):
RETURN id[p]
END METHOD
METHOD union(p, q):
pid ← id[p]
qid ← id[q]
FOR i FROM 0 TO length(id)-1:
IF id[i] = pid THEN
id[i] ← qid
END IF
END FOR
END METHOD
END CLASS
""")
    
def Quick_Union():
    print("""CLASS QuickUnion
ATTRIBUTES:
id: array of integers
CONSTRUCTOR(size):
id ← array where id[i] = i for all i in 0..size-1
END CONSTRUCTOR
METHOD find(p):
WHILE p ≠ id[p]:
p ← id[p]
END WHILE
RETURN p
END METHOD
METHOD union(p, q):
p_root ← find(p)
q_root ← find(q)
IF p_root = q_root THEN
RETURN
END IF
id[p_root] ← q_root
END METHOD
END CLASS""")
    
def LinkedList():
    print("""// Define a Node structure
STRUCTURE Node
DATA data
POINTER next
END STRUCTURE
// Define the Linked List
STRUCTURE SinglyLinkedList
POINTER head // Points to the first node
END STRUCTURE
// Function to append a new node at the end
FUNCTION append(SinglyLinkedList list, DATA value)
newNode = CREATE Node WITH data = value, next = NULL
IF list.head == NULL THEN
list.head = newNode
RETURN
END IF
current = list.head
WHILE current.next != NULL DO
current = current.next
END WHILE
current.next = newNode
END FUNCTION
// Function to prepend a new node at the beginning
FUNCTION prepend(SinglyLinkedList list, DATA value)
newNode = CREATE Node WITH data = value, next = list.head
list.head = newNode
END FUNCTION
// Function to insert after a specific node
FUNCTION insertAfter(Node prevNode, DATA value)
IF prevNode == NULL THEN
PRINT "Previous node cannot be null"
RETURN
END IF
newNode = CREATE Node WITH data = value, next = prevNode.next
prevNode.next = newNode
END FUNCTION
// Function to delete a node by value
FUNCTION deleteNode(SinglyLinkedList list, DATA value)
current = list.head
prev = NULL
// Case: node to delete is head
IF current != NULL AND current.data == value THEN
list.head = current.next
FREE current
RETURN
END IF
// Search for the node to delete
WHILE current != NULL AND current.data != value DO
prev = current
current = current.next
END WHILE
// If value not found
IF current == NULL THEN
RETURN
END IF
// Unlink the node
prev.next = current.next
FREE current
END FUNCTION
""")
    
def BinaryTree():
    print("""STRUCT Node
DATA value
POINTER left, right
END STRUCT
FUNCTION insert(root, value)
IF root == NULL
RETURN CREATE_NODE(value)
IF value < root.value
root.left = insert(root.left, value)
ELSE
root.right = insert(root.right, value)
RETURN root
END FUNCTION""")
    
def BinarySearchTree():
    print("""FUNCTION search(root, key)
IF root == NULL OR root.value == key
RETURN root
IF key < root.value
RETURN search(root.left, key)
ELSE
RETURN search(root.right, key)
END FUNCTION""")
    
def AVLTree():
    print("""FUNCTION rotateRight(y)
x = y.left
T = x.right
x.right = y
y.left = T
UPDATE_HEIGHTS(y, x)
RETURN x
END FUNCTION
FUNCTION insert(root, value)
STANDARD_BST_INSERT(root, value)
balance_factor = GET_BALANCE(root)
// Perform rotations if unbalanced
IF balance_factor > 1
IF value < root.left.value
RETURN rotateRight(root)
ELSE
root.left = rotateLeft(root.left)
RETURN rotateRight(root)
END FUNCTION""")
    
def RedBlackTree():
    print("""FUNCTION insertFixup(z)
WHILE z.parent.color == RED
IF z.parent == z.parent.parent.left
y = z.parent.parent.right
IF y.color == RED
RECOLOR(z.parent, y, z.parent.parent)
z = z.parent.parent
ELSE
IF z == z.parent.right
z = z.parent
rotateLeft(z)
RECOLOR_AND_ROTATE_RIGHT(z)
root.color = BLACK
END FUNCTION""")
    
def BTree():
    print("""FUNCTION insertNonFull(node, key)
i = node.key_count - 1
IF node.leaf
WHILE i >= 0 AND key < node.keys[i]
node.keys[i+1] = node.keys[i]
i--
node.keys[i+1] = key
node.key_count++
ELSE
WHILE i >= 0 AND key < node.keys[i]
i--
i++
IF node.children[i].key_count == 2t-1
SPLIT_CHILD(node, i)
IF key > node.keys[i]
i++
insertNonFull(node.children[i], key)
END FUNCTION""")
    
def HashTable():
    print("""DEFINE HashTable:
SIZE ← 10
table ← array of SIZE empty lists
FUNCTION hash(key):
RETURN key MOD SIZE
FUNCTION insert(key, value):
index ← hash(key)
FOR each (k, v) in table[index]:
IF k == key:
v ← value // Update existing key
RETURN
ADD (key, value) TO table[index]
FUNCTION search(key):
index ← hash(key)
FOR each (k, v) in table[index]:
IF k == key:
RETURN v
RETURN "Not Found"
FUNCTION delete(key):
index ← hash(key)
FOR each (k, v) in table[index]:
IF k == key:
REMOVE (k, v) FROM table[index]
RETURN "Deleted"
RETURN "Key not found"
insert(15, "Apple") // hash(15) = 5
insert(25, "Banana") // hash(25) = 5 → collision, stored in same list
insert(7, "Grape") // hash(7) = 7
search(25) // → returns "Banana"
delete(15) // → removes "Apple"
search(15) // → returns "Not Found""")
    
def Fisher_Yates_Algorithm():
    print("""import random
def fisher_yates_shuffle(arr):
n = len(arr)
for i in range(n-1, 0, -1):
j = random.randint(0, i)
arr[i], arr[j] = arr[j], arr[i]
return arr""")
    
def InsertionSort():
    print("""def insertion_sort(arr):
for i in range(1, len(arr)):
key = arr[i]
j = i - 1
while j >= 0 and arr[j] > key:
arr[j+1] = arr[j]
j -= 1
arr[j+1] = key
Then print and write your output result
""")