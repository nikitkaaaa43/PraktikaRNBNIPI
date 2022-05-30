import numpy as np
import matplotlib.pyplot as plt
import copy, math
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# ФАЙЛ
alt_path = "pologaya.dev"
# массив с глубинами пластов
# может быть указано любое число пластов
plast_levels = [-800, -1500, -2200]
colors = ['wheat', 'sienna', 'black', 'chocolate']
# ПАРАМЕТРЫ ЭЛЛИПСА ВЕРОЯТНОСТИ
sigmaX = 100
sigmaY = 200
sigmaZ = 150
_X0 = 500
_Y0 = 1000
# Z - серидина нефтеносного слоя


# ОПРЕДЕЛЕНИЕ ТИПА СКВАЖИНЫ ПО НАЗВАНИЮ ФАЙЛА
# 0, 1, 2 - VERT, POLOG, S_OBRAZ
if "vert" in alt_path:
    well_type = 0
if "polog" in alt_path:
    well_type = 1
if "s-obraz" in alt_path:
    well_type = 2


# функци расчета точек эллипса вероятности
def count_ellipse_points_POLOG_SOBR(X0, Y0, Z0, sigmaY, sigmaZ):
    x = []
    y = []
    z = []
    tx = []
    ty = []
    tz = []
    for i in np.arange(0 - sigmaZ, 0 + sigmaZ, 5):
        x.append(0)
        y.append(0 + math.sqrt((sigmaY * sigmaY) - (sigmaY * sigmaY) * (0 - i) * (0 - i) / (sigmaZ * sigmaZ)))
        z.append(i)
        tx.append(0)
        ty.append(0 - math.sqrt((sigmaY * sigmaY) - (sigmaY * sigmaY) * (0 - i) * (0 - i) / (sigmaZ * sigmaZ)))
        tz.append(i)
    tx.append(x[-1])
    ty.append(y[-1])
    tz.append(z[-1])
    tx.reverse()
    ty.reverse()
    tz.reverse()
    return x + tx, y + ty, z + tz


def count_ellipse_points_VERT(X0, Y0, Z0, sigmaX, sigmaY):
    x = []
    y = []
    z = []
    tx = []
    ty = []
    tz = []
    for i in np.arange(0 - sigmaX, 0 + sigmaX, 0.4):
        x.append(i)
        y.append(0 + math.sqrt((sigmaY * sigmaY) - (sigmaY * sigmaY) * (0 - i) * (0 - i) / (sigmaX * sigmaX)))
        z.append(0)
        tx.append(i)
        ty.append(0 - math.sqrt((sigmaY * sigmaY) - (sigmaY * sigmaY) * (0 - i) * (0 - i) / (sigmaX * sigmaX)))
        tz.append(0)
    tx.append(x[-1])
    ty.append(y[-1])
    tz.append(z[-1])
    tx.reverse()
    ty.reverse()
    tz.reverse()
    return x + tx, y + ty, z + tz


# функция поиска точки, в которой скважина пересечет плоскость эллипса
# эллипс вероятности
def GetWellPoint(wellX, wellY, wellZ, ellX, ellY, ellZ, wellType):
    PX = 0
    PY = 0
    PZ = 0
    if wellType == 0:  # vert, z_ell = const
        ind = 0
        for z in wellZ:
            if math.fabs(z - ellZ[0]) < 3:
                break
            ind += 1
        PX = wellX[ind - 1]
        PY = wellX[ind - 1]
        PZ = wellX[ind - 1]
    # s-obraz,polog, x_ell = const
    if wellType == 1 or wellType == 2:
        ind = 0
        for x in wellX:
            if math.fabs(x - ellX[0]) < 3:
                break
            ind += 1
        PX = wellX[ind - 1]
        PY = wellX[ind - 1]
        PZ = wellX[ind - 1]
    return PX, PY, PZ


# функция вычисления вероятности попадания в эллипс
def Probability(sigmaX, sigmaY):
    k = sigmaX / sigmaY
    return 1 - math.exp(-k * k / 2)


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

# интервалы
LOW, MID, HIGH = 0, 1, 2

# систематическая положительная ошибка из таблицы 7.1 (в градусах)
ERR = 0.25

# todo вычислять в ходе программы
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
# условия для каждого типа скважин и интервала
if well_type == 2 or well_type == 1:
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
elif well_type == 0:
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

# заполняем nan 0 для копии файла, чтобы видеть чем отличаются графики
# if well_type == S_OBRAZ or well_type == POLOG or well_type == VERT:
#    start_nan1 = test_copy_azim[start]
#    test_copy_azim[where_nan] = 0
#    print(test_copy_azim)
# считаем координаты для построения 3д графика для неисправленной скважины
# delta_x_test = (test_copy_md[1:] - test_copy_md[:-1]) * (np.sin((np.radians((test_copy_incl[1:] + test_copy_incl[:-1]) / 2)))) * (np.sin((np.radians((test_copy_azim[1:] + test_copy_azim[:-1]) / 2))))
# print(delta_x_test)
# delta_y_test = (test_copy_md[1:] - test_copy_md[:-1]) * (np.sin((np.radians((test_copy_incl[1:] + test_copy_incl[:-1]) / 2)))) * (np.cos((np.radians((test_copy_azim[1:] + test_copy_azim[:-1]) / 2))))
# print(delta_y_test)
# delta_z_test = (test_copy_md[1:] - test_copy_md[:-1]) * (np.cos((np.radians((test_copy_incl[1:] + test_copy_incl[:-1]) / 2))))
# print(delta_z_test)
# возвращает кумулятивную (накапливаемую) сумму элементов массива
#result_x_test = np.cumsum(delta_x_test)
# print(result_x_test)
#result_y_test = np.cumsum(delta_y_test)
# print(result_y_test)
#result_z_test = np.cumsum(delta_z_test) * (-1)
# print(result_z_test)

_Z0 = (plast_levels[-1] + min(result_z)) / 2
# построение эллипса вероятности в нефтеносном слое
# строим 2д график
fig = plt.figure()
ax = fig.add_subplot()
# условие для названия графика
# и построение эллипса
if well_type == 2:
    name_picture = 'S-Образная скважина'
    ax.set_title(name_picture)
    El_x, El_y, El_z = count_ellipse_points_POLOG_SOBR(_X0, _Y0, _Z0, sigmaY, sigmaZ)
    ax.plot(El_y, El_z, color='red',
            label="Эллипс в нефтеносном пласте\nsigmaY: " + str(sigmaY) + "\nsigmaY: " + str(sigmaZ))
    pX, pY, pZ = GetWellPoint(result_x, result_y, result_z, El_x, El_y, El_z, well_type)
    pX -= _X0
    pY -= _Y0
    pZ -= _Z0
    plt.plot(pY, pZ, 'o', label='Скважина\n' + str(Probability(sigmaY, sigmaZ)))
    ax.set_xlabel("Y")
    ax.set_ylabel("Z")

elif well_type == 1:
    name_picture = 'Пологая скважина'
    El_x, El_y, El_z = count_ellipse_points_POLOG_SOBR(_X0, _Y0, _Z0, sigmaY, sigmaZ)
    ax.set_title(name_picture)
    ax.plot(El_y, El_z, color='red',
            label="Эллипс в нефтеносном пласте\nsigmaY: " + str(sigmaY) + "\nsigmaZ: " + str(sigmaZ))
    pX, pY, pZ = GetWellPoint(result_x, result_y, result_z, El_x, El_y, El_z, well_type)
    pX -= _X0
    pY -= _Y0
    pZ -= _Z0
    plt.plot(pY, pZ, 'o', label='Скважина\n' + str(Probability(sigmaY, sigmaZ)))
    ax.set_xlabel("Y")
    ax.set_ylabel("Z")
elif well_type == 0:
    name_picture = 'Вертикальная скважина'
    ax.set_title(name_picture)
    El_x, El_y, El_z = count_ellipse_points_VERT(_X0, _Y0, _Z0, sigmaX, sigmaY)
    ax.plot(El_x, El_y, color='red',
            label="Эллипс в нефтеносном пласте\nsigmaX: " + str(sigmaX) + "\nsigmaY: " + str(sigmaY))
    pX, pY, pZ = GetWellPoint(result_x, result_y, result_z, El_x, El_y, El_z, well_type)
    pX -= _X0
    pY -= _Y0
    pZ -= _Z0
    plt.plot(pX, pY, 'o', label='Скважина\n' + str(Probability(sigmaX, sigmaY)))
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
else:
    print("Неизвестная скважина")

# параметры легенды
ax.legend(edgecolor='g')

# параметры графика
fig.set_figheight(10)
fig.set_figwidth(10)

plt.grid(color='black', linewidth=1)
plt.show()



