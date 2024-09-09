m,t = map(int, input().split())

Pi,Pj = map(int, input().split())
Pi,Pj = Pi-1, Pj-1

monster = dict()
arr = [[[] for _ in range(4)] for _ in range(4)]
dead = []
for idx in range(1,m+1):
    r,c,d = map(int, input().split())
    monster[idx] = [(r-1,c-1), d-1, 0, 1, -1] # (좌표)/ 방향인덱스/ 0몬1알/ 0죽1살/ -1디폴트시체카운팅
    arr[r-1][c-1].append(idx)
monster_cnt = m

# ↑0  ↖1  ←2  ↙3  ↓4  ↘5  →6  ↗7
di = [-1, -1, 0, 1, 1, 1, 0, -1]
dj = [0, -1, -1, -1, 0, 1, 1, 1]


for _ in range(t):
    # 몬스터 복제 시도
    for idx in list(monster.keys()):
        if monster[idx][3] == 1:
            monster_cnt += 1
            monster[monster_cnt] = [monster[idx][0], monster[idx][1], 1, 1, -1]

    # 몬스터 이동
    for idx, info in monster.items():
        if info[2] == 1 or info[3] == 0:
            continue

        ci,cj,d = info[0][0], info[0][1], info[1]
        for val in range(8):
            nd = (d+val) % 8
            ni,nj = ci+di[nd], cj+dj[nd]
            if 0<=ni<4 and 0<=nj<4 and (ni,nj) not in dead and (ni,nj)!=(Pi,Pj):
                info[0] = (ni,nj)
                info[1] = nd
                arr[ci][cj].remove(idx)
                arr[ni][nj].append(idx)
                break

    # 팩맨 이동
    max_eat = -1
    move_lst = []
    for d1 in (0,2,4,6):
        i1,j1 = Pi+di[d1], Pj+dj[d1]
        if not (0<=i1<4 and 0<=j1<4):
            continue
        eat1 = len(arr[i1][j1])

        for d2 in (0,2,4,6):
            i2,j2 = i1+di[d2], j1+dj[d2]
            if not (0<=i2<4 and 0<=j2<4):
                continue
            if (i2,j2) == (i1,j1):
                continue
            eat2 = len(arr[i2][j2])

            for d3 in (0,2,4,6):
                i3,j3 = i2+di[d3], j2+dj[d3]
                if not (0<=i3<4 and 0<=j3<4):
                    continue
                if (i3,j3) in ((i1,j1), (i2,j2)):
                    continue
                eat3 = len(arr[i3][j3])

                if max_eat < (eat1+eat2+eat3):
                    max_eat = eat1+eat2+eat3
                    move_lst = [d1,d2,d3]

    final_i1, final_j1 = Pi+di[move_lst[0]], Pj+dj[move_lst[0]]
    final_i2, final_j2 = final_i1+di[move_lst[1]], final_j1+dj[move_lst[1]]
    final_i3, final_j3 = final_i2+di[move_lst[2]], final_j2+dj[move_lst[2]]
    for i,j in ((final_i1,final_j1), (final_i2,final_j2), (final_i3,final_j3)):
        if len(arr[i][j]) != 0:
            for idx in arr[i][j]:
                monster[idx][3] = 0
                monster[idx][4] = 3
            arr[i][j] = []
    Pi,Pj = final_i3, final_j3

    # 몬스터 시체 소멸
    del_idx = []
    dead = []
    for idx, info in monster.items():
        if info[3] == 0:
            info[4] -= 1

            if info[4] == 0:
                del_idx.append(idx)
            else:
                dead.append(info[0])

    for idx in del_idx:
        del monster[idx]

    # 몬스터 복제 완성
    for idx, info in monster.items():
        if info[2] == 1:
            info[2] = 0
            arr[info[0][0]][info[0][1]].append(idx)

ans = 0
for idx, info in monster.items():
    if info[3] == 1:
        ans += 1
print(ans)