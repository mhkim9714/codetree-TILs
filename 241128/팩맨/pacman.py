import copy

# ↑0, ↖1, ←2, ↙3, ↓4, ↘5, →6, ↗7
di = [-1, -1, 0, 1, 1, 1, 0, -1]
dj = [0, -1, -1, -1, 0, 1, 1, 1]

m, t = map(int, input().split())
pi, pj = map(int, input().split())
pi, pj = pi-1, pj-1

monster = [[[0 for _ in range(8)] for _ in range(4)] for _ in range(4)]
for _ in range(m):
    r, c, d = map(int, input().split())
    monster[r-1][c-1][d-1] += 1

dead = [[0 for _ in range(4)] for _ in range(4)]


for _ in range(t):  # 10^1
    # 1. 몬스터 복제 시도
    egg = copy.deepcopy(monster)

    # 2. 몬스터 이동
    new_monster = [[[0 for _ in range(8)] for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for d in range(8):
                if monster[i][j][d] == 0:
                    continue
                for dd in range(8):
                    nd = (d+dd) % 8
                    ni, nj = i+di[nd], j+dj[nd]
                    if 0<=ni<4 and 0<=nj<4 and (ni,nj)!=(pi,pj) and dead[ni][nj]==0:
                        new_monster[ni][nj][nd] = monster[i][j][d]
                        break
    monster = new_monster

    # 3. 팩맨 이동 (상좌하우 우선순위)
    max_eat, npi, npj = -1, -1, -1
    path = []

    for d1 in [0,2,4,6]:
        npi1, npj1 = pi+di[d1], pj+dj[d1]
        if 0<=npi1<4 and 0<=npj1<4:
            for d2 in [0,2,4,6]:
                npi2, npj2 = npi1+di[d2], npj1+dj[d2]
                if 0<=npi2<4 and 0<=npj2<4:
                    for d3 in [0,2,4,6]:
                        npi3, npj3 = npi2+di[d3], npj2+dj[d3]
                        if 0<=npi3<4 and 0<=npj3<4:
                            cur_path = list({(npi1, npj1), (npi2, npj2), (npi3, npj3)})
                            cur_eat = 0
                            for i,j in cur_path:
                                cur_eat += sum(monster[i][j])
                            if max_eat < cur_eat:
                                max_eat, npi, npj = cur_eat, npi3, npj3
                                path = cur_path

    pi, pj = npi, npj
    for i,j in path:
        if sum(monster[i][j]) > 0:
            monster[i][j] = [0 for _ in range(8)]
            dead[i][j] = 3

    # 4. 몬스터 시체 소멸
    for i in range(4):
        for j in range(4):
            if dead[i][j] > 0:
                dead[i][j] -= 1

    # 5. 몬스터 복제 완성
    for i in range(4):
        for j in range(4):
            for d in range(8):
                monster[i][j][d] += egg[i][j][d]


ans = 0
for i in range(4):
    for j in range(4):
        ans += sum(monster[i][j])
print(ans)








