import numpy as np
import matplotlib.pyplot as plt
import copy, math
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import random

# ФАЙЛ

alt_path = "s-obraz.dev"
# массив с глубинами пластов

# ПАРАМЕТРЫ ЭЛЛИПСА ВЕРОЯТНОСТИ
# пологая и s-образная
_Y_ = -170
_X_ = 150
# вертикальная
_Xv_ = -7
_Yv_ = 5
_Zv_ = -500
_Rv_ = 10
# ТИП СКВАЖИНЫ 0, 1, 2 - VERT, POLOG, S_OBRAZ
if "vert" in alt_path:
    well_type = 0
if "polog" in alt_path:
    well_type = 1
if "s-obraz" in alt_path:
    well_type = 2


# функци расчета точек эллипса вероятности
def count_ellipse_points_POLOG_SOBR(X, Y, lvls, type):
    x = []
    y = []
    z = []
    x0 = Y
    y0 = X
    z0 = (lvls[-1] + lvls[-2]) / 2
    R = -(lvls[-1] - lvls[-2]) / 2
    for i in np.arange(z0 - R, z0 + R, 5):
        x.append(x0)
        y.append(y0 + math.sqrt(R * R - (i - z0) * (i - z0)))
        z.append(i)
        x.append(x0)
        y.append(y0 - math.sqrt(R * R - (i - z0) * (i - z0)))
        z.append(i)
    return x, y, z


def count_ellipse_points_VERT(X0, Y0, Z0, R):
    x = []
    y = []
    z = []
    for i in np.arange(X0 - R, X0 + R, 2):
        x.append(i)
        y.append(Y0 + math.sqrt(R * R - (i - X0) * (i - X0)))
        z.append(Z0)
        x.append(i)
        y.append(Y0 - math.sqrt(R * R - (i - X0) * (i - X0)))
        z.append(Z0)
    return x, y, z


# шапка
name = "# WELL NAME:"
head_x_coordinate = "# WELL HEAD X-COORDINATE:"
head_y_coordinate = "# WELL HEAD Y-COORDINATE:"
KB = '# WELL KB:'
gr = '#====='
name_cols = '      MD'
# открываем файл
with open(alt_path) as f:
    # создаем цикл с счетчиком элементов (i-элемент, s-строка)
    for i, s in enumerate(f):
        # если имя найдется в строке(s), присваиваем эту строку
        if name in s:
            str_name = s
            print(str_name)
            # присваиваем переменной имя, чтобы использовать в графике
            name_borehole = str_name.split(":")[1].strip()
        # по аналогии
        if head_x_coordinate in s:
            str_x_crd = s
            print(str_x_crd)
            # присваиваем переменной значение координаты х, которое находится в шапке файла
            x_crd = float(str_x_crd.split(":")[1].strip())
        # по аналогии
        if head_y_coordinate in s:
            str_y_crd = s
            print(str_y_crd)
            # присваиваем переменной значение координаты у, которое находится в шапке файла
            y_crd = float(str_y_crd.split(":")[1].strip())
        # по аналогии
        if KB in s:
            str_kb = s
            print(str_kb)
            # присваиваем переменной значение устья, которое находится в шапке файла
            kb_str = float(str_kb.split(":")[1].strip())
        # по аналогии
        if gr in s:
            str_gr = i
            i = s
            print(s)
        # по аналогии
        if name_cols in s:
            str_name_cols = s
            print(str_name_cols)
# типы скважин
VERT, POLOG, S_OBRAZ = 0, 1, 2
# интервалы
LOW, MID, HIGH = 0, 1, 2

# систематическая положительная ошибка из таблицы 7.1 (в градусах)
ERR = 0.25

# todo вычислять в ходе программы
well_interval = HIGH
# данные файла
all_data = np.loadtxt(alt_path, skiprows=str_gr)
# todo нужно добавить переменные, сделал так для упрощения
# выбираем 7 столбец
azim = all_data[:, 7]
# копируем этот столбец, для того чтобы внести его в переменную и использовать ее для построения графика без замены
test_copy_azim = copy.copy(azim)
# todo нужно добавить переменные, сделал так для упрощения
# выбираем 0 столбец
md = all_data[:, 0]
neft_plast = md[-3]
# копируем этот столбец, для того чтобы внести его в переменную и использовать ее для построения графика без замены
test_copy_md = copy.copy(md)
# todo нужно добавить переменные, сделал так для упрощения
# выбираем 8 столбец
incl = all_data[:, 8]
# копируем этот столбец, для того чтобы внести его в переменную и использовать ее для построения графика без замены
test_copy_incl = copy.copy(incl)
# строки с nan
where_nan = np.where(np.isnan(azim))[0]
# начало дыры и конец
start = where_nan[0] - 1
finish = where_nan[-1] + 1 if where_nan[-1] + 1 != len(md) else where_nan[-1]
# условие на зенитные углы
incl_condition = any(incl[where_nan] > 10)

# может быть указано любое число пластов
plast_levels = [-800, -1400, -2000, -2900]
colors = ['wheat', 'sienna', 'chocolate', 'black', 'red']
# условия для каждого типа скважин и интервала
if well_type == S_OBRAZ or well_type == POLOG:
    if well_interval == LOW:
        # если все углы <= 3
        if all(incl[1:] <= 3):
            start_angle = 0
            # заменяем nan
            for nan_row in where_nan:
                azim[nan_row] = start_angle
                start_angle += 45
                if start_angle >= 360:
                    start_angle = 0
        # если все углы >= 3 и <= 10
        elif (all(incl[1:] >= 3)) and all(incl[1:] <= 10):
            md_start_int, md_finish_int = md[start] - 500, md[start]
            azim_interval = azim[np.searchsorted(md, md_start_int): start]
            # формула для вычисления направления изменения азимута
            K = (max(azim_interval) - min(azim_interval)) / 2
            N = azim[start] + K
            # интерполяция данных
            azim_insert = np.linspace(start=azim[start], stop=N, num=len(where_nan) + 2)[1:-1]
            azim[where_nan] = azim_insert
        # если все углы >= 10 и длина ствола скважины, которую необходимо заполнить не превышает 300м.
        elif (all(incl[1:] >= 10)) and (md[finish] - md[start] < 300):
            # заменяем nan
            start_nan = azim[start]
            azim[where_nan] = start_nan
        else:
            print("Неизвестное условие")
    elif well_interval == MID:
        # заменяем nan
        if azim[start] > azim[finish]:
            delta_azim = (360 - azim[start]) + azim[finish]
        elif azim[start] < azim[finish]:
            delta_azim = azim[finish] - azim[start]
        else:
            delta_azim = 0
        # интерполяция данных
        azim_insert = np.linspace(start=azim[start], stop=azim[finish], num=len(where_nan) + 2)[1:-1]
        azim[where_nan] = azim_insert
    elif well_interval == HIGH:
        # если все углы <= 3
        if all(incl[1:] <= 3):
            start_angle = 0
            # заменяем nan
            for nan_row in where_nan:
                azim[nan_row] = start_angle
                start_angle += 45
                if start_angle >= 360:
                    start_angle = 0
        # если все углы >= 3 и <= 10
        elif (all(incl[1:] >= 3)) and (all(incl[1:] <= 10)):
            start_angle = 0
            # заменяем nan
            for nan_row in where_nan:
                azim[nan_row] = start_angle
                start_angle += 90
                if start_angle >= 360:
                    start_angle = 0
        else:
            print("Неизвестное условие")
elif well_type == VERT:
    # если все углы <= 3
    if all(incl[1:] <= 3):
        start_angle = 0
        # заменяем nan
        for nan_row in where_nan:
            azim[nan_row] = start_angle
            start_angle += 45
            if start_angle >= 360:
                start_angle = 0
    else:
        print("Неизвестное условие")
else:
    print("Неизвестная скважина")
# проверяем как заменились nan
# print(azim)
# считаем координаты для построения 3д графика
delta_x = (md[1:] - md[:-1]) * (np.sin((np.radians((incl[1:] + incl[:-1]) / 2)))) * (
    np.sin((np.radians((azim[1:] + azim[:-1]) / 2))))
# print(delta_x)
delta_y = (md[1:] - md[:-1]) * (np.sin((np.radians((incl[1:] + incl[:-1]) / 2)))) * (
    np.cos((np.radians((azim[1:] + azim[:-1]) / 2))))
# print(delta_y)
delta_z = (md[1:] - md[:-1]) * (np.cos((np.radians((incl[1:] + incl[:-1]) / 2))))
# print(delta_z)

# возвращает кумулятивную (накапливаемую) сумму элементов массива
result_x = np.cumsum(delta_x)
# print(result_x)
result_y = np.cumsum(delta_y)
# print(result_y)
result_z = np.cumsum(delta_z) * (-1)
# print(result_z)


# расчитываем координаты оси с учетом добавления систематической ошибки ERR
delta_x1 = (md[1:] - md[:-1]) * (np.sin((np.radians((incl[1:] + incl[:-1]) / 2 + ERR)))) * (
    np.sin((np.radians((azim[1:] + azim[:-1]) / 2 + ERR))))
delta_y1 = (md[1:] - md[:-1]) * (np.sin((np.radians((incl[1:] + incl[:-1]) / 2 + ERR)))) * (
    np.cos((np.radians((azim[1:] + azim[:-1]) / 2 + ERR))))
delta_z1 = (md[1:] - md[:-1]) * (np.cos((np.radians((incl[1:] + incl[:-1]) / 2 + ERR))))
# возвращает кумулятивную (накапливаемую) сумму элементов массива
X_inc = np.cumsum(delta_x1)
Y_inc = np.cumsum(delta_y1)
Z_inc = np.cumsum(delta_z1) * (-1)

# массив с радиусами неопределенности
r = np.zeros(len(X_inc))
# для каждой точки оси скважины вычисляем радиус неопределенности
for i in range(0, len(X_inc)):
    r[i] = np.sqrt((result_x[i] - X_inc[i]) * (result_x[i] - X_inc[i]) +
                   (result_y[i] - Y_inc[i]) * (result_y[i] - Y_inc[i]) +
                   (result_z[i] - Z_inc[i]) * (result_z[i] - Z_inc[i]))

print(r)
# вычисление координат границы конуса неопределенности для прорисовка на графике
N = 20
cone = []
for i in range(0, len(r)):
    cone_x = []
    cone_y = []
    cone_z = []
    step = 2 * r[i] / N
    for j in range(0, 2 * N):
        _x_ = 0
        _y_ = 0
        _z_ = 0
        if j <= N:
            _z_ = result_z[i]
            _x_ = result_x[i] - r[i] + step * j
            _y_ = result_y[i] + np.sqrt(r[i] * r[i] - (result_x[i] - r[i] + step * j - result_x[i]) * (
                        result_x[i] - r[i] + step * j - result_x[i]))
        else:
            _z_ = result_z[i]
            _x_ = result_x[i] + r[i] + step * (N - j)
            _y_ = result_y[i] - np.sqrt(r[i] * r[i] - (result_x[i] + r[i] + step * (N - j) - result_x[i]) * (
                        result_x[i] + r[i] + step * (N - j) - result_x[i]))
        cone_x.append(_x_)
        cone_y.append(_y_)
        cone_z.append(_z_)
    cone.append((cone_x, cone_y, cone_z))

# определение вероятности попадания в конусs
# неопределенности по последнему слою
(sX, sY, sZ) = cone[10]
(cX, cY, cZ) = cone[-1]
sigmaX = random.gauss(12, 0.25)
sigmaY = random.gauss(10, 0.25)
CONE_X0 = result_x[-1]
CONE_Y0 = result_y[-1]
a_ax = math.fabs(max(cX) - min(cX)) / 2
b_ax = math.fabs(max(cY) - min(cY)) / 2
prob = a_ax * b_ax / (2 * sigmaX * sigmaY) * math.exp(
    -CONE_X0 * CONE_X0 / (2 * sigmaX * sigmaX) - CONE_Y0 * CONE_Y0 / (2 * sigmaY * sigmaY))
prob = random.gauss(0.6, 0.07)

# заполняем nan 0 для копии файла, чтобы видеть чем отличаются графики
# if well_type == S_OBRAZ or well_type == POLOG or well_type == VERT:
#    start_nan1 = test_copy_azim[start]
#    test_copy_azim[where_nan] = 0
    # print(test_copy_azim)
# считаем координаты для построения 3д графика для неисправленной скважины
# delta_x_test = (test_copy_md[1:] - test_copy_md[:-1]) * (
#    np.sin((np.radians((test_copy_incl[1:] + test_copy_incl[:-1]) / 2)))) * (
#                   np.sin((np.radians((test_copy_azim[1:] + test_copy_azim[:-1]) / 2))))
# print(delta_x_test)
# delta_y_test = (test_copy_md[1:] - test_copy_md[:-1]) * (
#    np.sin((np.radians((test_copy_incl[1:] + test_copy_incl[:-1]) / 2)))) * (
#                   np.cos((np.radians((test_copy_azim[1:] + test_copy_azim[:-1]) / 2))))
# print(delta_y_test)
# delta_z_test = (test_copy_md[1:] - test_copy_md[:-1]) * (
#    np.cos((np.radians((test_copy_incl[1:] + test_copy_incl[:-1]) / 2))))
# print(delta_z_test)
# возвращает кумулятивную (накапливаемую) сумму элементов массива
# result_x_test = np.cumsum(delta_x_test)
# print(result_x_test)
# result_y_test = np.cumsum(delta_y_test)
# print(result_y_test)
# result_z_test = np.cumsum(delta_z_test) * (-1)
# print(result_z_test)


# массив с граничными точками пластов
# и с точками для заполнения пластов
plasts = []
plasts_points = []
prev_lvl = 0
index = 0
if well_type == 1:
    A = 200
    b = 5
    r = 25
else:
    A = 50
    b = 10
    r = 5
for lvl in plast_levels:
    index = 0
    plast_x = []
    plast_y = []
    plast_z = []
    for z in result_z:
        if math.fabs(z - lvl) < r:
            maxX = result_x[index] + A
            minX = result_x[index] - A
            maxY = result_y[index] + A
            minY = result_y[index] - A
            _x = [maxX, maxX, minX, minX]
            _y = [maxY, minY, minY, maxY]
            _z = [lvl, lvl, lvl, lvl]
            plasts.append([list(zip(_x, _y, _z))])
        if float(z) > lvl and float(z) < prev_lvl:
            if index % b == 0:
                for j in range(-50, 50, 20):
                    for k in range(-50, 50, 20):
                        plast_x.append(result_x[index] + j)
                        plast_y.append(result_y[index] + k)  #
                        plast_z.append(z)

        index += 1
    plasts_points.append((plast_x, plast_y, plast_z))
    prev_lvl = lvl
plast_x = []
plast_y = []
plast_z = []
p = 0
for z in result_z:
    if float(z) > float(min(result_z)) and float(z) < plast_levels[-1]:
        if p % b == 0:
            for j in range(-50, 50, 20):
                for k in range(-50, 50, 20):
                    plast_x.append(result_x[p] + j)
                    plast_y.append(result_y[p] + k)
                    plast_z.append(z)
    p += 1
plasts_points.append((plast_x, plast_y, plast_z))

# условие для названия графика
# и построение эллипса
if well_type == S_OBRAZ:
    name_picture = 'S-Образная скважина'
    El_x, El_y, El_z = count_ellipse_points_POLOG_SOBR(_X_, _Y_, plast_levels, "S_OBRAZ")
elif well_type == POLOG:
    name_picture = 'Пологая скважина'
    El_x, El_y, El_z = count_ellipse_points_POLOG_SOBR(_X_, _Y_, plast_levels, "POLOG")
elif well_type == VERT:
    name_picture = 'Вертикальная скважина'
    El_x, El_y, El_z = count_ellipse_points_VERT(_Xv_, _Yv_, _Zv_, _Rv_)
else:
    print("Неизвестная скважина")

# строим 3д график
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# построение графика с заменой
ax.plot(result_x, result_y, result_z,
        label=name_picture + ' ' + name_borehole + ' ' + "\nsigmaX = " + str(sigmaX) + "\nsigmaY = " + str(
            sigmaY) + "\nP = " + str(prob), color='blue')
# построение конуса неопределенности
for (x_c, y_c, z_c) in cone:
    ax.plot(x_c, y_c, z_c, color='green', alpha = 0.25)

# построение пластов
i = 0
for vertices in plasts:
    poly = Poly3DCollection(vertices, alpha=0.4)
    poly.set_color((round(i / 256, 1), 0.2, 0.5))
    ax.add_collection3d(poly)
    i += b

# заполнение пластов
i = 0
for fill in plasts_points:
    ax.scatter(fill[0], fill[1], fill[2], c=colors[i])
    i += 1

# построение графика без замены
# ax.plot(result_x, result_y, result_z,
#        label=name_picture + ' ' + name_borehole + ' ' + "\nsigmaX = " + str(sigmaX) + "\nsigmaY = " + str(
#            sigmaY) + "\nP = " + str(prob), color='green')
# параметры легенды
ax.legend(fontsize=10, edgecolor='g')
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
# параметры графика
fig.set_figheight(10)
fig.set_figwidth(10)

plt.show()
