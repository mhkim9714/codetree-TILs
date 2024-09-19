import copy

N,M,K = map(int, input().split())
init = [list(map(int, input().split())) for _ in range(N)]
arr = [[[] for _ in range(M)] for _ in range(N)]
for i in range(N):
    for j in range(M):
        arr[i][j] = [init[i][j], 0]


def BFS(ai,aj,ti,tj):
    q = []
    visited = [[0 for _ in range(M)] for _ in range(N)]
    route = [[[] for _ in range(M)] for _ in range(N)]

    q.append((ai,aj))
    visited[ai][aj] = 1
    route[ai][aj].append((ai,aj))

    while q:
        ci,cj = q.pop(0)
        for di,dj in ((0,1),(1,0),(0,-1),(-1,0)):
            ni,nj = (ci+di)%N, (cj+dj)%M
            if arr[ni][nj][0] != 0 and visited[ni][nj] == 0:
                q.append((ni,nj))
                visited[ni][nj] = 1
                tmp = copy.deepcopy(route[ci][cj])
                tmp.append((ni,nj))
                route[ni][nj] = tmp

                if (ni,nj) == (ti,tj):
                    return route[ti][tj]

    return route[ti][tj]


for round in range(1,K+1):
    # 공격자 선정
    attk_p, attk_t, attk_i, attk_j = 10e+4, -1, -1, -1
    for i in range(N):
        for j in range(M):
            if arr[i][j][0] != 0:
                if attk_p > arr[i][j][0]:
                    attk_p, attk_t, attk_i, attk_j = arr[i][j][0], arr[i][j][1], i, j
                elif attk_p == arr[i][j][0]:
                    if attk_t < arr[i][j][1]:
                        attk_p, attk_t, attk_i, attk_j = arr[i][j][0], arr[i][j][1], i, j
                    elif attk_t == arr[i][j][1]:
                        if attk_i+attk_j < i+j:
                            attk_p, attk_t, attk_i, attk_j = arr[i][j][0], arr[i][j][1], i, j
                        elif attk_i+attk_j == i+j:
                            if attk_j < j:
                                attk_p, attk_t, attk_i, attk_j = arr[i][j][0], arr[i][j][1], i, j
    arr[attk_i][attk_j][0] += (N+M)

    # 공격자 공격
    tgt_p, tgt_t, tgt_i, tgt_j = -1, K+1, N, M
    for i in range(N):
        for i in range(N):
            for j in range(M):
                if (i,j) != (attk_i,attk_j):
                    if tgt_p < arr[i][j][0]:
                        tgt_p, tgt_t, tgt_i, tgt_j = arr[i][j][0], arr[i][j][1], i, j
                    elif tgt_p == arr[i][j][0]:
                        if tgt_t > arr[i][j][1]:
                            tgt_p, tgt_t, tgt_i, tgt_j = arr[i][j][0], arr[i][j][1], i, j
                        elif tgt_t == arr[i][j][1]:
                            if tgt_i+tgt_j > i+j:
                                tgt_p, tgt_t, tgt_i, tgt_j = arr[i][j][0], arr[i][j][1], i, j
                            elif tgt_i+tgt_j == i+j:
                                if tgt_j < j:
                                    tgt_p, tgt_t, tgt_i, tgt_j = arr[i][j][0], arr[i][j][1], i, j

    bombed = BFS(attk_i, attk_j, tgt_i, tgt_j)

    if len(bombed) != 0: # 레이저 공격
        affected = copy.deepcopy(bombed)
        arr[attk_i][attk_j][1] = round
        bombed.remove((attk_i,attk_j))
        arr[tgt_i][tgt_j][0] = max(arr[tgt_i][tgt_j][0]-arr[attk_i][attk_j][0], 0)
        bombed.remove((tgt_i, tgt_j))
        for i,j in bombed:
            arr[i][j][0] = max(arr[i][j][0]-(arr[attk_i][attk_j][0]//2), 0)

    else: # 포탄 공격
        affected = [(attk_i,attk_j),(tgt_i,tgt_j)]
        arr[attk_i][attk_j][1] = round
        arr[tgt_i][tgt_j][0] = max(arr[tgt_i][tgt_j][0]-arr[attk_i][attk_j][0], 0)
        for di,dj in ((-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1)):
            ni,nj = (tgt_i+di)%N, (tgt_j+dj)%M
            if (ni,nj) != (attk_i,attk_j):
                arr[ni][nj][0] = max(arr[ni][nj][0]-(arr[attk_i][attk_j][0]//2), 0)
                affected.append((ni,nj))

    # 포탑 부서짐 & 포탑 정비
    alive_cnt = 0
    for i in range(N):
        for j in range(M):
            if arr[i][j][0] > 0:
                alive_cnt += 1

            if arr[i][j][0] != 0 and (i,j) not in affected:
                arr[i][j][0] += 1

    if alive_cnt == 1:
        break

max_p = 0
for i in range(N):
    for j in range(M):
        if arr[i][j][0] > max_p:
            max_p = arr[i][j][0]
print(max_p)