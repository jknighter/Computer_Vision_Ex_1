import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2


# def gauss(x, sigma):
#     # Your code here
#     x[:] = 1 / (np.sqrt(2 * np.pi) * sigma) * np.power(np.e, (-np.square(x[:]) / (2 * np.square(sigma))))
#     return x
#
#
# x = np.zeros((100, 3))
# x.fill(1)
# y = gauss(x, 1.0)
# fig, ax = plt.subplots()
# ax.plot(x, y)
# plt.show()

# a = np.array([[5, 6],
#               [2, 3],
#               [3, 4],
#               [6, 7]])
# b = np.array([[1, 2, 3], [4, 5, 6]])
# print(a.shape)
# # b = np.array([1,2])
# a = np.pad(a, pad_width=((2,2), (0,0)), mode="constant", constant_values=0)
# # print(np.dot(a,b))
# print(a)

# x, y = np.meshgrid(np.linspace(-1,1,10), np.linspace(-1,1,10))
# d = np.sqrt(x*x+y*y)
# print(d)

# M = np.array([[1,2],[3,4],[5,6],[7,8],[9,10],[11,12]])
# print(M[1::2])

a = np.arange(1, 10)
print(a[a == 5])
