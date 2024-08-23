N,M,K = map(int, input().split())

arr = [[[] for _ in range(M)] for _ in range(N)]
temp = [list(map(int, input().split())) for _ in range(N)]
for i in range(N):
    for j in range(M):
        if temp[i][j] != 0:
            arr[i][j] = [temp[i][j],0,0]

# 우0 하1 좌2 상3
di = [0, 1, 0, -1]
dj = [1, 0, -1, 0]


for turn in range(1,K+1):
    # 공격자 선정
    min_power,last_attack,attk_i,attk_j = 10000,-1,-1,-1
    for i in range(N):
        for j in range(M):
            if len(arr[i][j]) > 0:
                if min_power > arr[i][j][0]:
                    min_power,last_attack,attk_i,attk_j = arr[i][j][0],arr[i][j][1],i,j
                elif min_power == arr[i][j][0]:
                    if last_attack < arr[i][j][1]:
                        min_power,last_attack,attk_i,attk_j = arr[i][j][0],arr[i][j][1],i,j
                    elif last_attack == arr[i][j][1]:
                        if attk_i+attk_j < i+j:
                            min_power,last_attack,attk_i,attk_j = arr[i][j][0],arr[i][j][1],i,j
                        elif attk_i+attk_j == i+j:
                            if attk_j < j:
                                min_power,last_attack,attk_i,attk_j = arr[i][j][0],arr[i][j][1],i,j

    arr[attk_i][attk_j][0] += (M+N)

    # 공격 타겟 선정
    max_power,last_attack,tgt_i,tgt_j = -1,10000,-1,-1
    for i in range(N):
        for j in range(M):
            if (i,j) == (attk_i,attk_j):
                continue
            if len(arr[i][j]) > 0:
                if max_power < arr[i][j][0]:
                    max_power,last_attack,tgt_i,tgt_j = arr[i][j][0],arr[i][j][1],i,j
                elif max_power == arr[i][j][0]:
                    if last_attack > arr[i][j][1]:
                        max_power,last_attack,tgt_i,tgt_j = arr[i][j][0],arr[i][j][1],i,j
                    elif last_attack == arr[i][j][1]:
                        if tgt_i+tgt_j > i+j:
                            max_power,last_attack,tgt_i,tgt_j = arr[i][j][0],arr[i][j][1],i,j
                        elif tgt_i+tgt_j == i+j:
                            if tgt_j > j:
                                max_power,last_attack,tgt_i,tgt_j = arr[i][j][0],arr[i][j][1],i,j

    # 공격
    q = []
    visited = [[-2 for _ in range(N)] for _ in range(M)]

    q.append((attk_i,attk_j))
    visited[attk_i][attk_j] = -1

    laser_flag = 0
    while q:
        ci,cj = q.pop(0)
        for d in range(4):
            ni,nj = (ci+di[d]+4)%4, (cj+dj[d]+4)%4
            if visited[ni][nj]==-2 and len(arr[ni][nj])>0:
                q.append((ni,nj))
                visited[ni][nj] = (d+2)%4

                if (ni,nj) == (tgt_i,tgt_j): # 레이저 공격
                    pi,pj = tgt_i,tgt_j
                    involved = [(pi,pj)]
                    while True:
                        pi,pj = (pi+di[visited[pi][pj]]+4)%4, (pj+dj[visited[pi][pj]]+4)%4
                        involved.append((pi,pj))
                        if visited[pi][pj] == -1:
                            break

                    for i,j in involved:
                        if (i,j) == (attk_i,attk_j):
                            arr[i][j][1] = turn
                            arr[i][j][2] = 1
                        elif (i,j) == (tgt_i,tgt_j):
                            if arr[i][j][0] > arr[attk_i][attk_j][0]:
                                arr[i][j][0] -= arr[attk_i][attk_j][0]
                                arr[i][j][2] = 1
                            else:
                                arr[i][j] = []
                        else:
                            if arr[i][j][0] > (arr[attk_i][attk_j][0]//2):
                                arr[i][j][0] -= (arr[attk_i][attk_j][0]//2)
                                arr[i][j][2] = 1
                            else:
                                arr[i][j] = []
                    laser_flag = 1
                    break

    if laser_flag == 0: # 포탄 공격
        involved = [(attk_i,attk_j),(tgt_i,tgt_j)]
        for ddi,ddj in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)):
            involved.append(((tgt_i+di[ddi]+4)%4, (tgt_j+dj[ddj]+4)%4))

        for i, j in involved:
            if len(arr[i][j]) > 0:
                if (i, j) == (attk_i, attk_j):
                    arr[i][j][1] = turn
                    arr[i][j][2] = 1
                elif (i, j) == (tgt_i, tgt_j):
                    if arr[i][j][0] > arr[attk_i][attk_j][0]:
                        arr[i][j][0] -= arr[attk_i][attk_j][0]
                        arr[i][j][2] = 1
                    else:
                        arr[i][j] = []
                else:
                    if arr[i][j][0] > (arr[attk_i][attk_j][0] // 2):
                        arr[i][j][0] -= (arr[attk_i][attk_j][0] // 2)
                        arr[i][j][2] = 1
                    else:
                        arr[i][j] = []

    # 포탑 정비 & 종료 조건
    cnt_alive = 0
    for i in range(N):
        for j in range(M):
            if len(arr[i][j])>0:
                cnt_alive += 1
                if arr[i][j][2]!=1:
                    arr[i][j][0] += 1
    if cnt_alive == 1:
        break

ans = -1
for i in range(N):
    for j in range(M):
        if len(arr[i][j]) > 0:
            if arr[i][j][0] > ans:
                ans = arr[i][j][0]
print(ans)