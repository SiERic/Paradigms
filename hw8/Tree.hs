import Prelude hiding (lookup)

-- Implement a binary search tree (4 points)

data BinaryTree k v = Nil | Node k v (BinaryTree k v) (BinaryTree k v) deriving Show

-- “Ord k =>” requires, that the elements of type k are comparable
-- Takes a key and a tree and returns Just value if the given key is present,
-- otherwise returns Nothing
lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup key Nil = Nothing
lookup key (Node k v l r) | key < k   = lookup key l
                          | key == k  = Just v
                          | key > k   = lookup key r

-- Takes a key, value and tree and returns a new tree with key/value pair inserted.
-- If the given key was already present, the value is updated in the new tree.
insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert k v Nil = Node k v Nil Nil
insert key value (Node k v l r) | key < k   = Node k v (insert key value l) r
                                | key == k  = Node k v l r
                                | key > k   = Node k v l (insert key value r) 

merge :: BinaryTree k v -> BinaryTree k v -> BinaryTree k v
merge Nil t = t
merge (Node k v l r) t = Node k v l (merge r t)

-- Returns a new tree without the given key
delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete key Nil = Nil 
delete key (Node k v l r) | key < k   = Node k v (delete key l) r
                          | key == k  = merge l r
                          | key > k   = Node k v l (delete key r)
