n,m,k = map(int, input().split())

temp = [list(map(int, input().split())) for _ in range(n)]
arr = [[[] for _ in range(n)] for _ in range(n)]
for i in range(n):
    for j in range(n):
        arr[i][j].append(temp[i][j])

player = dict()
p_loc = [[0 for _ in range(n)] for _ in range(n)]
for idx in range(1,m+1):
    x,y,d,s = map(int, input().split())
    player[idx] = [(x-1,y-1),d,s,0,0]
    p_loc[x-1][y-1] = idx

# 상0 우1 하2 좌3
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]


for _ in range(k):
    for idx in list(player.keys()):
        # 1-1
        ci, cj, d = player[idx][0][0], player[idx][0][1], player[idx][1]
        ni, nj = ci+di[d], cj+dj[d]
        if not (0<=ni<n and 0<=nj<n):
            d = (d+2)%4
            ni, nj = ci+di[d], cj+dj[d]

        p_loc[ci][cj] = 0
        player[idx][0] = (ni,nj)
        player[idx][1] = d

        if p_loc[ni][nj] == 0:
            # 2-1
            arr[ni][nj].append(player[idx][3])
            max_gun = max(arr[ni][nj])
            player[idx][3] = max_gun
            arr[ni][nj].remove(max_gun)

            p_loc[ni][nj] = idx

        else:
            # 2-2-1
            if player[idx][2]+player[idx][3] > player[p_loc[ni][nj]][2]+player[p_loc[ni][nj]][3]:
                win_idx, lose_idx = idx, p_loc[ni][nj]
            elif player[idx][2]+player[idx][3] < player[p_loc[ni][nj]][2]+player[p_loc[ni][nj]][3]:
                win_idx, lose_idx = p_loc[ni][nj], idx
            else:
                if player[idx][2] > player[p_loc[ni][nj]][2]:
                    win_idx, lose_idx = idx, p_loc[ni][nj]
                else:
                    win_idx, lose_idx = p_loc[ni][nj], idx

            player[win_idx][4] += (player[win_idx][2]+player[win_idx][3]-player[lose_idx][2]-player[lose_idx][3])

            # 2-2-2
            if player[lose_idx][3] > 0:
                arr[ni][nj].append(player[lose_idx][3])
                player[lose_idx][3] = 0

            lose_ci, lose_cj, lose_d = player[lose_idx][0][0], player[lose_idx][0][1], player[lose_idx][1]
            for dd in range(4):
                lose_nd = (lose_d+dd)%4
                lose_ni, lose_nj = lose_ci+di[lose_nd], lose_cj+dj[lose_nd]
                if 0<=lose_ni<n and 0<=lose_nj<n and p_loc[lose_ni][lose_nj]==0:
                    player[lose_idx][0] = (lose_ni, lose_nj)
                    player[lose_idx][1] = lose_nd
                    p_loc[lose_ni][lose_nj] = lose_idx

                    arr[lose_ni][lose_nj].append(player[lose_idx][3])
                    max_gun = max(arr[lose_ni][lose_nj])
                    player[lose_idx][3] = max_gun
                    arr[lose_ni][lose_nj].remove(max_gun)
                    break

            # 2-2-3
            p_loc[ni][nj] = win_idx

            arr[ni][nj].append(player[win_idx][3])
            max_gun = max(arr[ni][nj])
            player[win_idx][3] = max_gun
            arr[ni][nj].remove(max_gun)


ans = []
for idx, info in player.items():
    ans.append(str(info[-1]))
ans_str = ' '.join(ans)
print(ans_str)