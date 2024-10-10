# 상(0) 우(1) 하(2) 좌(3)
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

n,m,k = map(int, input().split())

tmp = [list(map(int, input().split())) for _ in range(n)]
gun = [[[] for _ in range(n)] for _ in range(n)]
for i in range(n):
    for j in range(n):
        gun[i][j].append(tmp[i][j])

player = dict()
arr = [[[] for _ in range(n)] for _ in range(n)]
for idx in range(1,m+1):
    x,y,d,s = map(int, input().split())
    player[idx] = [[x-1,y-1], d, s, 0, 0] # 좌표(0), 방향(1), 플레이어 능력치(2), 총 공격력(3), 포인트(4)
    arr[x-1][y-1].append(idx)


for _ in range(k):
    for idx, info in player.items():
        # 1-1
        arr[info[0][0]][info[0][1]].remove(idx)
        ni, nj = info[0][0]+di[info[1]], info[0][1]+dj[info[1]]
        if 0 <= ni < n and 0 <= nj < n:
            info[0][0], info[0][1] = ni, nj
        else:
            info[1] = (info[1]+2) % 4
            ni, nj = info[0][0]+di[info[1]], info[0][1]+dj[info[1]]
            info[0][0], info[0][1] = ni, nj
        arr[info[0][0]][info[0][1]].append(idx)

        if len(arr[info[0][0]][info[0][1]]) == 1: # 2-1
            max_gun = max(gun[info[0][0]][info[0][1]])
            if max_gun > info[3]:
                gun[info[0][0]][info[0][1]].remove(max_gun)
                if len(gun[info[0][0]][info[0][1]])==0 or info[3]!=0:
                    gun[info[0][0]][info[0][1]].append(info[3])
                info[3] = max_gun

        elif len(arr[info[0][0]][info[0][1]]) > 1: # 2-2
            ci,cj = info[0][0], info[0][1]

            # 2-2-1
            other_idx = -1
            for candidate in arr[ci][cj]:
                if candidate != idx:
                    other_idx = candidate
            if info[2]+info[3] > player[other_idx][2]+player[other_idx][3]:
                win_idx, lose_idx = idx, other_idx
            elif info[2]+info[3] < player[other_idx][2]+player[other_idx][3]:
                win_idx, lose_idx = other_idx, idx
            else:
                if info[2] > player[other_idx][2]:
                    win_idx, lose_idx = idx, other_idx
                else:
                    win_idx, lose_idx = other_idx, idx
            player[win_idx][4] += ((player[win_idx][2]+player[win_idx][3]) - (player[lose_idx][2]+player[lose_idx][3]))

            # 2-2-2 (lose 처리)
            if len(gun[ci][cj])==0 or player[lose_idx][3]!=0:
                gun[ci][cj].append(player[lose_idx][3])
            player[lose_idx][3] = 0

            cli, clj, cld = player[lose_idx][0][0], player[lose_idx][0][1], player[lose_idx][1]
            for dd in range(4):
                nli,nlj = cli+di[(cld+dd)%4], clj+dj[(cld+dd)%4]
                if 0 <= nli < n and 0 <= nlj < n and len(arr[nli][nlj]) == 0:
                    player[lose_idx][0][0], player[lose_idx][0][1] = nli, nlj
                    player[lose_idx][1] = (cld+dd) % 4
                    arr[ci][cj].remove(lose_idx)
                    arr[nli][nlj].append(lose_idx)

                    max_gun = max(gun[nli][nlj])
                    if max_gun > player[lose_idx][3]:
                        gun[nli][nlj].remove(max_gun)
                        if len(gun[nli][nlj])==0 or player[lose_idx][3] != 0:
                            gun[nli][nlj].append(player[lose_idx][3])
                        player[lose_idx][3] = max_gun
                    break

            # 2-2-3 (win 처리)
            max_gun = max(gun[ci][cj])
            if max_gun > player[win_idx][3]:
                gun[ci][cj].remove(max_gun)
                if len(gun[ci][cj])==0 or player[win_idx][3] != 0:
                    gun[ci][cj].append(player[win_idx][3])
                player[win_idx][3] = max_gun

    sorted_player = dict(sorted(player.items()))
    player = sorted_player

ans = []
for idx, info in player.items():
    ans.append(str(info[4]))
print(' '.join(ans))