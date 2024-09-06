n,m = map(int, input().split())

tmp = [list(map(int, input().split())) for _ in range(n)]
base = []
for i in range(n):
    for j in range(n):
        if tmp[i][j] == 1:
            base.append((i,j))

player = dict()
for idx in range(1,m+1):
    x,y = map(int, input().split())
    player[idx] = [(-1,-1),(x-1,y-1)]

blocked = []


def BFS(si,sj,ei,ej):
    q = []
    visited = [[4*(n**2) for _ in range(n)] for _ in range(n)]
    for bli,blj in blocked:
        visited[bli][blj] = -1

    q.append((si,sj))
    visited[si][sj] = 0

    while q:
        ci,cj = q.pop(0)
        for di,dj in ((-1,0),(0,1),(1,0),(0,-1)):
            ni,nj = ci+di, cj+dj
            if 0<=ni<n and 0<=nj<n and visited[ni][nj]==4*(n**2):
                q.append((ni,nj))
                visited[ni][nj] = visited[ci][cj]+1
                if (ni,nj) == (ei,ej):
                    return visited[ei][ej]

    return visited[ei][ej]


time = 1
while True:
    # 격자내 사람들 이동
    blocked_candidate = []
    del_idx = []
    for idx, info in player.items():
        if info[0] == (-1,-1):
            continue

        min_dist,npi,npj = 3*(n**2),-1,-1
        for di,dj in ((-1,0),(0,-1),(0,1),(1,0)):
            ni,nj = info[0][0]+di, info[0][1]+dj
            if 0<=ni<n and 0<=nj<n and (ni,nj) not in blocked:
                dist = BFS(ni,nj,info[1][0],info[1][1])
                if dist < min_dist:
                    min_dist,npi,npj = dist,ni,nj

        info[0] = (npi,npj)

        if (npi,npj) == (info[1][0],info[1][1]): # 편의점 도착
            del_idx.append(idx)
            blocked_candidate.append((npi,npj))

    # 도착한 편의점 ban
    for bli,blj in blocked_candidate:
        blocked.append((bli,blj))

    # 종료 조건
    for idx in del_idx:
        del player[idx]

    if len(player) == 0:
        break

    # 베캠 이동
    if time <= m:
        cvi,cvj = player[time][1]
        min_dist,bi,bj = 3*(n**2), n, n
        for i,j in base:
            dist = BFS(i,j,cvi,cvj)
            if dist < min_dist:
                min_dist,bi,bj = dist,i,j
            elif dist == min_dist:
                if i < bi:
                    min_dist,bi,bj = dist,i,j
                elif i == bi:
                    if j < bj:
                        min_dist,bi,bj = dist,i,j

        player[time][0] = (bi,bj)
        blocked.append((bi,bj))
        base.remove((bi,bj))

    # 시간 증가
    time += 1

print(time)