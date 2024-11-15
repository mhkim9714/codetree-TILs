N,M = map(int, input().split())
medusa_i,medusa_j,park_i,park_j = map(int, input().split())

knight = dict()
knight_arr = [[[] for _ in range(N)] for _ in range(N)]
knight_location = list(map(int, input().split()))
for idx in range(1,M+1):
    knight[idx] = [(knight_location[2*idx-2],knight_location[2*idx-1]), 0]  # [(위치), 돌여부] 0:자유(default), 1:돌
    knight_arr[knight_location[2*idx-2]][knight_location[2*idx-1]].append(idx)

arr = [list(map(int, input().split())) for _ in range(N)]


def knight_view(si,sj,view):
    sight = []
    visited = [[0 for _ in range(N)] for _ in range(N)]

    q = [(si,sj)]
    visited[si][sj] = 1

    while q:
        ci,cj = q.pop(0)
        for di,dj in view:
            ni,nj = ci+di, cj+dj
            if 0<=ni<N and 0<=nj<N and visited[ni][nj]==0:
                q.append((ni,nj))
                visited[ni][nj] = 1
                sight.append((ni,nj))

    return sight


def medusa_view(medusa_d,view):
    sight = []
    unseen = []
    visited = [[0 for _ in range(N)] for _ in range(N)]
    cnt_in_sight = 0

    q = [(medusa_i, medusa_j)]
    visited[medusa_i][medusa_j] = 1
    while q:
        ci,cj = q.pop(0)
        for di,dj in view:
            ni,nj = ci+di, cj+dj
            if 0<=ni<N and 0<=nj<N and visited[ni][nj]==0 and (ni,nj) not in unseen:
                q.append((ni,nj))
                visited[ni][nj] = 1
                sight.append((ni,nj))
                if len(knight_arr[ni][nj]) > 0:
                    cnt_in_sight += len(knight_arr[ni][nj])
                    if medusa_d in [0,1]:  # 상,하 -> j처리
                        if nj < medusa_j:
                            new_view = view[:2]
                        elif nj == medusa_j:
                            new_view = [view[1]]
                        else:
                            new_view = view[1:]
                    else:  # 좌,우 -> i처리
                        if ni < medusa_i:
                            new_view = view[:2]
                        elif ni == medusa_i:
                            new_view = [view[1]]
                        else:
                            new_view = view[1:]
                    temp_unseen = knight_view(ni,nj,new_view)
                    unseen.extend(temp_unseen)
                    unseen = list(set(unseen))

    return sight, cnt_in_sight


def distance(i1,j1,i2,j2):
    return abs(i2-i1) + abs(j2-j1)


# [0] 메두사의 집부터 공원까지의 최단 경로 좌표 리스트 구하기
q = []
visited = [[[] for _ in range(N)] for _ in range(N)]  # 시작점 0, 미방문 [], 장애물 -1, 일반 [이전좌표]
for i in range(N):
    for j in range(N):
        if arr[i][j] == 1:
            visited[i][j] = -1

q.append((medusa_i, medusa_j))
visited[medusa_i][medusa_j] = 0

while q:
    ci,cj = q.pop(0)
    for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):  # 상하좌우 우선순위
        ni,nj = ci+di, cj+dj
        if 0<=ni<N and 0<=nj<N and visited[ni][nj]==[]:
            q.append((ni,nj))
            visited[ni][nj] = [(ci,cj)]

            if (ni,nj) == (park_i, park_j):
                q = []
                break

if visited[park_i][park_j] == []:
    print(-1)
    exit()
else:
    medusa_path = []
    i,j = park_i, park_j
    while True:
        if visited[i][j] == 0:
            break
        else:
            medusa_path.append((i,j))
            i,j = visited[i][j][0]
    medusa_path.reverse()


while True:
    sum_knight_move, cnt_rock, cnt_attacker = 0, 0, 0

    # [1] 메두사의 이동
    ni,nj = medusa_path.pop(0)

    if len(knight_arr[ni][nj]) > 0:
        for idx in knight_arr[ni][nj]:
            del knight[idx]
        knight_arr[ni][nj] = []

    if (ni,nj) == (park_i,park_j):
        print(0)
        break
    else:
        medusa_i, medusa_j = ni,nj

    if len(knight) == 0:
        print("0 0 0")
        continue

    # [2] 메두사의 시선
    sight = []
    cnt_in_sight = 0

    for d in range(4):  # 상하좌우 우선순위
        if d == 0:  # 상
            v = [(-1,-1),(-1,0),(-1,1)]
        elif d == 1:  # 하
            v = [(1,-1),(1,0),(1,1)]
        elif d == 2:  # 좌
            v = [(-1,-1),(0,-1),(1,-1)]
        else:  # 우
            v = [(-1,1),(0,1),(1,1)]
        cur_sight, cur_cnt_in_sight = medusa_view(d,v)
        if cnt_in_sight < cur_cnt_in_sight:
            sight, cnt_in_sight = cur_sight, cur_cnt_in_sight

    for idx, info in knight.items():
        if info[0] in sight:
            info[1] = 1
    cnt_rock = cnt_in_sight

    # [3] 전사들의 이동
    del_idx = []
    for idx, info in knight.items():
        if info[1] == 1:
            continue

        # 이동 연속 2번
        for direction in [[(-1,0),(1,0),(0,-1),(0,1)], [(0,-1),(0,1),(-1,0),(1,0)]]:
            cur_dist = distance(medusa_i,medusa_j,info[0][0],info[0][1])
            mv_i,mv_j = info[0][0], info[0][1]
            for di,dj in direction:
                ni,nj = info[0][0]+di, info[0][1]+dj
                if 0<=ni<N and 0<=nj<N and (ni,nj) not in sight:
                    next_dist = distance(medusa_i,medusa_j,ni,nj)
                    if next_dist < cur_dist:
                        cur_dist = next_dist
                        mv_i, mv_j = ni,nj

            if (mv_i,mv_j) == info[0]:  # 안움직인 경우
                break
            else:  # 움직인 경우
                sum_knight_move += 1
                if (mv_i,mv_j) == (medusa_i,medusa_j):  # 메두사 공격하는 경우
                    cnt_attacker += 1
                    del_idx.append(idx)
                    break
                else:  # 이동만 하는 경우
                    info[0] = (mv_i,mv_j)

    for idx in del_idx:
        del knight[idx]
    knight_arr = [[[] for _ in range(N)] for _ in range(N)]

    # [5] 전사들 돌 풀림
    for idx, info in knight.items():
        knight_arr[info[0][0]][info[0][1]].append(idx)
        info[1] = 0

    print(f'{sum_knight_move} {cnt_rock} {cnt_attacker}')

















