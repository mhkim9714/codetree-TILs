N, M, K = map(int, input().split())
tmp = [list(map(int, input().split())) for _ in range(N)]

arr = [[[0, 0] for _ in range(M)] for _ in range(N)]  # [공격력, 최근 공격시점]
for i in range(N):
    for j in range(M):
        arr[i][j][0] = tmp[i][j]

# 우0 하1 좌2 상3
di = [0, 1, 0, -1]
dj = [1, 0, -1, 0]


for time in range(1, K+1):  # O(1000)

    # 1. 공격자 선정  # O(100)
    min_power, max_last_attk, max_ij, max_j = 5001, -1, -1, -1
    for i in range(N):
        for j in range(M):
            if arr[i][j][0] == 0:
                continue
            if arr[i][j][0] < min_power:
                min_power, max_last_attk, max_ij, max_j = arr[i][j][0], arr[i][j][1], i + j, j
            elif arr[i][j][0] == min_power:
                if arr[i][j][1] > max_last_attk:
                    min_power, max_last_attk, max_ij, max_j = arr[i][j][0], arr[i][j][1], i + j, j
                elif arr[i][j][1] == max_last_attk:
                    if i + j > max_ij:
                        min_power, max_last_attk, max_ij, max_j = arr[i][j][0], arr[i][j][1], i + j, j
                    elif i + j == max_ij:
                        if j > max_j:
                            min_power, max_last_attk, max_ij, max_j = arr[i][j][0], arr[i][j][1], i + j, j

    attk_i, attk_j = max_ij-max_j, max_j
    arr[attk_i][attk_j][0] += N+M
    arr[attk_i][attk_j][1] = time

    # 2. 공격자의 공격 & 3. 포탑 무너짐  # O(100)
    max_power, min_last_attk, min_ij, min_j = -1, K+1, N+M, M
    for i in range(N):
        for j in range(M):
            if (i, j) == (attk_i, attk_j):
                continue
            if arr[i][j][0] > max_power:
                max_power, min_last_attk, min_ij, min_j = arr[i][j][0], arr[i][j][1], i + j, j
            elif arr[i][j][0] == max_power:
                if arr[i][j][1] < min_last_attk:
                    max_power, min_last_attk, min_ij, min_j = arr[i][j][0], arr[i][j][1], i + j, j
                elif arr[i][j][1] == min_last_attk:
                    if i + j < min_ij:
                        max_power, min_last_attk, min_ij, min_j = arr[i][j][0], arr[i][j][1], i + j, j
                    elif i + j == min_ij:
                        if j < min_j:
                            max_power, min_last_attk, min_ij, min_j = arr[i][j][0], arr[i][j][1], i + j, j

    tgt_i, tgt_j = min_ij-min_j, min_j

    # BFS -> 공격자부터 타켓 포탑까지 가는 최단 경로 존재하는지 확인 (경로상 모든 좌표 저장); 부서진 포탑 못지남, 엣지 연결, affected 포함 {공격자 포탑, 경로상 지점, 타겟 포탑}
    q = []
    visited = [[[] for _ in range(M)] for _ in range(N)]  # 미방문: [], 시작점: [-1, -1], 경로상 좌표: [이전 좌표의 i,j]

    q.append((attk_i, attk_j))
    visited[attk_i][attk_j] = [-1, -1]

    flag = 0
    while q:
        if flag == 1:
            break

        ci, cj = q.pop(0)
        for d in range(4):
            ni, nj = (ci+di[d])%N, (cj+dj[d])%M
            if arr[ni][nj][0] != 0 and len(visited[ni][nj]) == 0:
                q.append((ni, nj))
                visited[ni][nj] = [ci, cj]

                if (ni, nj) == (tgt_i, tgt_j):
                    flag = 1
                    break

    affected = []
    if flag == 1:  # 레이저 공격
        i, j = tgt_i, tgt_j
        while True:
            if i == -1 and j == -1:
                break
            affected.append((i, j))
            i, j = visited[i][j]

        for i, j in affected:
            if (i, j) == (attk_i, attk_j):
                continue
            elif (i, j) == (tgt_i, tgt_j):
                arr[i][j][0] = max(0, arr[i][j][0]-arr[attk_i][attk_j][0])
            else:
                arr[i][j][0] = max(0, arr[i][j][0]-arr[attk_i][attk_j][0]//2)

    else:  # 포탄 공격
        affected.append((attk_i, attk_j))
        arr[tgt_i][tgt_j][0] = max(0, arr[tgt_i][tgt_j][0]-arr[attk_i][attk_j][0])
        affected.append((tgt_i, tgt_j))
        for di8, dj8 in [(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1)]:
            ni, nj = (tgt_i+di8)%N, (tgt_j+dj8)%M
            if (ni, nj) == (attk_i, attk_j):
                continue
            elif arr[ni][nj][0] == 0:
                continue
            else:
                arr[ni][nj][0] = max(0, arr[ni][nj][0]-arr[attk_i][attk_j][0]//2)
                affected.append((ni, nj))

    # [종료조건] 부서지지 않은 포탑이 1개가 되면 break
    cnt_alive = 0
    for i in range(N):
        for j in range(M):
            if arr[i][j][0] > 0:
                cnt_alive += 1
    if cnt_alive == 1:
        break

    # 4. 포탑 정비
    for i in range(N):
        for j in range(M):
            if arr[i][j][0] == 0:
                continue
            if (i, j) not in affected:
                arr[i][j][0] += 1


answer = 0
for i in range(N):
    for j in range(M):
        answer = max(answer, arr[i][j][0])
print(answer)
