# №12
# 9битный числа -54 в дополнительный код:
# print(t12(9, -54, "Доп"))
from itertools import *
def t12(endBytes:int, fromInt:int, toType="Доп"):
    if fromInt>=0:
        return str(bin(fromInt))[2:]
    if toType=="Доп":
        return "1"+str(bin(2**(endBytes-1)+fromInt))[2:]
    r = str(bin(int(str(abs(fromInt).to_bytes(1, byteorder='big', signed=True))[4:-1], 16)))[2:]
    if toType=="Прямой":
        return "1"+"0"*(endBytes-1-len(r))+r
    if toType=="Обратный":
        return "1"+("0"*(endBytes-1-len(r))+r).replace("1","2").replace("0","1").replace("2","0")



# №11
# само выражение, со скобочками и пробелами: 241x3(13) + 2x025(13)
# найдите остаток от деления результата на 23
# t11('241x3(13) + 2x025(13)', 23)
def convert_to_decimal(number: str, x:int) -> int:
    base = int(number.split("(")[-1][:-1])
    number = number.replace(f"({base})", "")
    result = 0
    for i,a in enumerate(number[::-1]):
        result+=(alphabet.index(a) if a!="x" else x)*(base**i)
    return result
alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def t11(template:str, resRemainder:int):
    template_split = template.split(" ")
    minBase = min(int(q.split(")")[0]) for q in template_split[0].split("(")[1:])
    for x in range(1, minBase):
        result=convert_to_decimal(template_split[0], x)
        for n in range(2, len(template_split), 2):
            if template_split[n-1] == "+":
                result+=convert_to_decimal(template_split[n], x)
            elif template_split[n-1] == "-":
                result-=convert_to_decimal(template_split[n], x)
            elif template_split[n-1] == "*":
                result*=convert_to_decimal(template_split[n], x)
        if not abs(result)%resRemainder:
            print(f"Для x={x}: {result//resRemainder:}")


def t13(absolutePathToFile:str, is_N_Min:bool, conditionForN, conditionForPairs):
    file = open(absolutePathToFile, "r")
    data = list(map(int, file.read().split()))
    file.close()
    n=(min if is_N_Min else max)(d for d in data if conditionForN(d))
    counter = 0
    sums = []
    for i,d in enumerate(data[:-1]):
        if conditionForPairs(d, data, i, n):
            counter+=1
            sums.append(d+data[i+1])
    return counter, sums

# t13(Полный путь до файла, Пусть N - минимальное=>True; Пусть N - максимальное => False, N - число, НЕ КРАТНОЕ 15, пар элементов, где ОБА ЧИСЛА КРАТНЫ N)
# c, s = t13("13.txt", True, lambda number: number%15, lambda d, data, i, n: not d%n and not data[i+1]%n)
# количество пар, максимальную сумму пар
# print(c, max(s))

def t6():
    print('''
Приблизительная программа перебором:
from itertools import product
for i, w in enumerate(product(sorted("АКРУ"), repeat=6)):
    if w[2]=="Р":
        print(i+1, w)
        break
    ''')

# t5(lambda k: [(k[0],  1,    1,    k[1], 1),
#               (0,     k[2], k[3], 0,    1),
#               (k[4],  0,    1,    0,    1),
#              ],
#     lambda x,y,z,w: (not (y <= (x == w)) and (z <= x)),
#     "xyzw"
#    )
# tableLambda - таблица истинности. k[i] - неизвестное
# condition - выражение
# vars - буквы с переменными
def t5(tableLambda, condition, vars:str = "xyzw"):
    for k in product([0,1], repeat=len(k)):
        table = tableLambda(k)
        # Проверяем все ли строки различны по условию:
        if len(table) == len(set(table)):
            # Далее в переменную p поочередно получаем все перестановки xyzw
            for p in permutations(vars):
                s = 0
                for line in table:
                    # Кладем в соответствующие переменные
                    # именно их значения взятые из таблицы
                    xyzwf = [line[p.index(i)] for i in vars] + [line[-1]]
                    # Находим значение функции, сравниваем с f, и добавляем в сумму:
                    s += xyzwf[-1] == condition(*(xyzwf[:-1]))
                    # s += xyzwf[-1] == (not (y <= (x == w)) and (z <= x))
                    # Если кол-во верных строк, соответствует условию, то:
                if s == len(table):
                    print(''.join(p))
