#печать подстрочной цифры
def PrintNumb(i):
	n = ['₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉']
	print(n[i], end='')

#печать функции
def PrintFunction(c, m, n):
	for i in range(m):
		for j in range(n):
			if (i + j == 0):
				print(c[i][j], "x", sep='', end='')
			else:
				if (c[i][j] >= 0):
					print(" + ", sep='', end='')
				else:
					print(" - ", sep='', end='')
				print(abs(c[i][j]), "x", sep='', end='')
			PrintNumb(i)
			PrintNumb(j)
			
	print(" → min", sep='', end='')
		
#печать заголовка таблицы
def PrintHeader(num, val):
	for _ in range(21 + 9 * num):
		print("-", end='')

	print("\n  Поставщик  |", end='')
	for _ in range(round((9 * num - 11) / 2)):
		print(" ", end='')
	print("Потребитель", end='')
	for _ in range(9 * num - 12 - round((9 * num - 11) / 2)):
		print(" ", end='')
	print("|{: ^7}".format(val))

	print("             |", end='')
	for _ in range(9 * num - 1):
		print("-", end='')
	print("|                ")


	print("             |", end='')
	for i in range(num):
		print("   B", end='')
		PrintNumb(i)
		print("   |", end='')
	print()

	for _ in range(21 + 9 * num):
		print("-", end='')
	
	print()

#печать строки таблицы
def PrintRow(numb, coefs, counted, res):
	print("     A", sep='', end='')
	PrintNumb(numb)
	print("      |", sep='', end='')

	for c in coefs:
		print("{: <8}|".format(c), end='')

	print("{: ^7}".format(res))
	print("             |", end='')
	for i in range(len(coefs)):
		k = numb * len(coefs)
		if counted[i + k] < -1:
			c = " - "
		elif counted[i + k] == -1:
			c = "   "
		else:
			c = counted[i + k]
		print("{: >8}|".format(c), end='')

	print()
	for _ in range(21 + 9 * len(coefs)):
		print("-", end='')
	print()

#печать последней строки таблицы - потребность
def PrintBottom(res, val):
	print("{: ^13}|".format(val), end='')
	for number in res:
		print("{: ^8}|".format(number), end='')
	print()
	print()

def PrintTable(num, val_head, val_bot, coefs, xcount, a, b):
	PrintHeader(num, val_head)
	for i in range(m):
		PrintRow(i, coefs[i], xcount, a[i])
	PrintBottom(b, val_bot)
	print()

f = open('input.txt')
m = 0
n = 0

c = []
a = []
b = []
xcount = []
ccount = []

k = 0

#чтение файла
for line in f:
	if k == 0:
		m = int(line)
	elif k == 1:
		n = int(line)
	elif k == 2:
		s = line.split()
		for numb in s:
			a.append(int(numb))
	elif k == 3:
		s = line.split()
		for numb in s:
			b.append(int(numb))
	elif k < m + 4:
		s = line.split()
		c.append([])
		for numb in s:
			c[k - 4].append(int(numb))
			ccount.append(int(numb))
			xcount.append(-1)
	else:
		break

	k += 1

if k == 0:
	print("Файл пуст")
	exit()
	
print("\nТранспортная задача\n\nF = ", end='')
PrintFunction(c, m, n)
print("\n")

count = len([item for item in xcount if item >= 0])

PrintTable(n, "Запас", "Потребность", c, xcount, a, b)

while count < m + n - 1:

	min_coef = min([item for item in ccount if item >= 0])

	num_row = -1
	num_col = -1
	res = 0
	res_k = -1

	for k, item in enumerate(ccount):
		if item == min_coef:
			i = k // n
			j = k % n
			if (a[i] > 0 or b[j] > 0) and xcount[k] == -1:
				item_res = min(a[i], b[j])

				if item_res > res:
					num_row = -1
					num_col = -1
					if item_res == a[i]:
						num_row = i
					else:
						num_col = j
					res_k = k
					res = item_res

	if num_row < 0 and num_col < 0:
		for k, item in enumerate(ccount):
			if item == min_coef:
				i = k // n
				j = k % n
				if (a[i] > 0 or b[j] > 0) and xcount[k] == -1:
					item_res = min(a[i], b[j])

					if item_res == res:
						if item_res == a[i]:
							num_row = i
						else:
							num_col = j
						res_k = k
						res = item_res
						break

	if num_row >= 0:
		a[num_row] -= res
		b[res_k % n] -= res
		if a[num_row] == 0:
			for i in range(n):
				ccount[num_row * n  + i] = -1
				if xcount[num_row * n  + i] < 0: 
					xcount[num_row * n  + i] = -2
	elif num_col >= 0:
		a[res_k // n] -= res
		b[num_col] -= res
		if b[num_col] == 0:
			for i in range(m):
				ccount[i * n  + num_col] = -1
				if xcount[i * n  + num_col] < 0: 
					xcount[i * n  + num_col] = -2

	xcount[res_k] = res

	PrintTable(n, "Запас", "Потребность", c, xcount, a, b)
	count = len([item for item in xcount if item >= 0])

result = 0

for i in range(len(xcount)):
	if (xcount[i] > 0):
		result += c[i // n][i % n] * xcount[i]

print("Результат: F = ", result)


print("\n\n\nМетод потенциалов\n")

v = [0 for _ in range(n)]
v_ready = [False for _ in range(n)]
u = [0 for _ in range(m)]
u_ready = [False for _ in range(m)]

u_ready[0] = True


row = 0

while (not all(v_ready)) or (not all(u_ready)):
	if u_ready[row]:
		if not all(v_ready):
			for i in range(n):
				if xcount[row * n + i] >= 0 and not v_ready[i]:
					v[i] = c[row][i] - u[row]
					v_ready[i] = True
					
		if not all(u_ready):
			for col in range(n):
				if v_ready[col]:
					for i in range(m):
						if xcount[i * n + col] >= 0 and not u_ready[i]:
							u[i] = c[i][col] - v[col]
							u_ready[i] = True
							if row == -1:
								row = i - 1

	row += 1

	if row == m:
		row = 0

	

PrintTable(n, "U", "V", c, xcount, u, v)

otr = False
print("\nОценки незадействованных маршрутов: ")
for row in range(m):
	for col in range(n):
		if xcount[row * n + col] < 0:
			print("A", end='')
			PrintNumb(row)
			print("B", end='')
			PrintNumb(col)
			print(": Δ", end='')
			PrintNumb(row)
			PrintNumb(col)
			res = c[row][col] - (u[row] + v[col])
			print(" =", res)

			otr = (res < 0)
			
if otr:
	print("\nЕсть отрицательная оценка! Возможно получение нового решения, как минимум, не хуже имеющегося.")
else:
	print("\nОтрицательных оценок нет! Найдено оптимальное решение.")