n,m = map(int, input().split())
INF = n*n*n

temp = [list(map(int, input().split())) for _ in range(n)]
base = []
for i in range(n):
    for j in range(n):
        if temp[i][j] == 1:
            base.append((i,j))
arr = [[0 for _ in range(n)] for _ in range(n)]

people = dict()
for idx in range(1,m+1):
    x,y = map(int, input().split())
    people[idx] = [(-1,-1), (x-1,y-1)]


def BFS(si,sj,ti,tj):
    q = []
    visited = [[INF for _ in range(n)] for _ in range(n)]

    q.append((si,sj))
    visited[si][sj] = 0

    while q:
        ci,cj = q.pop(0)
        for di,dj in ((-1,0),(0,-1),(0,1),(1,0)):
            ni,nj = ci+di,cj+dj
            if 0<=ni<n and 0<=nj<n and visited[ni][nj]==INF and arr[ni][nj]==0:
                q.append((ni,nj))
                visited[ni][nj] = visited[ci][cj] + 1
                if (ni,nj) == (ti,tj):
                    return visited[ti][tj]

    return visited[ti][tj]


time = 1
while True:
    blocked = []

    # 격자 사람 모두 이동
    arrived = 0
    for idx, info in people.items():
        if info[0] == (-1,-1):
            continue
        if info[0] == info[1]:
            arrived += 1
            continue

        min_d = BFS(info[0][0],info[0][1],info[1][0],info[1][1])
        final_i,final_j = info[0][0],info[0][1]
        for di,dj in ((-1,0),(0,-1),(0,1),(1,0)):
            ni,nj = info[0][0]+di,info[0][1]+dj
            if 0<=ni<n and 0<=nj<n:
                dist = BFS(ni,nj,info[1][0],info[1][1])
                if min_d > dist:
                    min_d = dist
                    final_i,final_j = ni,nj

        info[0] = (final_i,final_j)

        if info[0] == info[1]:
            arrived += 1
            blocked.append(info[1])

    # 종료 조건
    if arrived == m:
        break

    # 베이스캠프 처리
    if time <= m:
        target = people[time][1]

        min_d, min_i, min_j = INF+1, n, n
        for bi,bj in base:
            dist = BFS(bi,bj,target[0],target[1])
            if min_d > dist:
                min_d, min_i, min_j = dist, bi, bj
            elif min_d == dist:
                if min_i > bi:
                    min_d, min_i, min_j = dist, bi, bj
                elif min_i == bi:
                    if min_j > bj:
                        min_d, min_i, min_j = dist, bi, bj

        people[time][0] = (min_i,min_j)
        base.remove((min_i,min_j))
        blocked.append((min_i,min_j))

    # blocked 처리
    for i,j in blocked:
        arr[i][j] = 1

    time += 1

print(time)