-- 1. head' возвращает первый элемент непустого списка (0,5 балла)
head' :: [a] -> a
head' [x] = x
head' (x : xs) = x

-- 2. tail' возвращает список без первого элемента, для пустого - пустой (0,5)
tail' :: [a] -> [a]

tail' [] = []
tail' [x] = []
tail' (x : xs) = xs

-- 3. take' возвращает первые n >= 0 элементов исходного списка (0,5)
take' :: Int -> [a] -> [a]
take' 0 a = []
take' n a = ((head' a) : (take' (n - 1) (tail' a)))

-- 4. drop' возвращает список без первых n >= 0 элементов; если n больше длины
-- списка, то пустой список. (0,5)
drop' :: Int -> [a] -> [a]
drop' 0 a = a
drop' n a = drop' (n - 1) (tail' a)

is_positive :: Int -> Bool
is_positive x = x > 0

-- 5. filter' возвращает список из элементов, для которых f возвращает True (0,5)
filter' :: (a -> Bool) -> [a] -> [a]
filter' f xs = [x | x <- xs, f(x)]

-- 6. foldl' последовательно применяет функцию f к элементу списка l и значению,
-- полученному на предыдущем шаге, начальное значение z (0,5)
-- foldl' (+) 0 [1, 2, 3] == (((0 + 1) + 2) + 3)
-- foldl' (*) 4 [] == 4
foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' f z [] = z
foldl' f z l = foldl' (f) (f z (head' l)) (tail' l) 

-- 7. concat' принимает на вход два списка и возвращает их конкатенацию (0,5)
-- concat' [1,2] [3] == [1,2,3]
concat' :: [a] -> [a] -> [a]
concat' [] xs = xs
concat' xs [] = xs
concat' (x : xs) y = x : (concat' xs y)

-- 8. quickSort' возвращает его отсортированный список (0,5)
-- quickSort' должен быть реализован через алгоритм QuickSort
-- (выбор pivot может быть любым)

quickSort' :: Ord a => [a] -> [a]
quickSort' [] = []
quickSort' [x] = [x]
quickSort' (x : xs) = concat' (quickSort' (filter' (< x) xs)) (concat' [x] (quickSort' (filter' (>= x) xs)))