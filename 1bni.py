import numpy as np
import pandas as pd
name = "# WELL NAME:"
head_x_coordinate = "# WELL HEAD X-COORDINATE:"
head_y_coordinate = "# WELL HEAD Y-COORDINATE:"
KB = '# WELL KB:'
gr = '#====='
name_cols = '      MD'
alt_path = "1234 - corrupted.dev"

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

alt_path = "1234 - corrupted.dev"

f = open(alt_path)
aa = f.readlines()

np.loadtxt(alt_path, skiprows=12)
# типы скважин
VERT, POLOG, S_OBRAZ = 0, 1, 2
# интервалы
LOW, MID, HIGH = 0, 1, 2

# todo вычислять в ходе программы
well_type = S_OBRAZ
well_interval = 1
# данные файла
all_data = np.loadtxt(alt_path, skiprows=12, usecols=(None))
azim = all_data[:, 7]
md = all_data[:, 0]
incl = all_data[:, 8]
# строки с nan
where_nan = np.where(np.isnan(azim))
# начало дыры и конец
start, finish = where_nan[0][0] - 1, where_nan[0][-1] + 1
#условие на зенитные углы
incl_condition = any(incl[where_nan] > 10)

if well_type == S_OBRAZ:
    if well_interval == 0:
        if all(incl[1:] <= 3):
            start_angle = 0
            for nan_row in where_nan:
                azim[nan_row] = start_angle // 360
                start_angle += 45
        elif (all(incl[1:] <= 3)) and all(incl[1:] >= 10):
            md_start_int, md_finish_int = md[start] - 500, md[start]
            azim_interval = azim[np.searchsorted(md, md_start_int): start]
        elif (all(incl[1:] >= 10)) and (md[start] - md[finish] < 300):
            start_nan = azim[start]
            for nan_row1 in where_nan:
                azim[nan_row1] = start_nan
        else:
            NotImplementedError
    elif well_interval == 1:
        if azim[start] > azim[finish]:
            delta_azim = (360 - azim[start]) + azim[finish]
        elif azim[start] < azim[finish]:
            delta_azim = azim[finish] - azim[start]
        else:
            delta_azim = 0
        # fixme учесть случай когда start больше finish
        azim_insert = np.linspace(start=azim[start], stop=azim[finish], num=len(where_nan[0]) + 2)[1:-1]
        azim[where_nan] = azim_insert
    elif well_interval == 2:
        if all(incl[1:] <= 3):
            start_angle = 0
            for nan_row in where_nan:
                azim[nan_row] = start_angle // 360
                start_angle += 45
        elif (all(incl[1:] <= 3)) and (all(incl[1:] >= 10)) :
            start_angle = 0
            for nan_row in where_nan:
                azim[nan_row] = start_angle // 360
                start_angle += 90
        else:
            NotImplementedError
elif well_type == VERT:
    if all(incl[1:] <= 3):
        start_angle = 0
        for nan_row in where_nan:
            azim[nan_row] = start_angle // 360
            start_angle += 45
    else:
        NotImplementedError
elif well_type == POLOG:
    if well_interval == 0:
        if all(incl[1:] <= 3):
            start_angle = 0
            for nan_row in where_nan:
                azim[nan_row] = start_angle // 360
                start_angle += 45
        elif (all(incl[1:] <= 3)) and all(incl[1:] >= 10):
            md_start_int, md_finish_int = md[start] - 500, md[start]
            azim_interval = azim[np.searchsorted(md, md_start_int): start]
        elif (all(incl[1:] >= 10)) and (md[start] - md[finish] < 300):
            start_nan = azim[start]
            for nan_row1 in where_nan:
                azim[nan_row1] = start_nan
        else:
            NotImplementedError
    elif well_interval == 1:
        if azim[start] > azim[finish]:
            delta_azim = (360 - azim[start]) + azim[finish]
        elif azim[start] < azim[finish]:
            delta_azim = azim[finish] - azim[start]
        else:
            delta_azim = 0
        # fixme учесть случай когда start больше finish
        azim_insert = np.linspace(start=azim[start], stop=azim[finish], num=5)[1:-1]
        azim[where_nan] = azim_insert
    elif well_interval == 2:
        if all(incl[1:] <= 3):
            start_angle = 0
            for nan_row in where_nan:
                azim[nan_row] = start_angle // 360
                start_angle += 45
        elif (all(incl[1:] <= 3)) and (all(incl[1:] >= 10)) :
            start_angle = 0
            for nan_row in where_nan:
                azim[nan_row] = start_angle // 360
                start_angle += 90
        else:
            NotImplementedError
else:
    NotImplementedError
print(azim)





        # fixme учесть случай когда start больше finish
        #azim_insert = np.linspace(start=azim[start], stop=azim[finish], num=5)[1:-1]
        #azim[where_nan] = azim_insert
        #print(all_data[:, 7])











