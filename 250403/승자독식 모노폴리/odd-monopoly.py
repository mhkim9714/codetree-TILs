n, m, k = map(int, input().split())
arr_init = [list(map(int, input().split())) for _ in range(n)]
d_init = list(map(int, input().split()))

real_estate = [[[] for _ in range(n)] for _ in range(n)]  # [소유 플레이어 인덱스, 계약 남은 턴수]
arr = [[[] for _ in range(n)] for _ in range(n)]  # [해당 칸에 있는 플레이어 인덱스]
player = dict()  # [(좌표), 방향]

for i in range(n):
    for j in range(n):
        if arr_init[i][j] > 0:
            idx = arr_init[i][j]
            real_estate[i][j] = [idx, k]
            arr[i][j].append(idx)
            player[idx] = [(i, j), d_init[idx-1]-1]

d_priority = [[] for _ in range(m+1)]
for idx in range(1, m+1):
    up_priority = list(map(int, input().split()))
    up_priority = [x-1 for x in up_priority]
    down_priority = list(map(int, input().split()))
    down_priority = [x-1 for x in down_priority]
    left_priority = list(map(int, input().split()))
    left_priority = [x-1 for x in left_priority]
    right_priority = list(map(int, input().split()))
    right_priority = [x-1 for x in right_priority]
    d_priority[idx] = [up_priority, down_priority, left_priority, right_priority]

# 상0 하1 좌2 우3
di = [-1, 1, 0, 0]
dj = [0, 0, -1, 1]


turn = 1
while True:
    # [종료 조건] 턴수 == 1000 이면, print -1하고 break
    if turn == 1000:
        print(-1)
        break

    # 모든 플레이어 마다, (동시에 이동이라는 거 잊지 말기)
    new_arr = [[[] for _ in range(n)] for _ in range(n)]
    for idx, info in player.items():
        # <이동 1트>
        for d in d_priority[idx][info[1]]:
            ni, nj = info[0][0]+di[d], info[0][1]+dj[d]
            if 0<=ni<n and 0<=nj<n and real_estate[ni][nj]==[]:
                new_arr[ni][nj].append(idx)
                info[0] = (ni, nj)
                info[1] = d
                break
        else:
            # 이동 못했으면, <이동 2트>
            for d in d_priority[idx][info[1]]:
                ni, nj = info[0][0]+di[d], info[0][1]+dj[d]
                if 0<=ni<n and 0<=nj<n and real_estate[ni][nj][0]==idx:
                    new_arr[ni][nj].append(idx)
                    info[0] = (ni, nj)
                    info[1] = d
                    break
    arr = new_arr

    # 플레이어 제거 & 부동산 계약
    for i in range(n):
        for j in range(n):
            if len(arr[i][j]) == 0:
                continue

            elif len(arr[i][j]) == 1:  # 부동산 독점 계약
                real_estate[i][j] = [arr[i][j][0], k+1]

            else:  # 플레이어 삭제 -> 부동산 독점 계약
                min_idx = min(arr[i][j])
                for idx in arr[i][j]:
                    if idx != min_idx:
                        del player[idx]
                arr[i][j] = [min_idx]

                real_estate[i][j] = [min_idx, k+1]

    # [종료 조건] 남은 플레이어가 1명이면, 현재까지 턴수 print하고 break
    if len(player) == 1:
        print(turn)
        break

    # 전체적으로 부동산 계약 남은 턴수 -= 1
    for i in range(n):
        for j in range(n):
            if len(real_estate[i][j]) > 0:
                remain = max(0, real_estate[i][j][1]-1)
                if remain > 0:
                    real_estate[i][j][1] = remain
                else:
                    real_estate[i][j] = []

    # 턴수 += 1
    turn += 1

