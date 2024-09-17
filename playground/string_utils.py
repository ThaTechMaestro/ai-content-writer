# import deque
from collections import deque 
a = [1,2,5,4]
a.sort()
print(a)

N= 5
queue = deque()

for i in range(N):
    queue.append(i)

print(queue)
queue.popleft()
print(queue)
queue.pop()
print(queue)

print((2 + 3) / 2)