m,t = map(int, input().split())

Pi,Pj = map(int, input().split())
Pi,Pj = Pi-1, Pj-1

monster = [[[] for _ in range(4)] for _ in range(4)] # 방향인덱스
egg = [[[] for _ in range(4)] for _ in range(4)] # 방향인덱스
dead = [[0 for _ in range(4)] for _ in range(4)] # 시체카운트
dead_loc = []

for _ in range(m):
    r,c,d = map(int, input().split())
    monster[r-1][c-1].append(d-1)

# ↑0  ↖1  ←2  ↙3  ↓4  ↘5  →6  ↗7
di = [-1, -1, 0, 1, 1, 1, 0, -1]
dj = [0, -1, -1, -1, 0, 1, 1, 1]


for _ in range(t): # 10e1
    # 몬스터 복제 시도
    for i in range(4): # 10e2
        for j in range(4):
            if len(monster[i][j]) > 0:
                egg[i][j] = monster[i][j]

    # 몬스터 이동
    new_monster = [[[] for _ in range(4)] for _ in range(4)]
    for ci in range(4):
        for cj in range(4):
            if len(monster[ci][cj]) > 0:
                for d in monster[ci][cj]:
                    for val in range(8):
                        nd = (d+val) % 8
                        ni,nj = ci+di[nd], cj+dj[nd]
                        if 0<=ni<4 and 0<=nj<4 and (ni,nj) not in dead_loc and (ni,nj) != (Pi,Pj):
                            new_monster[ni][nj].append(nd)
                            break
                    else:
                        new_monster[ci][cj].append(d)
    monster = new_monster

    # 팩맨 이동
    max_eat = -1
    move_lst = []
    for d1 in (0,2,4,6):
        i1,j1 = Pi+di[d1], Pj+dj[d1]
        if not (0<=i1<4 and 0<=j1<4):
            continue

        for d2 in (0,2,4,6):
            i2,j2 = i1+di[d2], j1+dj[d2]
            if not (0<=i2<4 and 0<=j2<4):
                continue

            for d3 in (0,2,4,6):
                i3,j3 = i2+di[d3], j2+dj[d3]
                if not (0<=i3<4 and 0<=j3<4):
                    continue

                eat_lst = list(set([(i1,j1),(i2,j2),(i3,j3)]))
                cur_eat = 0
                for i,j in eat_lst:
                    cur_eat += len(monster[i][j])
                if max_eat < cur_eat:
                    max_eat = cur_eat
                    move_lst = [d1,d2,d3]

    final_i1, final_j1 = Pi+di[move_lst[0]], Pj+dj[move_lst[0]]
    final_i2, final_j2 = final_i1+di[move_lst[1]], final_j1+dj[move_lst[1]]
    final_i3, final_j3 = final_i2+di[move_lst[2]], final_j2+dj[move_lst[2]]

    for i,j in ((final_i1,final_j1), (final_i2,final_j2), (final_i3,final_j3)):
        if len(monster[i][j]) != 0:
            dead[i][j] = max(dead[i][j],3)
            monster[i][j] = []
    Pi,Pj = final_i3, final_j3

    # 몬스터 시체 소멸
    dead_loc = []
    for i in range(4):
        for j in range(4):
            dead[i][j] = max(dead[i][j]-1,0)
            if dead[i][j] > 0:
                dead_loc.append((i,j))

    # 몬스터 복제 완성
    for i in range(4):
        for j in range(4):
            if len(egg[i][j]) > 0:
                monster[i][j].extend(egg[i][j])
    egg = [[[] for _ in range(4)] for _ in range(4)]

ans = 0
for i in range(4):
    for j in range(4):
        if len(monster[i][j]) > 0:
            ans += len(monster[i][j])
print(ans)