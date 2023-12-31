def Matrix_sum(A, B, n):
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = A[i][j] + B[i][j]
    return result
def multiplyMatrices(matrix, B_Matrix, n):
    Result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            Result[i][j] = 0
            for k in range(n):
                Result[i][j] += matrix[i][k] * B_Matrix[k][j]
    return Result   #нужно
def transpose(matrix, n):
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    return matrix
def minor(matrix, n, i, j):
    temp = [[0] * (n - 1) for _ in range(n - 1)]
    a, b = 0, 0
    for k in range(n):
        if k != i:
            for l in range(n):
                if l != j:
                    temp[a][b] = matrix[k][l]
                    b += 1
                    if b == n - 1:
                        b = 0
                        a += 1
    return temp
def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))
def deter(matrix, n):
    det = 0
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]

    for j in range(n):
        temp = [[0] * (n - 1) for _ in range(n - 1)]
        a, b = 0, 0
        for k in range(1, n):
            for l in range(n):
                if l != j:
                    temp[a][b] = matrix[k][l]
                    b += 1
            a += 1
            b = 0
        det += (-1) ** j * matrix[0][j] * deter(temp, n - 1)
    return det
def opositMatrix(matrix, n):
    oposit = [[0] * n for _ in range(n)]
    det = deter(matrix, n)
    if det == 0:
        print("\nInverse matrix does not exist!\n")
        return None
    else:
        for i in range(n):
            for j in range(n):
                minorMatrix = minor(matrix, n, i, j)
                oposit[i][j] = (-1) ** (i + j) * deter(minorMatrix, n - 1)
        return oposit #нужно


def rank(matrix):
    # Function to perform Gaussian elimination
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])

        for pivot_row in range(min(rows, cols)):
            # Find the pivot element
            pivot = matrix[pivot_row][pivot_row]

            # If pivot is zero, swap with a non-zero row below
            if pivot == 0:
                for i in range(pivot_row + 1, rows):
                    if matrix[i][pivot_row] != 0:
                        matrix[pivot_row], matrix[i] = matrix[i], matrix[pivot_row]
                        break
                    # If no non-zero pivot is found, move to the next column
                    if i == rows - 1:
                        pivot_row += 1

            # Reduce the rows below the pivot row
            for i in range(pivot_row + 1, rows):
                ratio = matrix[i][pivot_row] / pivot
                for j in range(cols):
                    matrix[i][j] -= ratio * matrix[pivot_row][j]

        return matrix

    # Perform Gaussian elimination on the matrix
    reduced_matrix = gaussian_elimination([row.copy() for row in matrix])

    # Count non-zero rows, which gives the rank of the matrix
    rank = sum(1 for row in reduced_matrix if any(row))

    return rank
