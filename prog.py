import numpy as np

N = input()
N = int(N)

distance_matrix = np.zeros(shape=[N, N], dtype=int)
for i in range(N):
    distance_matrix[i] = input().split()

distance_matrix_work = np.array(distance_matrix)
distance_matrix_sort = []

'''1 Подготовка матрицы расстояний'''

'''1.1 Сортировка ребер по длине'''
while (distance_matrix_work != 0).sum() != 0:
    distance_matrix_max = distance_matrix_work[distance_matrix_work != 0].max()
    for i in range(N):
        for j in range(0, N):
            if (distance_matrix_work[i][j] != 0
                    and distance_matrix_work[i][j] == distance_matrix_max):
                distance_matrix_sort += [[i, j, distance_matrix_work[i][j]]]
                distance_matrix_work[i][j] = 0

'''1.2 Поочередная проверка ребер и их удаление,
в случае если ребро выгоднее обойти по какому-либо пути'''
for i in range(len(distance_matrix_sort)):
    distance_matrix_work = np.array(distance_matrix)
    x = distance_matrix_sort[i][0]
    y = distance_matrix_sort[i][1]
    val = distance_matrix_sort[i][2]

    tops = [False]*N
    distance_matrix_work[x][y] = 0
    tops[x] = True
    x_new = x
    s = 0
    r = []
    stop = False

    while not(stop):
        inv_tops = [False] * N
        for k in range(N):
            inv_tops[k] = not(tops[k])
        if sum((distance_matrix_work[x_new] * inv_tops) != 0) > 1:
            v = []
            for c in range(N):
                if distance_matrix_work[x_new][c] != 0 and inv_tops[c]:
                    v += [c]
            r += [[x_new, s, v]]
            x_old = x_new
            x_new = r[len(r) - 1][2][0]
            del(r[len(r) - 1][2][0])
            if r[len(r) - 1][2] == []:
                del (r[len(r) - 1])
        elif sum((distance_matrix_work[x_new] * inv_tops) != 0) == 1:
            x_old = x_new
            x_new = ((distance_matrix_work[x_new] *
                      inv_tops) != 0).tolist().index(True)
        else:
            if r != []:
                x_old = r[len(r) - 1][0]
                x_new = r[len(r) - 1][2][0]
                s = r[len(r) - 1][1]
                del (r[len(r) - 1][2][0])
                if r[len(r) - 1][2] == []:
                    del (r[len(r) - 1])
            else:
                stop = True
                break
        s += distance_matrix_work[x_old][x_new]
        if x_new == y:
            if s < val:
                distance_matrix[x][y] = 0
                stop = True
                break
            else:
                if r != []:
                    x_new = r[len(r) - 1][2][0]
                    x_old = r[len(r) - 1][0]
                    s = r[len(r) - 1][1]
                    del (r[len(r) - 1][2][0])
                    if r[len(r) - 1][2] == []:
                        del (r[len(r) - 1])
                    s += distance_matrix_work[x_old][x_new]
                else:
                    stop = True
                    break
        elif x_new == x:
            if r != []:
                x_new = r[len(r) - 1][2][0]
                x_old = r[len(r) - 1][0]
                s = r[len(r) - 1][1]
                del (r[len(r) - 1][2][0])
                if r[len(r) - 1][2] == []:
                    del (r[len(r) - 1])
                s += distance_matrix_work[x_old][x_new]
            else:
                stop = True
                break
        else:
            pass
        distance_matrix_work[x_old][x_new] = 0
        tops[x_new] = True


'''2 Введем разделение графов на ориентированные и неориентированные'''
symmetry = (distance_matrix != distance_matrix.T).sum == 0

'''3 Обход графа'''
'''Обход делаем методом нахождения ближайшего соседа'''
tops = [True] * N
tops[0] = False
tops_distance = np.full([1, N], 10**9, dtype=int)[0]
for i in range(N):
    if distance_matrix[i, 0] != 0:
        tops_distance[i] = distance_matrix[i, 0]
    else:
        pass
tops_distance[0] = 0
road = 0
i_finish = 0
i = 0
dist = np.array(distance_matrix)
r = []
stop = False
road_all = []

while not(stop):
    while i != i_finish or sum(tops) != 0:
        if sum(dist[i] * tops != 0) > 0:
            distanse_to_top_before = tops_distance[i]
            min_way = np.zeros([1, N], dtype=int)[0]

            for kol in range(N):
                if dist[i][kol] == 0 or not(tops[kol]):
                    min_way[kol] = 10**9
                else:
                    min_way[kol] = dist[i][kol]
            '''Для симметричной матрицы расстояний придерживаемся правила
            нахождения ближайшего соседа. В случае, 
            если минимальных путей из данной точки несколько, 
            то будем проверять путь для каждого ближайшего соседа'''
            if symmetry and sum(min_way == min(min_way)) > 1:
                v = []
                for c in range(N):
                    if min_way[c] == min(min_way):
                        v += [c]
                r += [[i, road,
                       list(tops),
                       np.array(tops_distance),
                       i_finish,
                       v]]
                i_new = r[len(r) - 1][5][0]
                del (r[len(r) - 1][5][0])
                if r[len(r) - 1][5] == []:
                    del (r[len(r) - 1])
                ''' В случае несимметричной матрицы алгоритм выбора ближайшего соседа 
                не даст минимальный путь обхода графа. В этом случае используем 
                полный перебор для всех соседей текущей точки.'''
            elif not(symmetry):
                v = []
                for c in range(N):
                    if min_way[c] != 10**9:
                        v += [c]
                r += [[i,
                       road,
                       list(tops),
                       np.array(tops_distance),
                       i_finish,
                       v]]
                i_new = r[len(r) - 1][5][0]
                del (r[len(r) - 1][5][0])
                if r[len(r) - 1][5] == []:
                    del (r[len(r) - 1])
            else:
                i_new = np.argmin(min_way)

            step = dist[i][i_new]
            step_to_back = dist[i_new][i]
            i = i_new
            tops[i] = False

            if tops_distance[i] == 10 ** 9 and step_to_back != 0:
                tops_distance[i] = distanse_to_top_before + step_to_back

            road += step
            '''Если мы побывали во всех точках, 
            то возвращаемся в 0 по кротчайшему пути'''
        elif (i != i_finish) and sum(dist[i] * tops != 0) == 0:
            inv_tops = [False] * N

            for k in range(N):
                inv_tops[k] = not(tops[k])
            min_way = np.zeros([1, N], dtype=int)[0]

            for kol in range(N):
                if dist[i][kol] == 0:
                    min_way[kol] = 10**9
                else:
                    min_way[kol] = tops_distance[kol] + dist[i][kol]

            i_new = np.argmin(min_way)
            step = dist[i][i_new]
            i = i_new
            road += step
            '''Если в графе существует мост, 
            который мы не обойдем и при этом уже достигнем 0, 
            то рассмотрим его в отдельном порядке'''
        elif (i == i_finish) and sum(tops) != 0:
            start = 0
            inv_tops = [False] * N

            for k in range(N):
                inv_tops[k] = not(tops[k])
            way = (((dist * tops).T * inv_tops).T).sum(axis=0)
            min_way = np.zeros([1, N], dtype=int)[0]

            for kol in range(N):
                if way[kol] == 0:
                    min_way[kol] = 10 ** 9
                else:
                    min_way[kol] = way[kol]

            bridge_end = np.argmin(min_way)
            min_way = np.zeros([1, N], dtype=int)[0]

            for kol in range(N):
                if (dist[:, bridge_end]*inv_tops)[kol] == 0:
                    min_way[kol] = 10 ** 9
                else:
                    min_way[kol] = (dist[:, bridge_end]*inv_tops)[kol]

            bridge_start = np.argmin(min_way)
            i = bridge_start
            i_finish = bridge_start
    '''Для выполнения перебора будем последовательно возвращаться
     в специально зафиксированные точки и начинать алгоритм с них '''
    if r != []:
        road_all += [road]
        i_old = r[len(r) - 1][0]
        i_new = r[len(r) - 1][5][0]
        road = r[len(r) - 1][1] + dist[i_old][i_new]

        i_finish = r[len(r) - 1][4]
        tops = list(r[len(r) - 1][2])
        tops_distanse = np.array(r[len(r) - 1][3])
        i = i_new
        tops[i] = False
        distanse_to_top_before = tops_distance[i_old]
        if tops_distance[i] == 10 ** 9:
            tops_distance[i] = distanse_to_top_before + dist[i_old][i_new]

        del (r[len(r) - 1][5][0])
        if r[len(r) - 1][5] == []:
            del (r[len(r) - 1])
    else:
        stop = True

if road_all == []:
    print(road)
else:
    print(min(road_all + [road]))