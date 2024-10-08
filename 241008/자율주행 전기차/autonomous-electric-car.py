n,m,c = map(int, input().split())
INF = n**3
arr = [list(map(int, input().split())) for _ in range(n)]

car_i,car_j = map(int, input().split())
car_i,car_j = car_i-1, car_j-1

people = dict()
for idx in range(1,m+1):
    x_s,y_s,x_e,y_e = map(int, input().split())
    people[idx] = [(x_s-1, y_s-1), (x_e-1, y_e-1)]


def BFS(si,sj):
    q = []
    visited = [[INF for _ in range(n)] for _ in range(n)]

    q.append((si,sj))
    visited[si][sj] = 0

    while q:
        ci,cj = q.pop(0)
        for di,dj in [(-1,0),(0,1),(1,0),(0,-1)]:
            ni,nj = ci+di, cj+dj
            if 0<=ni<n and 0<=nj<n and visited[ni][nj]==INF and arr[ni][nj]!=1:
                q.append((ni,nj))
                visited[ni][nj] = visited[ci][cj]+1

    return visited


while len(people) > 0:
    # 태울 승객 구하기 (거리작 -> i작 -> j작)
    distance = BFS(car_i,car_j)

    min_dist, tgt_i, tgt_j, tgt_idx = INF+1, n, n, -1
    for idx,info in people.items():
        if min_dist > distance[info[0][0]][info[0][1]]:
            min_dist, tgt_i, tgt_j, tgt_idx = distance[info[0][0]][info[0][1]], info[0][0], info[0][1], idx
        elif min_dist == distance[info[0][0]][info[0][1]]:
            if tgt_i > info[0][0]:
                min_dist, tgt_i, tgt_j, tgt_idx = distance[info[0][0]][info[0][1]], info[0][0], info[0][1], idx
            elif tgt_i == info[0][0]:
                if tgt_j > info[0][1]:
                    min_dist, tgt_i, tgt_j, tgt_idx = distance[info[0][0]][info[0][1]], info[0][0], info[0][1], idx

    if min_dist == INF:
        c = 0
        break

    if c > min_dist:
        car_i, car_j = tgt_i, tgt_j
        c -= min_dist

    else:
        c = 0
        break

    # 목적지로 이동하기
    dest_i, dest_j = people[tgt_idx][1][0], people[tgt_idx][1][1]
    distance = BFS(car_i,car_j)
    dest_dist = distance[dest_i][dest_j]

    if dest_dist == INF:
        c = 0
        break

    if c >= dest_dist:
        car_i, car_j = dest_i, dest_j
        c += dest_dist
    else:
        c = 0
        break

    # tgt 승객 처리 완료
    del people[tgt_idx]

if c == 0:
    print(-1)
else:
    print(c)