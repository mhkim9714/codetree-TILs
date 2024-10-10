N,M,K = map(int, input().split())
tmp = [list(map(int, input().split())) for _ in range(N)]

arr = [[[] for _ in range(M)] for _ in range(N)]
for i in range(N):
    for j in range(M):
        arr[i][j] = [tmp[i][j], 0]


def BFS(si,sj,ei,ej):
    q = []
    visited = [[(-1,-1) for _ in range(M)] for _ in range(N)]

    q.append((si,sj))
    visited[si][sj] = (si,sj)

    while q:
        ci,cj = q.pop(0)
        for di,dj in [(0,1),(1,0),(0,-1),(-1,0)]:
            ni,nj = (ci+di)%N, (cj+dj)%M
            if visited[ni][nj] == (-1,-1) and arr[ni][nj][0] > 0:
                q.append((ni,nj))
                visited[ni][nj] = (ci,cj)

                if (ni,nj) == (ei,ej):
                    fci,fcj = ei,ej
                    out = []
                    while True:
                        out.append((fci,fcj))
                        fbi,fbj = visited[fci][fcj]
                        if (fci,fcj) != (fbi,fbj):
                            fci,fcj = fbi,fbj
                        else:
                            break
                    return out

    return [(si,sj)]


for t in range(1,K+1):
    # 1) 공격자 선정
    attk_pow, attk_t, attk_i, attk_j = 5001, -1, -1, -1
    for i in range(N):
        for j in range(M):
            if arr[i][j][0] == 0:
                continue

            if attk_pow > arr[i][j][0]:
                attk_pow, attk_t, attk_i, attk_j = arr[i][j][0], arr[i][j][1], i, j
            elif attk_pow == arr[i][j][0]:
                if attk_t < arr[i][j][1]:
                    attk_pow, attk_t, attk_i, attk_j = arr[i][j][0], arr[i][j][1], i, j
                elif attk_t == arr[i][j][1]:
                    if attk_i + attk_j < i + j:
                        attk_pow, attk_t, attk_i, attk_j = arr[i][j][0], arr[i][j][1], i, j
                    elif attk_i + attk_j == i + j:
                        if attk_j < j:
                            attk_pow, attk_t, attk_i, attk_j = arr[i][j][0], arr[i][j][1], i, j

    arr[attk_i][attk_j][0] += (N+M)

    # 2) 공격자 공격
    tgt_pow, tgt_t, tgt_i, tgt_j = -1, K+1, N, M
    for i in range(N):
        for j in range(M):
            if (i,j) == (attk_i,attk_j):
                continue

            if tgt_pow < arr[i][j][0]:
                tgt_pow, tgt_t, tgt_i, tgt_j = arr[i][j][0], arr[i][j][1], i, j
            elif tgt_pow == arr[i][j][0]:
                if tgt_t > arr[i][j][1]:
                    tgt_pow, tgt_t, tgt_i, tgt_j = arr[i][j][0], arr[i][j][1], i, j
                elif tgt_t == arr[i][j][1]:
                    if tgt_i + tgt_j > i + j:
                        tgt_pow, tgt_t, tgt_i, tgt_j = arr[i][j][0], arr[i][j][1], i, j
                    elif tgt_i + tgt_j == i + j:
                        if tgt_j > j:
                            tgt_pow, tgt_t, tgt_i, tgt_j = arr[i][j][0], arr[i][j][1], i, j

    affected = BFS(attk_i, attk_j, tgt_i, tgt_j)

    if len(affected) > 1: # 레이저 공격
        for i,j in affected:
            if (i,j) == (attk_i,attk_j):
                continue
            elif (i,j) == (tgt_i,tgt_j):
                arr[i][j][0] = max(arr[i][j][0]-arr[attk_i][attk_j][0], 0)
            else:
                arr[i][j][0] = max(arr[i][j][0]-arr[attk_i][attk_j][0]//2, 0)

        arr[attk_i][attk_j][1] = t

    else: # 포탄 공격
        arr[tgt_i][tgt_j][0] = max(arr[tgt_i][tgt_j][0]-arr[attk_i][attk_j][0], 0)
        affected.append((tgt_i,tgt_j))

        for di,dj in [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]:
            ni,nj = (tgt_i+di)%N, (tgt_j+dj)%M
            if arr[ni][nj][0] > 0 and (ni,nj) != (attk_i,attk_j):
                arr[ni][nj][0] = max(arr[ni][nj][0]-arr[attk_i][attk_j][0]//2, 0)
                affected.append((ni,nj))

        arr[attk_i][attk_j][1] = t

    # 종료 조건
    cnt = 0
    for i in range(N):
        for j in range(M):
            if arr[i][j][0] > 0:
                cnt += 1
    if cnt == 1:
        break

    # 4) 포탑 정비
    for i in range(N):
        for j in range(M):
            if arr[i][j][0]>0 and (i,j) not in affected:
                arr[i][j][0] += 1

ans = -1
for i in range(N):
    for j in range(M):
        if ans < arr[i][j][0]:
            ans = arr[i][j][0]
print(ans)