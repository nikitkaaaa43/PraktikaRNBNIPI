import numpy as np


name = "# WELL NAME:"
head_x_coordinate = "# WELL HEAD X-COORDINATE:"
head_y_coordinate = "# WELL HEAD Y-COORDINATE:"
KB = '# WELL KB:'
gr = '#====='
name_cols = '      MD'

with open('1234-new.txt') as f:
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

fname = '1234 - corrupted.txt'
a = np.loadtxt(fname, skiprows=str_gr, usecols=(1,2,3,4,5,6))
print(a)



#KEY_FOR_SEARCH = input('Что будем искать?\n')
#PATH_FOR_COPY = input('Куда скопировать файлы?\n')

#def search():
#   for adress, dirs, files in os.walk(input('Введите путь откуда начать поиск\n')):
#        for file in files:
#            if file.endswith('.txt') and '$' not in file:
#                yield os.path.join(adress, file)

#def read_from_pathtxt(path):
#    with open(path) as r:
#        for i in r:
#            if KEY_FOR_SEARCH in i:
#                return copy(path)

#def copy(path):
#    file_name = path.split('\\')[-1]

#    shutil.copyfile(path, os.path.join(PATH_FOR_COPY, file_name))
#    print('Файл скопирован', file_name)

#for i in search():
#    try:
#        read_from_pathtxt(i)
#    except Exception as e:
#        with open(os.path.join(PATH_FOR_COPY, 'errors.txt'), 'a') as r:
#            r.write(str(e) + '\n' + i + '\n')








