n,m,k = map(int, input().split())
arr = []
for _ in range(n):
    arr.append(list(map(int, input().split())))

# 방향: 우(0), 상(1), 좌(2), 하(3)
bdi = [0, -1, 0, 1]
bdj = [1, 0, -1, 0]

# 공 던져지는 순서 미리 정해놓기 (4n회) -> (0,i,bd) or (1,j,bd)
ball = []
for i in range(n):
    ball.append((0,i,0))
for j in range(n):
    ball.append((1,j,1))
for i in range(n-1,-1,-1):
    ball.append((0,i,2))
for j in range(n-1,-1,-1):
    ball.append((1,j,3))

def bfs(si,sj):
    q = []
    visited = [[-1 for _ in range(n)] for _ in range(n)]
    head, tail = [], []
    cnt = 0

    q.append((si,sj))
    visited[si][sj] = cnt
    if arr[si][sj] == 1:
        head = (si,sj)
    elif arr[si][sj] == 3:
        tail = (si,sj)

    while q:
        ci,cj = q.pop(0)
        cnt += 1
        for di,dj in [(0,1),(0,-1),(1,0),(-1,0)]:
            ni,nj = ci+di,cj+dj
            if 0<=ni<n and 0<=nj<n and visited[ni][nj]==-1 and arr[ni][nj]>=1 and arr[ni][nj]<=3:
                if arr[ni][nj] == 1:
                    head = (ni, nj)
                elif arr[ni][nj] == 3:
                    tail = (ni, nj)

                q.append((ni,nj))
                visited[ni][nj] = cnt
                break

    return head, tail, visited[head[0]][head[1]]+1

ans = 0
for rnd in range(k):
    # 사람 한칸 이동 (동시에)
    narr = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if arr[i][j] == 4:
                for (di,dj) in [(0,1),(0,-1),(1,0),(-1,0)]:
                    ni,nj = i+di,j+dj
                    if 0<=ni<n and 0<=nj<n and arr[ni][nj]==1:
                        narr[i][j] = 1
                        break
                    elif 0<=ni<n and 0<=nj<n and arr[ni][nj]!=1:
                        narr[i][j] = 4
            if arr[i][j] == 2:
                for (di,dj) in [(0,1),(0,-1),(1,0),(-1,0)]:
                    ni,nj = i+di,j+dj
                    if 0<=ni<n and 0<=nj<n and arr[ni][nj]==3:
                        narr[i][j] = 3
                        break
                    elif 0<=ni<n and 0<=nj<n and arr[ni][nj]!=3:
                        narr[i][j] = 2
            elif arr[i][j] in [1,3]:
                narr[i][j] = arr[i][j] + 1
    arr = narr

    # 공 던져지는 축,좌표 결정
    axis, idx, dir = ball[rnd%(4*n)]
    if axis == 0: # 행축
        si,sj = idx,0
    else: # 열축
        si,sj = 0,idx

    # 사람 맞추고 점수 & 머리 꼬리 체인지
    ci,cj = si,sj
    for _ in range(n):
        if arr[ci][cj] in [1,2,3]: # 사람 맞춘 경우 -> 점수 올리고, 머리 꼬리 체인지
            head, tail, score = bfs(ci,cj)
            ans += (score*score)
            arr[head[0]][head[1]] = 3
            arr[tail[0]][tail[1]] = 1
            break
        ci,cj = ci+bdi[dir],cj+bdj[dir]

print(ans)