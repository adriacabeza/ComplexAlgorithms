# python3
# useful link: https://www.csie.ntu.edu.tw/~lyuu/complexity/2011/20111018.pdf

import itertools

n, m = map(int, input().split())
edges = [list(map(int, input().split())) for i in range(m)]

clauses = list()
for i in range(1, n+1):
	# Each node must appear once
	# X_{1,j} V X_{2,j} V X_{3,j} ... X_{n,j} for all j <= n
	Xij = [j for j in range((i-1) * n + 1, i * n + 1)]
	clauses.append(Xij)
	# No nodes appear twice
	# -X_{i,j} V -X_{k,j} for all i,j,k s.t. i != k
	negative_literals = list(map(lambda x: -x, Xij))
	clauses += list(map(list, itertools.combinations(negative_literals, 2)))

for i in range(1, n+1):
	# Every position i on the path must be occupied
	# X_{i,1} V X_{i,2} V X_{i,3} ...V X_{i,n}
	Xij = [j for j in range(i, n * n + i, n)]
	# No two nodes j and k occupy the same position in the path
	# -X_{i,j} V -X_{i,k} for all i,j,k s.t. j!=k
	clauses.append(Xij)
	negative_literals = list(map(lambda x: -x, Xij))
	clauses += list(map(list, itertools.combinations(negative_literals,2 )))


lst = list(i for i in range(1, n + 1))
subsets = list(map(list, itertools.combinations(lst, 2)))
# Non adjacent nodes can't be adjacent in the path
# -X_{k,i} V -X_{k+1,j} for all (i,j) in E and k=1,2,3,4...n-1
for u, v in subsets:
	if [u, v] not in edges and [v, u] not in edges:
		for i in range(1, n):
			clauses.append([-((u - 1) * n + i), -((v - 1) * n + i + 1)])
			clauses.append([-((v - 1) * n + i), -((u - 1) * n + i + 1)])


n_clauses = len(clauses)
n_variables = n**2
print(n_clauses, n_variables)

for clause in clauses:
	for literal in clause:
		print(literal, end=' ')
	print(0)