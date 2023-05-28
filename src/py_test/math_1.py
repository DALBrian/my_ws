import numpy as np
a = np.zeros([3,3])


element = 0
for i in range(3):
    for j in range(3):
        a[i][j] = element
        element += 1
print(a)
for i in range(3):
    b = sum([(a[i][j]) ** 2 for j in range(i) ])
    c = [a[i][j] **2 for j in range(i)]
    print(c)
print(b)




# for i in range(3):
#     print("i = ", i)
#     print("j = ", j for j in range(i))