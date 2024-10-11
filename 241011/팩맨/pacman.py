import copy

# 0↑, 1↖, 2←, 3↙, 4↓, 5↘, 6→, 7↗
di = [-1, -1, 0, 1, 1, 1, 0, -1]
dj = [0, -1, -1, -1, 0, 1, 1, 1]

m,t = map(int, input().split())
pi,pj = map(int, input().split())
pi,pj = pi-1,pj-1

monster = []
dead = [[0 for _ in range(4)] for _ in range(4)]
for _ in range(m):
    r,c,d = map(int, input().split())
    monster.append([r-1,c-1,d-1])

for _ in range(t): # 10^1
    # 1) 몬스터 복제 시도
    egg = copy.deepcopy(monster)

    # 2) 몬스터 이동
    monster_arr = [[[] for _ in range(4)] for _ in range(4)]
    for idx in range(len(monster)): # 10^7
        ci,cj,cd = monster[idx]
        for dd in range(8): # 10^7
            nd = (cd+dd)%8
            ni,nj = ci+di[nd], cj+dj[nd]
            if 0<=ni<4 and 0<=nj<4 and (ni,nj)!=(pi,pj) and dead[ni][nj]==0:
                monster[idx] = [ni,nj,nd]
                monster_arr[ni][nj].append(idx)
                break
        else:
            monster_arr[ci][cj].append(idx)

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
                tmp_route = {(pi1,pj1), (pi2,pj2), (pi3,pj3)}
                for i,j in tmp_route:
                    eat += len(monster_arr[i][j])
                if max_eat < eat:
                    max_eat = eat
                    route = [(pi1,pj1), (pi2,pj2), (pi3,pj3)]
    pi,pj = route[-1]

    rmv_list = []
    for i,j in route:
        if len(monster_arr[i][j]) > 0:
            dead[i][j] = 3
        for idx in monster_arr[i][j]:
            rmv_list.append(monster[idx])
    for item in rmv_list:
        monster.remove(item)

    # 4) 몬스터 시체 소멸
    for i in range(4):
        for j in range(4):
            if dead[i][j] > 0:
                dead[i][j] -= 1

    # 5) 몬스터 복제 완성
    monster = monster + egg

print(len(monster))