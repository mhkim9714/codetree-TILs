# 우0, 하1, 좌2, 상3
di = [0, 1, 0, -1]
dj = [1, 0, -1, 0]

N, M, K = map(int, input().split())
arr = [[[] for _ in range(M)] for _ in range(N)]
tmp = [list(map(int, input().split())) for _ in range(N)]
for i in range(N):
    for j in range(M):
        arr[i][j] = [tmp[i][j], 0]  # [공격력, 최근 공격 시점]


def BFS(si, sj, ei, ej):  # s:공격자 / e:대상자
    q = []
    visited = [[0 for _ in range(M)] for _ in range(N)]

    q.append((si,sj))
    visited[si][sj] = (si,sj)
    end_flag = 0

    while q:
        ci, cj = q.pop(0)
        for d in range(4):
            ni, nj = (ci+di[d])%N, (cj+dj[d])%M
            if arr[ni][nj][0]!=0 and visited[ni][nj]==0:
                q.append((ni, nj))
                visited[ni][nj] = (ci, cj)
                if (ni, nj) == (ei, ej):
                    end_flag = 1
                    break
        if end_flag == 1:
            break

    if visited[ei][ej] != 0:
        path = []
        ci, cj = ei, ej
        while True:
            path.append((ci,cj))
            ni, nj = visited[ci][cj]
            if (ci, cj) == (ni, nj):
                break
            else:
                ci, cj = ni, nj
        return path
    else:
        return []


for turn in range(1,K+1):
    # 1. 공격자 선정
    min_power, max_attk_time, attk_i, attk_j = 10000, -1, -1, -1
    for i in range(N):
        for j in range(M):
            if arr[i][j][0] == 0:
                continue
            if min_power > arr[i][j][0]:
                min_power, max_attk_time, attk_i, attk_j = arr[i][j][0], arr[i][j][1], i, j
            elif min_power == arr[i][j][0]:
                if max_attk_time < arr[i][j][1]:
                    min_power, max_attk_time, attk_i, attk_j = arr[i][j][0], arr[i][j][1], i, j
                elif max_attk_time == arr[i][j][1]:
                    if attk_i+attk_j < i+j:
                        min_power, max_attk_time, attk_i, attk_j = arr[i][j][0], arr[i][j][1], i, j
                    elif attk_i+attk_j == i+j:
                        if attk_j < j:
                            min_power, max_attk_time, attk_i, attk_j = arr[i][j][0], arr[i][j][1], i, j

    arr[attk_i][attk_j][0] += (M+N)
    arr[attk_i][attk_j][1] = turn

    # 2. 공격자의 공격 & 3. 포탑 부서짐
    # 대상자 선정
    max_power, min_attk_time, tgt_i, tgt_j = -1, 10000, N, M
    for i in range(N):
        for j in range(M):
            if (i,j) == (attk_i,attk_j):
                continue
            if max_power < arr[i][j][0]:
                max_power, min_attk_time, tgt_i, tgt_j = arr[i][j][0], arr[i][j][1], i, j
            elif max_power == arr[i][j][0]:
                if min_attk_time > arr[i][j][1]:
                    max_power, min_attk_time, tgt_i, tgt_j = arr[i][j][0], arr[i][j][1], i, j
                elif min_attk_time == arr[i][j][1]:
                    if tgt_i+tgt_j > i+j:
                        max_power, min_attk_time, tgt_i, tgt_j = arr[i][j][0], arr[i][j][1], i, j
                    elif tgt_i+tgt_j == i+j:
                        if tgt_j > j:
                            max_power, min_attk_time, tgt_i, tgt_j = arr[i][j][0], arr[i][j][1], i, j

    # 최단 경로 구하기
    relevant = BFS(attk_i, attk_j, tgt_i, tgt_j)

    if len(relevant) != 0:
        # (1) 레이저 공격
        for i, j in relevant:
            if (i, j) == (attk_i, attk_j):
                continue
            elif (i, j) == (tgt_i, tgt_j):
                arr[i][j][0] = max(0, arr[i][j][0]-arr[attk_i][attk_j][0])
            else:
                arr[i][j][0] = max(0, arr[i][j][0]-arr[attk_i][attk_j][0]//2)
    else:
        # (2) 포탄 공격
        relevant.append((attk_i, attk_j))
        relevant.append((tgt_i, tgt_j))
        arr[tgt_i][tgt_j][0] = max(0, arr[tgt_i][tgt_j][0]-arr[attk_i][attk_j][0])
        for di8, dj8 in ((-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)):
            affected_i, affected_j = (tgt_i+di8)%N, (tgt_j+dj8)%M
            if (affected_i, affected_j) != (attk_i, attk_j):
                relevant.append((affected_i, affected_j))
                arr[affected_i][affected_j][0] = max(0, arr[affected_i][affected_j][0]-arr[attk_i][attk_j][0]//2)

    # 3'. 종료 조건
    cnt_alive = 0
    for i in range(N):
        for j in range(M):
            if arr[i][j][0] > 0:
                cnt_alive += 1

    if cnt_alive <= 1:
        break

    # 4. 포탑 정비
    for i in range(N):
        for j in range(M):
            if arr[i][j][0] == 0:
                continue
            else:
                if (i,j) in relevant:
                    continue
                else:
                    arr[i][j][0] += 1


max_power = -1
for i in range(N):
    for j in range(M):
        if max_power < arr[i][j][0]:
            max_power = arr[i][j][0]
print(max_power)




