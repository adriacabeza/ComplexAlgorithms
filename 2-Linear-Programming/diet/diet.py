# python3
import copy
import itertools


class Equation:
	def __init__(self, a, b):
		self.a = a
		self.b = b


class Position:
	def __init__(self, row, column):
		self.column = column
		self.row = row


def select_pivot(pivot, a, used_rows):
	while used_rows[pivot.row] or a[pivot.row][pivot.column] == 0:
		pivot.row += 1
		if pivot.row == len(a):
			return None
	return pivot


def swap_lines(a, b, used_rows, pivot_element):
	a[pivot_element.column], a[pivot_element.row] = a[pivot_element.row], a[pivot_element.column]
	b[pivot_element.column], b[pivot_element.row] = b[pivot_element.row], b[pivot_element.column]
	used_rows[pivot_element.column], used_rows[pivot_element.row] = used_rows[pivot_element.row], used_rows[
		pivot_element.column]
	pivot_element.row = pivot_element.column


def process_pivot(a, b, pivot, used_rows):
	scale = a[pivot.row][pivot.column]
	if scale != 1:
		for i in range(len(a)):
			a[pivot.row][i] /= scale
		b[pivot.row] /= scale
	for i in range(len(a)):
		if i != pivot.row:
			multiple = a[i][pivot.column]
			for j in range(len(a)):
				a[i][j] -= a[pivot.row][j] * multiple
			b[i] -= b[pivot.row] * multiple
	used_rows[pivot.row] = True


def gaussian_elimination(subset, equation):
	# make equation
	a = []
	b = []
	for i in subset:
		a.append(copy.deepcopy(equation.a[i]))
		b.append(copy.deepcopy(equation.b[i]))
	# solve equation
	size = len(a)
	used_rows = [False] * size
	for i in range(size):
		pivot_element = Position(0, i)
		pivot_element = select_pivot(pivot_element, a, used_rows)
		if not pivot_element:
			return None
		# print(pivot_element.row, pivot_element.column)
		swap_lines(a, b, used_rows, pivot_element)
		process_pivot(a, b, pivot_element, used_rows)
	return b


def check_solution(solution, equation, m):
	for i in range(len(equation.a)):
		sum = 0
		for j in range(m):
			sum += equation.a[i][j] * solution[j]
		if sum - equation.b[i] > 0.00001:
			return False
	return True


def solve(subsets, equation, pleasure, m):
	solutions = []
	for subset in subsets:
		solution = gaussian_elimination(subset, equation)
		if solution is not None:
			if check_solution(solution, equation, m):
				solutions.append(solution)
	if not solutions:
		print('No solution')
	else:
		best = float('-inf')
		result = None
		for s in solutions:
			p = 0
			for i in range(m):
				p += pleasure[i] * s[i]
			if p > best:
				best = p
				result = s
		temp = 0
		for e in result:
			temp += e
		#print(temp)
		if temp > 1000000000:
			print('Infinity')
		else:
			print('Bounded solution')
			for e in result:
				print("{0:.18f}".format(e), end=' ')


def print_column(column):
	for value in column:
		print("%.20lf" % value)


def combinations(n, m):
	lst = list(range(n + m + 1))
	subsets = list(map(set, itertools.combinations(lst, m)))
	return subsets


def read_data():
	n, m = map(int, input().split())
	a = list()
	for _ in range(n):
		a.append(list(map(int, input().split())))
	b = list(map(int, input().split()))

	pleasure = list(map(int, input().split()))
	# setting variables to be non negative
	for i in range(m):
		lst = [0] * m
		lst[i] = -1
		a.append(lst)
		b.append(0)
	#setting the upperbound
	a.append([1] * m)
	b.append(1000000001)
	#print('A:{}'.format(a))
	#print('B:{}'.format(b))
	subsets = combinations(n, m)
	equation = Equation(a, b)
	return equation, pleasure, subsets, m


if __name__ == '__main__':
	matrix, pleasure, subsets, m = read_data()
	solution = solve(subsets, matrix, pleasure, m)
	exit(0)
