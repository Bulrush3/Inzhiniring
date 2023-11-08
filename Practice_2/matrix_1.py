import json
import numpy as np

mtrx = np.load('files/matrix_60.npy')

size = len(mtrx)

matrix_stat = {}
matrix_stat['sum'] = 0
matrix_stat['avr'] = 0
matrix_stat['sumMD'] = 0
matrix_stat['avrMD'] = 0
matrix_stat['sumSD'] = 0
matrix_stat['avrSD'] = 0
matrix_stat['max'] = mtrx[0][0]
matrix_stat['min'] = mtrx[0][0]

for i in range(0, size):
    for j in range(0, size):
        matrix_stat['sum'] += mtrx[i][j]
        if i == j:
            matrix_stat['sumMD'] += mtrx[i][j]
        if i + j == size:
            matrix_stat['sumSD'] += mtrx[i][j]
        matrix_stat['min'] = min(matrix_stat['min'], mtrx[i][j])
        matrix_stat['max'] = max(matrix_stat['max'], mtrx[i][j])

matrix_stat['avr'] = matrix_stat['sum'] / (size*size)
matrix_stat['avrMD'] = matrix_stat['sumMD'] / size
matrix_stat['avrSD'] = matrix_stat['sumSD'] / size

for key in matrix_stat.keys():
    matrix_stat[key] = float(matrix_stat[key])

with open("files/matrix_stat.json", 'w') as result:
    result.write(json.dumps(matrix_stat))

norm_matrix = np.ndarray((size, size), dtype=float)

for i in range(0, size):
    for j in range(0, size):
        norm_matrix[i][j] = mtrx[i][j] / matrix_stat['sum']

np.save('files/norm_matrix', norm_matrix)


