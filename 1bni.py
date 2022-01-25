import numpy as np
import matplotlib.pyplot as plt
import copy
import math
import cmath
import pywt
# шапка
name = "# WELL NAME:"
head_x_coordinate = "# WELL HEAD X-COORDINATE:"
head_y_coordinate = "# WELL HEAD Y-COORDINATE:"
KB = '# WELL KB:'
gr = '#====='
name_cols = '      MD'
alt_path = "pologaya.dev"
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
well_type = POLOG
well_interval = HIGH
# данные файла
all_data = np.loadtxt(alt_path, skiprows=str_gr)
# todo нужно добавить переменные, сделал так для упрощения
# выбираем 7 столбец
azim = all_data[:, 7]
#print(azim)
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
# копируем массив зенитного угла
test_incl = copy.copy(incl)
test1_incl = copy.copy(incl)
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
#print(azim)
# копируем массив азимутального угла
test_azim = copy.copy(azim)
test1_azim = copy.copy(azim)
# считаем координаты для построения 3д графика
delta_x = (md[1:] - md[:-1]) * (np.sin((np.radians((incl[1:] + incl[:-1]) / 2)))) * (np.sin((np.radians((azim[1:] + azim[:-1]) / 2))))
# print(delta_x)
delta_y = (md[1:] - md[:-1]) * (np.sin((np.radians((incl[1:] + incl[:-1]) / 2)))) * (np.cos((np.radians((azim[1:] + azim[:-1]) / 2))))
# print(delta_y)
delta_z = (md[1:] - md[:-1]) * (np.cos((np.radians((incl[1:] + incl[:-1]) / 2))))
test_incl += 0.25
#print(test_incl)
test1_incl -= 0.25
#print(test1_incl)
test_azim += 5
#print(test_azim)
test1_azim -= 5
#print(test1_azim)
delta_x_rad = (md[1:] - md[:-1]) * (np.sin((np.radians((test_incl[1:] + test_incl[:-1]) / 2)))) * (np.sin((np.radians((test_azim[1:] + test_azim[:-1]) / 2))))
# print(delta_x)
delta_y_rad = (md[1:] - md[:-1]) * (np.sin((np.radians((test_incl[1:] + test_incl[:-1]) / 2)))) * (np.cos((np.radians((test_azim[1:] + test_azim[:-1]) / 2))))
# print(delta_y)
delta_z_rad = (md[1:] - md[:-1]) * (np.cos((np.radians((test_incl[1:] + test_incl[:-1]) / 2))))
#delta_x_rad1 = (md[1:] - md[:-1]) * (np.sin((np.radians((test1_incl[1:] + test1_incl[:-1]) / 2)))) * (np.sin((np.radians((test1_azim[1:] + test1_azim[:-1]) / 2))))
# print(delta_x)
#delta_y_rad1 = (md[1:] - md[:-1]) * (np.sin((np.radians((test1_incl[1:] + test1_incl[:-1]) / 2)))) * (np.cos((np.radians((test1_azim[1:] + test1_azim[:-1]) / 2))))
# print(delta_y)
#delta_z_rad1 = (md[1:] - md[:-1]) * (np.cos((np.radians((test1_incl[1:] + test1_incl[:-1]) / 2))))
radius_skv = np.sqrt((x_crd - delta_x_rad)**2 + (y_crd - delta_y_rad)**2 + (kb_str - delta_z_rad)**2)
print(radius_skv)
# print(delta_z)
# возвращает кумулятивную (накапливаемую) сумму элементов массива
result_x = np.cumsum(delta_x)
# print(result_x)
result_y = np.cumsum(delta_y)
# print(result_y)
result_z = np.cumsum(delta_z) * (-1)
# print(result_z)
# заполняем nan 0 для копии файла, чтобы видеть чем отличаются графики
if well_type == S_OBRAZ or well_type == POLOG or well_type == VERT:
    start_nan1 = test_copy_azim[start]
    test_copy_azim[where_nan] = 0
    #print(test_copy_azim)
# считаем координаты для построения 3д графика для неисправленной скважины
delta_x_test = (test_copy_md[1:] - test_copy_md[:-1]) * (np.sin((np.radians((test_copy_incl[1:] + test_copy_incl[:-1]) / 2)))) * (np.sin((np.radians((test_copy_azim[1:] + test_copy_azim[:-1]) / 2))))
# print(delta_x_test)
delta_y_test = (test_copy_md[1:] - test_copy_md[:-1]) * (np.sin((np.radians((test_copy_incl[1:] + test_copy_incl[:-1]) / 2)))) * (np.cos((np.radians((test_copy_azim[1:] + test_copy_azim[:-1]) / 2))))
# print(delta_y_test)
delta_z_test = (test_copy_md[1:] - test_copy_md[:-1]) * (np.cos((np.radians((test_copy_incl[1:] + test_copy_incl[:-1]) / 2))))
# print(delta_z_test)
# возвращает кумулятивную (накапливаемую) сумму элементов массива
result_x_test = np.cumsum(delta_x_test)
# print(result_x_test)
result_y_test = np.cumsum(delta_y_test)
# print(result_y_test)
result_z_test = np.cumsum(delta_z_test) * (-1)
# print(result_z_test)


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
# построение графика с заменой
ax.plot(result_x, result_y, result_z, label=name_picture + ' ' + name_borehole, color='blue')
# построение графика без замены
ax.plot(result_x_test, result_y_test, result_z_test, label=name_picture + ' ' + name_borehole + ' без замены', color='red')
# параметры легенды
ax.legend(fontsize=15, edgecolor='g')
# параметры графика
fig.set_figheight(10)
fig.set_figwidth(10)
plt.show()












