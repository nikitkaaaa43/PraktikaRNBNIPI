import numpy as np
import matplotlib.pyplot as plt
import copy, math
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# функция расчета точек эллипса вероятности
def count_ellipse_points(X, Y, lvls, type):
    x = []
    y = []
    z = []
    if type == "POLOG" or "S_OBRAZ":
        x0 = X
        y0 = Y
        z0 = (lvls[-2] + lvls[-1]) / 2
        R = 50
        for i in np.arange(- R, R, 1):
            x.append(X)
            z.append(z0 + math.sqrt(R * R - (i - z0) * (i - z0)))
            y.append(i)
            x.append(X)
            z.append(z0 - math.sqrt(R * R - (i - z0) * (i - z0)))
            y.append(i)
    if type == "VERT":
        pass
    return x, y, z




# шапка
name = "# WELL NAME:"
head_x_coordinate = "# WELL HEAD X-COORDINATE:"
head_y_coordinate = "# WELL HEAD Y-COORDINATE:"
KB = '# WELL KB:'
gr = '#====='
name_cols = '      MD'
alt_path = "vert.dev"
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


# todo вычислять в ходе программы
well_type = VERT
well_interval = MID
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

# тип измеряемого инструмента
Magnetic_inclinometers, Telesystems_Wired_Channel, Telesystems_hydraulic_communication_channel, Gyroscopic_inclinometers = 0, 1, 2, 3

# систематическая положительная ошибка из таблицы 7.1 (в градусах)
well_inclinometers = Telesystems_Wired_Channel
if all(incl[1:] < 5):
    ERR = 0.25
elif well_inclinometers == Magnetic_inclinometers and all(incl[1:] > 5):
    ERR = 0.2
elif well_inclinometers == Telesystems_Wired_Channel and all(incl[1:] > 5):
    ERR = 0.15
elif well_inclinometers == Telesystems_hydraulic_communication_channel and all(incl[1:] > 5):
    ERR = 0.1
elif well_inclinometers == Gyroscopic_inclinometers and all(incl[1:] > 5):
    ERR = 0.1
else:
    print("Неизвестное условие")

#337
# копируем этот столбец, для того чтобы внести его в переменную и использовать ее для построения графика без замены
test_copy_incl = copy.copy(incl)
# строки с nan
where_nan = np.where(np.isnan(azim))[0]
# начало дыры и конец
start = where_nan[0] - 1
finish = where_nan[-1] + 1 if where_nan[-1] + 1 != len(md) else where_nan[-1]
# условие на зенитные углы
incl_condition = any(incl[where_nan] > 10)
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
        # todo учесть случай когда start больше finish
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
print(azim)
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

# print(r)
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

# заполняем nan 0 для копии файла, чтобы видеть чем отличаются графики
# if well_type == S_OBRAZ or well_type == POLOG or well_type == VERT:
# start_nan1 = test_copy_azim[start]
# test_copy_azim[where_nan] = 0
# print(test_copy_azim)
# считаем координаты для построения 3д графика для неисправленной скважины
# delta_x_test = (test_copy_md[1:] - test_copy_md[:-1]) * (
# np.sin((np.radians((test_copy_incl[1:] + test_copy_incl[:-1]) / 2)))) * (
# np.sin((np.radians((test_copy_azim[1:] + test_copy_azim[:-1]) / 2))))
# print(delta_x_test)
# delta_y_test = (test_copy_md[1:] - test_copy_md[:-1]) * (
# np.sin((np.radians((test_copy_incl[1:] + test_copy_incl[:-1]) / 2)))) * (
# np.cos((np.radians((test_copy_azim[1:] + test_copy_azim[:-1]) / 2))))
# print(delta_y_test)
# delta_z_test = (test_copy_md[1:] - test_copy_md[:-1]) * (
# np.cos((np.radians((test_copy_incl[1:] + test_copy_incl[:-1]) / 2))))
# print(delta_z_test)
# возвращает кумулятивную (накапливаемую) сумму элементов массива
# result_x_test = np.cumsum(delta_x_test)
# print(result_x_test)
# result_y_test = np.cumsum(delta_y_test)
# print(result_y_test)
# result_z_test = np.cumsum(delta_z_test) * (-1)
# print(result_z_test)


# массив с глубинами пластов
# может быть указано любое число пластов
plast_levels = [-800, -1500, -2200, -abs(neft_plast)]
colors = ['wheat', 'sienna', 'black', 'chocolate']

# массив с граничными точками пластов
# и с точками для заполнения пластов
plasts = []
plasts_points = []
prev_lvl = 0
for lvl in plast_levels:
    index = 0
    plast_x = []
    plast_y = []
    plast_z = []
    for z in result_z:
        if math.fabs(z - lvl) < 5:
            maxX = result_x[index] + 50
            minX = result_x[index] - 50
            maxY = result_y[index] + 50
            minY = result_y[index] - 50
            _x = [maxX, maxX, minX, minX]
            _y = [maxY, minY, minY, maxY]
            _z = [lvl, lvl, lvl, lvl]
            plasts.append([list(zip(_x, _y, _z))])
        if float(z) > lvl and float(z) < prev_lvl:
            if index % 10 == 0:
                for j in range(-50, 50, 20):
                    for k in range(-50, 50, 20):
                        plast_x.append(result_x[index] + j)
                        plast_y.append(result_y[index] + k)
                        plast_z.append(z)

        index += 1
    plasts_points.append((plast_x, plast_y, plast_z))
    prev_lvl = lvl

# условие для названия графика
if well_type == S_OBRAZ:
    name_picture = 'S-Образная скважина'
elif well_type == POLOG:
    name_picture = 'Пологая скважина'
elif well_type == VERT:
    name_picture = 'Вертикальная скважина'
else:
    print("Неизвестная скважина")
# строим 3д график
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# построение конуса неопределенности
for (x_c, y_c, z_c) in cone:
    ax.plot(x_c, y_c, z_c, color='green')

# построение пластов
i = 0
for vertices in plasts:
    poly = Poly3DCollection(vertices, alpha=0.4)
    ax.add_collection3d(poly)
    poly.set_color((round(i / 256, 1), 0.2, 0.5))
    i += 10

# заполнение пластов
i = 0
for fill in plasts_points:
    ax.scatter(fill[0], fill[1], fill[2], c=colors[i])
    i += 1

# построение графика с заменой
ax.plot(result_x, result_y, result_z, label=name_picture + ' ' + name_borehole, color='blue')
# параметры легенды
ax.legend(fontsize=15, edgecolor='g')
# параметры графика
fig.set_figheight(10)
fig.set_figwidth(10)
plt.show()
