import os
import numpy as np

matrix = np.load('files/matrix_60_2.npy')

size = len(matrix)

x = list()
y = list()
z = list()

limit = 560

for i in range(0, size):
    for j in range(0, size):
        if matrix[i][j] > limit:
            x.append(i)
            y.append(j)
            z.append(matrix[i][j])

np.savez("files/points", x=x, y=y, z=z)
np.savez_compressed("files/points_zip", x=x, y=y, z=z)

print(f"points     = {os.path.getsize('files/points.npz')}")
print(f"points_zip = {os.path.getsize('files/points_zip.npz')}")




