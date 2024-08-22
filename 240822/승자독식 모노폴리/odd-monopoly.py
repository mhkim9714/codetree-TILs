n,m,k = map(int, input().split())

arr = [[[] for _ in range(n)] for _ in range(n)]
temp = [list(map(int, input().split())) for _ in range(n)]
temp_d = list(map(int, input().split()))

player = dict()
for i in range(n):
    for j in range(n):
        if temp[i][j] > 0:
            player[temp[i][j]] = [(i,j), temp_d[temp[i][j]-1]-1]
            arr[i][j] = [temp[i][j], k]

priority = dict()
for idx in range(1,m+1):
    up_ = list(map(int, input().split()))
    up = [x-1 for x in up_]
    down_ = list(map(int, input().split()))
    down = [x-1 for x in down_]
    left_ = list(map(int, input().split()))
    left = [x-1 for x in left_]
    right_ = list(map(int, input().split()))
    right = [x-1 for x in right_]

    priority[idx] = [up, down, left, right]

# 상0 하1 좌2 우3
di = [-1, 1, 0, 0]
dj = [0, 0, -1, 1]


for turn in range(1,1000):
    # 각 플레이어 이동 -> player 업뎃
    for idx, info in player.items():
        d_empty, d_mine = -1, -1
        for d in priority[idx][info[1]][::-1]:
            ni,nj = info[0][0]+di[d], info[0][1]+dj[d]
            if 0<=ni<n and 0<=nj<n:
                if len(arr[ni][nj]) == 0:
                    d_empty = d
                elif arr[ni][nj][0] == idx:
                    d_mine = d

        if d_empty != -1:
            nd = d_empty
        else:
            nd = d_mine

        ni,nj = info[0][0]+di[nd], info[0][1]+dj[nd]
        info[0] = (ni,nj)
        info[1] = nd

    # 각 플레이어가 이동한 칸에서 독점계약 진행 -> arr 업뎃
    del_player_idx = []
    for idx, info in player.items():
        if len(arr[info[0][0]][info[0][1]]) == 0:
            arr[info[0][0]][info[0][1]] = [idx, k+1]
        else:
            if idx != arr[info[0][0]][info[0][1]][0]:
                if idx < arr[info[0][0]][info[0][1]][0]:
                    small, big = idx, arr[info[0][0]][info[0][1]][0]
                else:
                    small, big = arr[info[0][0]][info[0][1]][0], idx
                arr[info[0][0]][info[0][1]] = [small, k+1]
                del_player_idx.append(big)
            else:
                arr[info[0][0]][info[0][1]] = [idx, k+1]

    for idx in del_player_idx:
        del player[idx]

    if len(player) == 1:
        print(turn)
        break

    # 독점 계약 기한 -1
    for i in range(n):
        for j in range(n):
            if len(arr[i][j]) > 0:
                if arr[i][j][1] > 1:
                    arr[i][j][1] -= 1
                elif arr[i][j][1] == 1:
                    arr[i][j] = []

else:
    print(-1)