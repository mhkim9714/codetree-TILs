# 동0 남1 서2 북3
di = [0, 1, 0, -1]
dj = [1, 0, -1, 0]

N, M, F = map(int, input().split())

floor = [[0 for _ in range(N)] for _ in range(N)]  # NxN
floor_idx = [[0 for _ in range(N)] for _ in range(N)]  # NxN (1~64)
wall = [[[0 for _ in range(M)] for _ in range(M)] for _ in range(5)]  # 5xMxM (동남서북위)
wall_idx = [[[0 for _ in range(M)] for _ in range(M)] for _ in range(5)]  # 5xMxM (동남서북위)(65~109)

############### NODE ###############
cnt = 1
# 평면도 채우기
tmp = [list(map(int, input().split())) for _ in range(N)]
for i in range(N):
    for j in range(N):
        floor[i][j] = tmp[i][j]
        floor_idx[i][j] = cnt
        cnt += 1

# 시간의 벽 채우기 (동남서북위 순서로)
east = [list(map(int, input().split())) for _ in range(M)]
west = [list(map(int, input().split())) for _ in range(M)]
south = [list(map(int, input().split())) for _ in range(M)]
north = [list(map(int, input().split())) for _ in range(M)]
up = [list(map(int, input().split())) for _ in range(M)]
for idx, tmp in enumerate([east, south, west, north, up]):
    for i in range(M):
        for j in range(M):
            wall[idx][i][j] = tmp[i][j]
            wall_idx[idx][i][j] = cnt
            cnt += 1

############### EDGE ###############
adj = [[0 for _ in range(4)] for _ in range(cnt)]  # 총 노드 수(cnt) x 4(동남서북); idx 0은 무시
# Edge: 평-평
for i in range(N):
    for j in range(N):
        if floor[i][j] == 3:
            continue
        for d in range(4):
            ni,nj = i+di[d], j+dj[d]
            if 0<=ni<N and 0<=nj<N and floor[ni][nj]!=3:
                adj[floor_idx[i][j]][d] = floor_idx[ni][nj]

# Edge: 평-{동0남1서2북3}
si, sj, end_flag = -1, -1, 0  # 평면도 기준 시간의 벽 시작 좌표 구하기
for i in range(N):
    for j in range(N):
        if floor[i][j] == 3:
            si, sj, end_flag = i, j, 1
            break
    if end_flag == 1:
        break
for a in range(M):  # 평-동
    floor_i, floor_j = si+a, sj+M
    east_i, east_j = M-1, M-1-a
    f_idx, e_idx = floor_idx[floor_i][floor_j], wall_idx[0][east_i][east_j]
    adj[f_idx][2], adj[e_idx][1] = e_idx, f_idx
for a in range(M):  # 평-남
    floor_i, floor_j = si+M, sj+a
    south_i, south_j = M-1, a
    f_idx, s_idx = floor_idx[floor_i][floor_j], wall_idx[1][south_i][south_j]
    adj[f_idx][3], adj[s_idx][1] = s_idx, f_idx
for a in range(M):  # 평-서
    floor_i, floor_j = si+a, sj-1
    west_i, west_j = M-1, a
    f_idx, w_idx = floor_idx[floor_i][floor_j], wall_idx[2][west_i][west_j]
    adj[f_idx][0], adj[w_idx][1] = w_idx, f_idx
for a in range(M):  # 평-북
    floor_i, floor_j = si-1, sj+a
    north_i, north_j = M-1, M-1-a
    f_idx, n_idx = floor_idx[floor_i][floor_j], wall_idx[3][north_i][north_j]
    adj[f_idx][1], adj[n_idx][1] = n_idx, f_idx

# Edge: {동남서북}-{동남서북}
for f in range(4):
    for i in range(M):
        for j in range(M):
            for d in range(4):
                ni, nj = i+di[d], j+dj[d]
                if not 0<=ni<M:
                    continue
                if nj<0:
                    adj[wall_idx[f][i][j]][d] = wall_idx[(f+1)%4][ni][M-1]
                elif 0<=nj<M:
                    adj[wall_idx[f][i][j]][d] = wall_idx[f][ni][nj]
                else:
                    adj[wall_idx[f][i][j]][d] = wall_idx[(f-1)%4][ni][0]

# Edge: 위-위
for i in range(M):
    for j in range(M):
        for d in range(4):
            ni, nj = i+di[d], j+dj[d]
            if 0<=ni<M and 0<=nj<M:
                adj[wall_idx[4][i][j]][d] = wall_idx[4][ni][nj]

# Edge: 위-{동0남1서2북3}
for a in range(M):  # 위-동
    up_i, up_j = a, M-1
    east_i, east_j = 0, M-1-a
    u_idx, e_idx = wall_idx[4][up_i][up_j], wall_idx[0][east_i][east_j]
    adj[u_idx][0], adj[e_idx][3] = e_idx, u_idx
for a in range(M):  # 위-남
    up_i, up_j = M-1, a
    south_i, south_j = 0, a
    u_idx, s_idx = wall_idx[4][up_i][up_j], wall_idx[1][south_i][south_j]
    adj[u_idx][1], adj[s_idx][3] = s_idx, u_idx
for a in range(M):  # 위-서
    up_i, up_j = a, 0
    west_i, west_j = 0, a
    u_idx, w_idx = wall_idx[4][up_i][up_j], wall_idx[2][west_i][west_j]
    adj[u_idx][2], adj[w_idx][3] = w_idx, u_idx
for a in range(M):  # 위-북
    up_i, up_j = 0, a
    north_i, north_j = 0, M-1-a
    u_idx, n_idx = wall_idx[4][up_i][up_j], wall_idx[3][north_i][north_j]
    adj[u_idx][3], adj[n_idx][3] = n_idx, u_idx


# 이상 현상 저장
event = dict()  # idx: [(좌표), 방향, 확산상수]
for e_idx in range(1,F+1):
    r, c, d, v = map(int, input().split())
    if d == 1:  # 서
        d = 2
    elif d == 2:  # 남
        d = 1
    event[e_idx] = [(r, c), d, v]
    floor[r][c] = 1


# 시작점과 도착점 인덱스 구하기
start_idx, end_flag = -1, 0
for i in range(M):
    for j in range(M):
        if wall[4][i][j] == 2:
            start_idx, end_flag = wall_idx[4][i][j], 1
            break
    if end_flag == 1:
        break

end_idx, end_flag = -1, 0
for i in range(N):
    for j in range(N):
        if floor[i][j] == 4:
            end_idx, end_flag = floor_idx[i][j], 1
            break
    if end_flag == 1:
        break


q_idx = []
visited_idx = [-1 for _ in range(cnt)]  # -2: 못방문, -1: 미방문, 0~: 방문한 시각

for i in range(N):
    for j in range(N):
        if floor[i][j] in [1,3]:
            visited_idx[floor_idx[i][j]] = -2
for f in range(5):
    for i in range(M):
        for j in range(M):
            if wall[f][i][j] == 1:
                visited_idx[wall_idx[f][i][j]] = -2

q_idx.append(start_idx)
visited_idx[start_idx] = 0

time = 1
ans = -1
while True:
    if len(q_idx) == 0:
        break

    # 이상 현상 확산
    del_e_idx = []
    for e_idx, info in event.items():
        if time % info[2] == 0:
            times = time // info[2]
            next_event_i, next_event_j = info[0][0]+times*di[info[1]], info[0][1]+times*dj[info[1]]
            if floor[next_event_i][next_event_j] == 0:
                visited_idx[floor_idx[next_event_i][next_event_j]] = -2
            else:
                del_e_idx.append(e_idx)
    for e_idx in del_e_idx:
        del event[e_idx]

    # 타임머신 이동
    next_q_idx = []
    while q_idx:
        c_idx = q_idx.pop(0)
        for d in range(4):
            n_idx = adj[c_idx][d]
            if n_idx>0 and visited_idx[n_idx]==-1:
                next_q_idx.append(n_idx)
                visited_idx[n_idx] = time

                if n_idx == end_idx:
                    ans = time
                    break
        if ans != -1:
            break
    if ans != -1:
        break

    time += 1
    q_idx = next_q_idx


print(ans)


