INF = int(1e9+10)

N,M,F = map(int, input().split())

# 동0 남1 서2 북3
di = [0, 1, 0, -1]
dj = [1, 0, -1, 0]

bottom = [list(map(int, input().split())) for _ in range(N)]
bottom_idx = [[0 for _ in range(N)] for _ in range(N)]
wall = [[[0 for _ in range(M)] for _ in range(M)] for _ in range(5)] # [동0,남1,서2,북3,top4]
wall_idx = [[[0 for _ in range(M)] for _ in range(M)] for _ in range(5)]
for i in range(M):  # 동
    wall[0][i] = list(map(int, input().split()))
for i in range(M):  # 서
    wall[2][i] = list(map(int, input().split()))
for i in range(M):  # 남
    wall[1][i] = list(map(int, input().split()))
for i in range(M):  # 북
    wall[3][i] = list(map(int, input().split()))
for i in range(M):  # top
    wall[4][i] = list(map(int, input().split()))

events = []
for _ in range(F):
    r, c, d, v = map(int, input().split())
    if d == 1:  # 서
        direction = 2
    elif d == 2:  # 남
        direction = 1
    else:
        direction = d
    event = [(r,c), direction, v, 0] # 0:alive / 1: dead
    events.append(event)


# 1. 그래프 자료 구조 생성
# 1-1. vertex 생성 (1~100)
cnt = 0
for i in range(N):
    for j in range(N):
        if bottom[i][j] == 3:
            continue
        cnt += 1
        bottom_idx[i][j] = cnt

for w in range(5):
    for i in range(M):
        for j in range(M):
            cnt += 1
            wall_idx[w][i][j] = cnt

# 1-2. edge 생성
edge = [[-1 for _ in range(4)] for _ in range(cnt+1)] # -1:연결X / 1~100: 연결된 vertex 인덱스 (100*4) # 동남서북

# 1-2-1. bottom-bottom edge
for i in range(N):
    for j in range(N):
        if bottom[i][j] == 3:
            continue
        idx1 = bottom_idx[i][j]
        for d in range(4):
            ni,nj = i+di[d], j+dj[d]
            if 0<=ni<N and 0<=nj<N and bottom[ni][nj]!=3:
                idx2 = bottom_idx[ni][nj]
                edge[idx1][d] = idx2

# 1-2-2. wall(동남서북)-wall(동남서북) edge
for w in range(4):
    for i in range(M):
        for j in range(M):
            idx1 = wall_idx[w][i][j]
            for d in range(4):
                ni,nj = i+di[d], j+dj[d]
                if not 0<=ni<M:
                    continue
                if nj < 0:  # 동->남->서->북
                    idx2 = wall_idx[(w+1)%4][ni][M-1]
                    edge[idx1][d] = idx2
                elif nj >= M:  # 동->북->서->남
                    idx2 = wall_idx[(w+3)%4][ni][0]
                    edge[idx1][d] = idx2
                else: # 내부
                    idx2 = wall_idx[w][ni][nj]
                    edge[idx1][d] = idx2

# 1-2-3. wall(위)-wall(위) edge
for i in range(M):
    for j in range(M):
        idx1 = wall_idx[4][i][j]
        for d in range(4):
            ni,nj = i+di[d], j+dj[d]
            if 0<=ni<M and 0<=nj<M:
                idx2 = wall_idx[4][ni][nj]
                edge[idx1][d] = idx2

# 1-2-4. wall(위)-wall(동남서북) edge
for i in range(M):  # 동
    idx1 = wall_idx[4][i][M-1]
    idx2 = wall_idx[0][0][M-1-i]
    edge[idx1][0] = idx2
    edge[idx2][3] = idx1
for i in range(M):  # 남
    idx1 = wall_idx[4][M-1][i]
    idx2 = wall_idx[1][0][i]
    edge[idx1][1] = idx2
    edge[idx2][3] = idx1
for i in range(M):  # 서
    idx1 = wall_idx[4][i][0]
    idx2 = wall_idx[2][0][i]
    edge[idx1][2] = idx2
    edge[idx2][3] = idx1
for i in range(M):  # 북
    idx1 = wall_idx[4][0][i]
    idx2 = wall_idx[3][0][M-1-i]
    edge[idx1][3] = idx2
    edge[idx2][3] = idx1

# 1-2-5. bottom-wall(동남서북) edge
si, sj = -1, -1  # bottom에서 wall이 시작하는 좌상단 좌표
for i in range(N):
    for j in range(N):
        if bottom[i][j] == 3:
            si,sj = i,j
            break
    if si != -1:
        break

if si+M < N:  # 동
    for i in range(M):
        idx1 = bottom_idx[si+i][sj+M]
        idx2 = wall_idx[0][M-1][M-1-i]
        edge[idx1][2] = idx2
        edge[idx2][1] = idx1
if sj+M < N:  # 남
    for i in range(M):
        idx1 = bottom_idx[si+M][sj+i]
        idx2 = wall_idx[1][M-1][i]
        edge[idx1][3] = idx2
        edge[idx2][1] = idx1
if sj > 0:  # 서
    for i in range(M):
        idx1 = bottom_idx[si+i][sj-1]
        idx2 = wall_idx[2][M-1][i]
        edge[idx1][0] = idx2
        edge[idx2][1] = idx1
if si > 0:  # 북
    for i in range(M):
        idx1 = bottom_idx[si-1][sj+i]
        idx2 = wall_idx[3][M-1][M-1-i]
        edge[idx1][1] = idx2
        edge[idx2][1] = idx1


# 2. BFS 통해 최단 경로 찾기
time = 0
visited = [-1 for _ in range(cnt+1)] # 1~ 거리 / 0 시작점 / -1 미방문 / INF 장애물

# 2-1. 시작점 vertex 인덱스 찾기
s_idx = -1
for i in range(M):
    for j in range(M):
        if wall[4][i][j] == 2:
            s_idx = wall_idx[4][i][j]
            break
    if s_idx != -1:
        break

# 2-2. 끝점 vertex 인덱스 찾기
e_idx = -1
for i in range(N):
    for j in range(N):
        if bottom[i][j] == 4:
            e_idx = bottom_idx[i][j]
            break
    if e_idx != -1:
        break

# 2-3. 장애물 처리 (원래 장애물 & 이상 현상 시작 지점)
# 2-3-1. bottom 장애물 처리
for i in range(N):
    for j in range(N):
        if bottom[i][j] == 1:
            idx = bottom_idx[i][j]
            visited[idx] = INF

for e in range(F):
    r, c = events[e][0]
    idx = bottom_idx[r][c]
    visited[idx] = INF

# 2-3-2. wall 장애물 처리
for w in range(5):
    for i in range(M):
        for j in range(M):
            if wall[w][i][j] == 1:
                idx = wall_idx[w][i][j]
                visited[idx] = INF

q = [s_idx]
visited[s_idx] = 0
while True:
    time += 1

    # 해당 턴에 시간 이상 현상 확산 (빈공간'0'으로만 확산)
    for e in range(F):
        coord, d, v, a = events[e]
        r, c = coord

        if a == 1 or time % v != 0:
            continue

        step = time // v
        if d == 0:  # 동
            c += step
        elif d == 1:  # 남
            r += step
        elif d == 2:  # 서
            c -= step
        else:  # 북
            r -= step

        if not (0<=r<N and 0<=c<N):  # 격자 밖 -> 확산 X
            events[e][3] = 1
        elif bottom[r][c] != 0:  # 격자 내 & 빈공간 X -> 확산 X
            events[e][3] = 1
        else:  # 격자 내 & 빈공간 O -> 확산 O
            nidx = bottom_idx[r][c]
            visited[nidx] = INF

    # 타임 머신 이동 (BFS 1회)
    next_q = []
    while q:
        cidx = q.pop(0)
        for d in range(4):
            nidx = edge[cidx][d]
            if visited[nidx] == -1:  # 미방문
                next_q.append(nidx)
                visited[nidx] = time

    if len(next_q) == 0:
        break
    elif e_idx in next_q:
        break
    else:
        q = next_q


if visited[e_idx] == -1 or visited[e_idx] == INF:
    print(-1)
else:
    print(visited[e_idx])