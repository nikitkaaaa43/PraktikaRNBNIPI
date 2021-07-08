import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
md = all_data[:, 0]
incl = all_data[:, 8]
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
print(delta_x)
delta_y = (md[1:] - md[:-1]) * (np.sin((np.radians((incl[1:] + incl[:-1]) / 2)))) * (np.cos((np.radians((azim[1:] + azim[:-1]) / 2))))
print(delta_y)
delta_z = (md[1:] - md[:-1]) * (np.cos((np.radians((incl[1:] + incl[:-1]) / 2))))
print(delta_z)
# строим 3д график
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(delta_x, delta_y, delta_z, label='parametric curve')
plt.show()












