base = []
conv = []
people = []

n,m = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(n)]
for _ in range(m):
    ci,cj = map(int, input().split())
    conv.append((ci-1,cj-1))
    people.append((-1,-1))
for i in range(n):
    for j in range(n):
        if arr[i][j] == 1:
            base.append((i,j))
arr = [[0]*n for _ in range(n)]

# 거리구하는 함수 (막힌 루트 고려해서 최소거리를 구해야함)
def distance(si,sj,ei,ej):
    q = []
    visited = [[0]*n for _ in range(n)]

    q.append((si,sj))
    visited[si][sj] = 0

    while q:
        ci,cj = q.pop(0)
        if (ci,cj) == (ei,ej):
            break

        for di,dj in ((-1,0),(0,-1),(0,1),(1,0)):
            ni,nj = ci+di, cj+dj
            if 0<=ni<n and 0<=nj<n and visited[ni][nj]==0 and arr[ni][nj]!=1:
                q.append((ni,nj))
                visited[ni][nj] = visited[ci][cj]+1

    return visited[ei][ej]


time = 0
while True:
    if conv == people:
        break

    block = []
    for i, (pi,pj) in enumerate(people):
        if (pi,pj) != (-1,-1): # 격자내 사람에 대해서만 추출한 [사람의 좌표]
            ci,cj = conv[i] # 할당된 [편의점의 좌표]

            if (pi,pj) == (ci,cj): # 이미 편의점에 도착한 사람은 냅둠
                continue

            # [1] 격자내 모든 사람 최단 거리 이동 to 할당된 편의점
            min_d = 2*n
            ppi,ppj = pi,pj # [사람이 이동할 새로운 좌표]
            for di,dj in ((-1,0),(0,-1),(0,1),(1,0)):
                ni,nj = pi+di,pj+dj
                if 0<=ni<n and 0<=nj<n and arr[ni][nj]==0 and distance(ni,nj,ci,cj)<min_d:
                    min_d = distance(ni,nj,ci,cj)
                    ppi,ppj = ni,nj
            people[i] = (ppi,ppj)

            # [2] 할당된 편의점에 도착했다면 그 편의점 block list에 추가
            if (ppi,ppj) == (ci,cj):
                block.append((ci,cj))

    # [3] block 후보들 싹다 블로킹 진행
    for i, j in block:
        arr[i][j] = 1

    # [4] 사람들 베이스캠프에 할당
    if time < len(people):
        ci,cj = conv[time] # 해당 time의 타겟 편의점 좌표

        temp = []
        for bi,bj in base:
            if arr[bi][bj] == 0:
                temp.append((distance(bi,bj,ci,cj),bi,bj))

        sorted_temp = sorted(temp, key=lambda x: (x[0], x[1], x[2])) # 작->큰
        people[time] = sorted_temp[0][1], sorted_temp[0][2]
        arr[sorted_temp[0][1]][sorted_temp[0][2]] = 1

    time += 1

print(time)