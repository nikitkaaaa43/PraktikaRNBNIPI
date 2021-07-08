import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy
# шапка
name = "# WELL NAME:"
head_x_coordinate = "# WELL HEAD X-COORDINATE:"
head_y_coordinate = "# WELL HEAD Y-COORDINATE:"
KB = '# WELL KB:'
gr = '#====='
name_cols = '      MD'
alt_path = "vert.dev"

with open(alt_path) as f:
    for i, s in enumerate(f):
        if name in s:
            str_name = s
            print(str_name)
        if head_x_coordinate in s:
            str_x_crd = s
            print(str_x_crd)
        if head_y_coordinate in s:
            str_y_crd = s
            print(str_y_crd)
        if KB in s:
            str_kb = s
            print(str_kb)
        if gr in s:
            str_gr = i
            i = s
            print(s)
        if name_cols in s:
            str_name_cols = s
            print(str_name_cols)


f = open(alt_path)
aa = f.readlines()

np.loadtxt(alt_path, skiprows=12)
# типы скважин
VERT, POLOG, S_OBRAZ = 0, 1, 2
# интервалы
LOW, MID, HIGH = 0, 1, 2

# todo вычислять в ходе программы
well_type = VERT
well_interval = MID
# данные файла
all_data = np.loadtxt(alt_path, skiprows=12, usecols=(None))
azim = all_data[:, 7]
test_copy_azim = copy.copy(azim)
md = all_data[:, 0]
test_copy_md = copy.copy(md)
incl = all_data[:, 8]
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
            for nan_row in where_nan:
                azim[nan_row] = start_angle
                start_angle += 45
                if start_angle >= 360:
                    start_angle = 0
        # если все углы >= 3 и <= 10
        elif (all(incl[1:] >= 3)) and all(incl[1:] <= 10):
            md_start_int, md_finish_int = md[start] - 500, md[start]
            azim_interval = azim[np.searchsorted(md, md_start_int): start]
            K = (max(azim_interval) - min(azim_interval)) / 2
            N = azim[start] + K
            azim_insert = np.linspace(start=azim[start], stop=N, num=len(where_nan) + 2)[1:-1]
            azim[where_nan] = azim_insert
        elif (all(incl[1:] >= 10)) and (md[finish] - md[start] < 300):
            start_nan = azim[start]
            azim[where_nan] = start_nan
        else:
            NotImplementedError
    elif well_interval == MID:
        if azim[start] > azim[finish]:
            delta_azim = (360 - azim[start]) + azim[finish]
        elif azim[start] < azim[finish]:
            delta_azim = azim[finish] - azim[start]
        else:
            delta_azim = 0
        # fixme учесть случай когда start больше finish
        azim_insert = np.linspace(start=azim[start], stop=azim[finish], num=len(where_nan) + 2)[1:-1]
        azim[where_nan] = azim_insert
    elif well_interval == HIGH:
        # если все углы <= 3
        if all(incl[1:] <= 3):
            start_angle = 0
            for nan_row in where_nan:
                azim[nan_row] = start_angle
                start_angle += 45
                if start_angle >= 360:
                    start_angle = 0
        # если все углы >= 3 и <= 10
        elif (all(incl[1:] >= 3)) and (all(incl[1:] <= 10)):
            start_angle = 0
            for nan_row in where_nan:
                azim[nan_row] = start_angle
                start_angle += 90
                if start_angle >= 360:
                    start_angle = 0
        else:
            NotImplementedError
elif well_type == VERT:
    if all(incl[1:] <= 3):
        start_angle = 0
        for nan_row in where_nan:
            azim[nan_row] = start_angle
            start_angle += 45
            if start_angle >= 360:
                start_angle = 0
    else:
        NotImplementedError
else:
    NotImplementedError
# проверяем как заменились nan
print(azim)
# считаем координаты для построения 3д графика
delta_x = (md[1:] - md[:-1]) * (np.sin((np.radians((incl[1:] + incl[:-1]) / 2)))) * (np.sin((np.radians((azim[1:] + azim[:-1]) / 2))))
#print(delta_x)
delta_y = (md[1:] - md[:-1]) * (np.sin((np.radians((incl[1:] + incl[:-1]) / 2)))) * (np.cos((np.radians((azim[1:] + azim[:-1]) / 2))))
#print(delta_y)
delta_z = (md[1:] - md[:-1]) * (np.cos((np.radians((incl[1:] + incl[:-1]) / 2))))
#print(delta_z)
# возвращает кумулятивную (накапливаемую) сумму элементов массива
result_x = np.cumsum(delta_x)
#print(result_x)
result_y = np.cumsum(delta_y)
#print(result_y)
result_z = np.cumsum(delta_z) *(-1)
#print(result_z)
# заполняем nan 0 для копии файла, чтобы видеть чем отличаются графики
if well_type == S_OBRAZ or well_type == POLOG or well_type == VERT:
    start_nan1 = test_copy_azim[start]
    test_copy_azim[where_nan] = 0
    #print(test_copy_azim)
# считаем координаты для построения 3д графика для неисправленной скважины
delta_x_test = (test_copy_md[1:] - test_copy_md[:-1]) * (np.sin((np.radians((test_copy_incl[1:] + test_copy_incl[:-1]) / 2)))) * (np.sin((np.radians((test_copy_azim[1:] + test_copy_azim[:-1]) / 2))))
#print(delta_x_test)
delta_y_test = (test_copy_md[1:] - test_copy_md[:-1]) * (np.sin((np.radians((test_copy_incl[1:] + test_copy_incl[:-1]) / 2)))) * (np.cos((np.radians((test_copy_azim[1:] + test_copy_azim[:-1]) / 2))))
#print(delta_y_test)
delta_z_test = (test_copy_md[1:] - test_copy_md[:-1]) * (np.cos((np.radians((test_copy_incl[1:] + test_copy_incl[:-1]) / 2))))
#print(delta_z_test)
# возвращает кумулятивную (накапливаемую) сумму элементов массива
result_x_test = np.cumsum(delta_x_test)
#print(result_x_test)
result_y_test = np.cumsum(delta_y_test)
#print(result_y_test)
result_z_test = np.cumsum(delta_z_test) *(-1)
#print(result_z_test)

# строим 3д график
if well_type == S_OBRAZ:
    name_picture = 'S-Образная скважина'
elif well_type == POLOG:
    name_picture = 'Пологая скважина'
elif well_type == VERT:
    name_picture = 'Вертикальная скважина'
else:
    NotImplementedError

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# построение графика с заменой
ax.plot(result_x, result_y, result_z, label = name_picture, color = 'blue')
# построение графика без замены
ax.plot(result_x_test, result_y_test, result_z_test, label = name_picture + ' без замены', color = 'red')
# параметры легенды
ax.legend(fontsize = 15, edgecolor = 'g')
# параметры графика
fig.set_figheight(10)
fig.set_figwidth(10)
plt.show()












