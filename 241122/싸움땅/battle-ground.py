# 상0, 우1, 하2, 좌3
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

n, m, k = map(int, input().split())

gun_arr = [[[] for _ in range(n)] for _ in range(n)]
tmp = [list(map(int, input().split())) for _ in range(n)]
for i in range(n):
    for j in range(n):
        if tmp[i][j] != 0:
            gun_arr[i][j].append(tmp[i][j])

player_dict = dict()
player_arr = [[0 for _ in range(n)] for _ in range(n)]
for idx in range(1, m+1):
    x, y, d, s = map(int, input().split())
    player_dict[idx] = [(x-1, y-1), d, s, 0, 0]  # [(좌표), 방향, 초기능력치, 총능력치, 포인트]
    player_arr[x-1][y-1] = idx


for _ in range(k):
    for idx, info in player_dict.items():
        # 1-1. 한 칸 이동
        player_arr[info[0][0]][info[0][1]] = 0

        ni, nj = info[0][0]+di[info[1]], info[0][1]+dj[info[1]]
        if 0<=ni<n and 0<=nj<n:
            info[0] = (ni,nj)

        else:
            info[1] = (info[1]+2)%4
            ni, nj = info[0][0]+di[info[1]], info[0][1]+dj[info[1]]
            info[0] = (ni,nj)

        if player_arr[ni][nj] == 0:
            # 2-1. 이동한 좌표에 다른 플레이어가 없는 경우
            player_arr[ni][nj] = idx

            if len(gun_arr[ni][nj]) != 0:  # 총 있는 경우
                max_gun = max(gun_arr[ni][nj])
                if max_gun > info[3]:
                    if info[3] == 0:
                        gun_arr[ni][nj].remove(max_gun)
                        info[3] = max_gun
                    else:
                        gun_arr[ni][nj].remove(max_gun)
                        gun_arr[ni][nj].append(info[3])
                        info[3] = max_gun
        else:
            # 2-2-1. 두 플레이어의 싸움
            idx2 = player_arr[ni][nj]
            info2 = player_dict[idx2]

            if info[2]+info[3] > info2[2]+info2[3]:  # idx win & idx2 lose
                win_idx, win_info, lose_idx, lose_info = idx, info, idx2, info2
            elif info[2]+info[3] < info2[2]+info2[3]:  # idx lose & idx2 win
                win_idx, win_info, lose_idx, lose_info  = idx2, info2, idx, info
            else:
                if info[2] >= info2[2]:  # idx win & idx2 lose
                    win_idx, win_info, lose_idx, lose_info = idx, info, idx2, info2
                else:  # idx lose & idx2 win
                    win_idx, win_info, lose_idx, lose_info  = idx2, info2, idx, info

            point = (win_info[2]+win_info[3]) - (lose_info[2]+lose_info[3])
            player_dict[win_idx][4] += point
            player_arr[ni][nj] = win_idx

            # 2-2-2. 진 플레이어 처리
            if lose_info[3] != 0:
                gun_arr[ni][nj].append(lose_info[3])
                lose_info[3] = 0

            for dd in range(4):
                ld = (lose_info[1]+dd)%4
                lni, lnj = lose_info[0][0]+di[ld], lose_info[0][1]+dj[ld]
                if 0<=lni<n and 0<=lnj<n and player_arr[lni][lnj]==0:
                    lose_info[0] = (lni, lnj)
                    lose_info[1] = ld
                    player_arr[lni][lnj] = lose_idx
                    break

            if len(gun_arr[lni][lnj]) != 0:  # 총 있는 경우
                max_gun = max(gun_arr[lni][lnj])
                gun_arr[lni][lnj].remove(max_gun)
                lose_info[3] = max_gun

            # 2-2-3. 이긴 플레이어 처리
            if len(gun_arr[ni][nj]) != 0:  # 총 있는 경우
                max_gun = max(gun_arr[ni][nj])
                if max_gun > win_info[3]:
                    if win_info[3] == 0:
                        gun_arr[ni][nj].remove(max_gun)
                        win_info[3] = max_gun
                    else:
                        gun_arr[ni][nj].remove(max_gun)
                        gun_arr[ni][nj].append(win_info[3])
                        win_info[3] = max_gun

ans = []
for idx, info in player_dict.items():
    ans.append(str(info[-1]))
str_ans = ' '.join(ans)
print(str_ans)

