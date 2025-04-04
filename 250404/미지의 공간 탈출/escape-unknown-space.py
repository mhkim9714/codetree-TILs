import copy

# 동0 서1 남2 북3
di = [0, 0, 1, -1]
dj = [1, -1, 0, 0]

N, M, F = map(int, input().split())

cnt = 0
start_idx = -1
exit_idx = -1

bottom = [list(map(int, input().split())) for _ in range(N)]  # 0빈칸, 1장애물, 3시간의벽, 4탈출구 / 여기에만 시간 이상 현상 존재
bottom_idx = [[0 for _ in range(N)] for _ in range(N)]
east = [list(map(int, input().split())) for _ in range(M)]  # 0빈칸, 1장애물
east_idx = [[0 for _ in range(M)] for _ in range(M)]
west = [list(map(int, input().split())) for _ in range(M)]  # 0빈칸, 1장애물
west_idx = [[0 for _ in range(M)] for _ in range(M)]
south = [list(map(int, input().split())) for _ in range(M)]  # 0빈칸, 1장애물
south_idx = [[0 for _ in range(M)] for _ in range(M)]
north = [list(map(int, input().split())) for _ in range(M)]  # 0빈칸, 1장애물
north_idx = [[0 for _ in range(M)] for _ in range(M)]
top = [list(map(int, input().split())) for _ in range(M)]  # 0빈칸, 1장애물, 2시작점
top_idx = [[0 for _ in range(M)] for _ in range(M)]

arr = [bottom, east, west, south, north, top]
vertice = []

for i in range(N):
    for j in range(N):
        if bottom[i][j] == 4:
            exit_idx = cnt
        bottom_idx[i][j] = cnt
        vertice.append([0, (i, j)])
        cnt += 1

for i in range(M):
    for j in range(M):
        east_idx[i][j] = cnt
        vertice.append([1, (i, j)])
        cnt += 1

for i in range(M):
    for j in range(M):
        west_idx[i][j] = cnt
        vertice.append([2, (i, j)])
        cnt += 1

for i in range(M):
    for j in range(M):
        south_idx[i][j] = cnt
        vertice.append([3, (i, j)])
        cnt += 1

for i in range(M):
    for j in range(M):
        north_idx[i][j] = cnt
        vertice.append([4, (i, j)])
        cnt += 1

for i in range(M):
    for j in range(M):
        if top[i][j] == 2:
            start_idx = cnt
        top_idx[i][j] = cnt
        vertice.append([5, (i, j)])
        cnt += 1

anomalies = dict()
for idx in range(1, F+1):
    r, c, d, v = map(int, input().split())
    anomalies[idx] = [r, c, d, v]

adj_list = [[-1,-1,-1,-1] for _ in range(cnt)]  # 모든 idx마다 [동,서,남,북]

# bottom 내부 연결
for i in range(N):
    for j in range(N):
        idx = bottom_idx[i][j]
        for d in range(4):
            ni, nj = i+di[d], j+dj[d]
            if 0<=ni<N and 0<=nj<N:
                adj_list[idx][d] = bottom_idx[ni][nj]

# bottom-side 연결
si, sj = -1, -1
for i in range(N):
    if (si, sj) != (-1, -1):
        break
    for j in range(N):
        if bottom[i][j] == 3:
            si, sj = i, j
            break

# bottom-동side
for i in range(si, si+M):
    adj_list[bottom_idx[i][sj+M-1+1]][1] = east_idx[M-1][M-1-(i-si)]
    adj_list[east_idx[M-1][M-1-(i-si)]][2] = bottom_idx[i][sj+M-1+1]

# bottom-서side
for i in range(si, si+M):
    adj_list[bottom_idx[i][sj-1]][0] = west_idx[M-1][i-si]
    adj_list[west_idx[M-1][i-si]][2] = bottom_idx[i][sj-1]

# bottom-남side
for j in range(sj, sj+M):
    adj_list[bottom_idx[si+M-1+1][j]][3] = south_idx[M-1][j-sj]
    adj_list[south_idx[M-1][j-sj]][2] = bottom_idx[si+M-1+1][j]

# bottom-북side
for j in range(sj, sj+M):
    adj_list[bottom_idx[si-1][j]][2] = north_idx[M-1][M-1-(j-sj)]
    adj_list[north_idx[M-1][M-1-(j-sj)]][2] = bottom_idx[si-1][j]

# side 각각 내부 연결
# 동side
for i in range(M):
    for j in range(M):
        idx = east_idx[i][j]
        for d in range(4):
            ni, nj = i+di[d], j+dj[d]
            if 0<=ni<M and 0<=nj<M:
                adj_list[idx][d] = east_idx[ni][nj]

# 서side
for i in range(M):
    for j in range(M):
        idx = west_idx[i][j]
        for d in range(4):
            ni, nj = i+di[d], j+dj[d]
            if 0<=ni<M and 0<=nj<M:
                adj_list[idx][d] = west_idx[ni][nj]

# 남side
for i in range(M):
    for j in range(M):
        idx = south_idx[i][j]
        for d in range(4):
            ni, nj = i+di[d], j+dj[d]
            if 0<=ni<M and 0<=nj<M:
                adj_list[idx][d] = south_idx[ni][nj]

# 북side
for i in range(M):
    for j in range(M):
        idx = north_idx[i][j]
        for d in range(4):
            ni, nj = i+di[d], j+dj[d]
            if 0<=ni<M and 0<=nj<M:
                adj_list[idx][d] = north_idx[ni][nj]

# side 끼리 연결
# 동<->북
for x in range(M):
    adj_list[east_idx[x][M-1]][0] = north_idx[x][0]
    adj_list[north_idx[x][0]][1] = east_idx[x][M-1]

# 북<->서
for x in range(M):
    adj_list[north_idx[x][M-1]][0] = west_idx[x][0]
    adj_list[west_idx[x][0]][1] = north_idx[x][M-1]

# 서<->남
for x in range(M):
    adj_list[west_idx[x][M-1]][0] = south_idx[x][0]
    adj_list[south_idx[x][0]][1] = west_idx[x][M-1]

# 남<->동
for x in range(M):
    adj_list[south_idx[x][M-1]][0] = east_idx[x][0]
    adj_list[east_idx[x][0]][1] = south_idx[x][M-1]

# side-top 연결
# top-동side
for x in range(M):
    adj_list[top_idx[x][M-1]][0] = east_idx[0][M-1-x]
    adj_list[east_idx[0][M-1-x]][3] = top_idx[x][M-1]

# top-서side
for x in range(M):
    adj_list[top_idx[x][0]][1] = west_idx[0][x]
    adj_list[west_idx[0][x]][3] = top_idx[x][0]

# top-남side
for x in range(M):
    adj_list[top_idx[M-1][x]][2] = south_idx[0][x]
    adj_list[south_idx[0][x]][3] = top_idx[M-1][x]

# top-북side
for x in range(M):
    adj_list[top_idx[0][x]][3] = north_idx[0][M-1-x]
    adj_list[north_idx[0][M-1-x]][3] = top_idx[0][x]

# top 내부 연결
for i in range(M):
    for j in range(M):
        idx = top_idx[i][j]
        for d in range(4):
            ni, nj = i+di[d], j+dj[d]
            if 0<=ni<M and 0<=nj<M:
                adj_list[idx][d] = top_idx[ni][nj]


time = 1
q = [start_idx]
visited = set()
visited.add(start_idx)

for anom_idx, info in anomalies.items():
    arr[0][info[0]][info[1]] = 1

while True:
    # 이상 현상 확산
    if len(anomalies) > 0:
        del_anom_idx = []
        new_bottom = copy.deepcopy(arr[0])
        for anom_idx, info in anomalies.items():
            if time % info[3] == 0:
                n_anom_i, n_anom_j = info[0] + (time//info[3])*di[info[2]], info[1] + (time//info[3])*dj[info[2]]
                if 0<=n_anom_i<N and 0<=n_anom_j<N:
                    if arr[0][n_anom_i][n_anom_j] == 0:
                        new_bottom[n_anom_i][n_anom_j] = 1
                    else:
                        del_anom_idx.append(anom_idx)
                else:
                    del_anom_idx.append(anom_idx)

        arr[0] = new_bottom
        for anom_idx in del_anom_idx:
            del anomalies[anom_idx]

    # BFS 한 스텝 수행
    next_q = []
    while q:
        c_idx = q.pop(0)
        for d in range(4):
            n_idx = adj_list[c_idx][d]
            if n_idx == -1:
                continue
            where, n_loc = vertice[n_idx]
            if arr[where][n_loc[0]][n_loc[1]] in [0, 4] and n_idx not in visited:
                next_q.append(n_idx)
                visited.add(n_idx)

                if n_idx == exit_idx:
                    print(time)
                    exit()

    q = next_q
    if len(q) == 0:
        print(-1)
        exit()

    time += 1
