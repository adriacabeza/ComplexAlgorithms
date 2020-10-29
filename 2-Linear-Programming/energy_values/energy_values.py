# python3

class Equation:
	def __init__(self, a, b):
		self.a = a
		self.b = b


class Position:
	def __init__(self, row,  column):
		self.column = column
		self.row = row


def select_pivot(pivot, a, used_rows):
	while used_rows[pivot.row] or a[pivot.row][pivot.column] == 0:
		pivot.row += 1
	if pivot.row == len(a):
		return False
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


def solve_equation(equation):
	a = equation.a
	b = equation.b
	size = len(a)
	used_rows = [False] * size
	for i in range(size):
		pivot_element = Position(0, i)
		pivot_element = select_pivot(pivot_element, a, used_rows)
		if not pivot_element:
			return None
		#print(pivot_element.row, pivot_element.column)
		swap_lines(a, b, used_rows, pivot_element)
		process_pivot(a, b, pivot_element, used_rows)
		#print('a:{}'.format(a), 'b:{}'.format(b))
	return b


def print_column(column):
	for value in column:
		print("%.20lf" % value)


def read_data():
	n = int(input())
	a = list()
	b = list()
	for _ in range(n):
		information = list(map(int, input().split()))
		a.append(information[:n])
		b.append(information[-1])
	return Equation(a, b)


if __name__ == '__main__':
	matrix = read_data()
	solution = solve_equation(matrix)
	print_column(solution)
	exit(0)
