import copy

# 0↑, 1↖, 2←, 3↙, 4↓, 5↘, 6→, 7↗
di = [-1, -1, 0, 1, 1, 1, 0, -1]
dj = [0, -1, -1, -1, 0, 1, 1, 1]

m,t = map(int, input().split())
pi,pj = map(int, input().split())
pi,pj = pi-1,pj-1

monster = [[[0 for _ in range(8)] for _ in range(4)] for _ in range(4)] # [각 방향별 갯수] len=8
dead = [[0 for _ in range(4)] for _ in range(4)]
for _ in range(m):
    r,c,d = map(int, input().split())
    monster[r-1][c-1][d-1] += 1


for _ in range(t): # 10^1
    # 1) 몬스터 복제 시도
    egg = copy.deepcopy(monster)

    # 2) 몬스터 이동
    new_monster = [[[0 for _ in range(8)] for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for d in range(8):
                cnt = monster[i][j][d]
                if cnt == 0:
                    continue
                for dd in range(8): # 10^4
                    nd = (d+dd) % 8
                    ni,nj = i+di[nd], j+dj[nd]
                    if 0<=ni<4 and 0<=nj<4 and (ni,nj)!=(pi,pj) and dead[ni][nj]==0:
                        new_monster[ni][nj][nd] += cnt
                        break
                else:
                    new_monster[i][j][d] += cnt
    monster = new_monster

    # 3) 팩맨 이동
    max_eat = -1
    route = []
    for d1 in [0,2,4,6]:
        pi1,pj1 = pi+di[d1],pj+dj[d1]
        if not (0<=pi1<4 and 0<=pj1<4):
            continue

        for d2 in [0,2,4,6]:
            pi2,pj2 = pi1+di[d2],pj1+dj[d2]
            if not (0<=pi2<4 and 0<=pj2<4):
                continue

            for d3 in [0,2,4,6]:
                pi3,pj3 = pi2+di[d3],pj2+dj[d3]
                if not (0<=pi3<4 and 0<=pj3<4):
                    continue

                eat = 0
                for i,j in {(pi1,pj1), (pi2,pj2), (pi3,pj3)}:
                    eat += sum(monster[i][j])
                if max_eat < eat:
                    max_eat = eat
                    route = [(pi1,pj1), (pi2,pj2), (pi3,pj3)]
    pi,pj = route[-1]

    for i,j in set(route):
        if sum(monster[i][j]) > 0:
            dead[i][j] = 3
            monster[i][j] = [0,0,0,0,0,0,0,0]

    # 4) 몬스터 시체 소멸
    for i in range(4):
        for j in range(4):
            if dead[i][j] > 0:
                dead[i][j] -= 1

    # 5) 몬스터 복제 완성
    for i in range(4):
        for j in range(4):
            for d in range(8):
                monster[i][j][d] += egg[i][j][d]

ans = 0
for i in range(4):
    for j in range(4):
        for d in range(8):
            ans += monster[i][j][d]
print(ans)