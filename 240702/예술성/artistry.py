import sys
sys.stdin = open('input.txt', 'r')

n = int(input())
M = int(n/2)
arr = []
for _ in range(n):
    input_list = list(map(int, input().split()))
    arr.append(input_list)


def bfs(si,sj,val,total_visited):
    q = []
    visited = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if total_visited[i][j] == 1:
                visited[i][j] = -1

    q.append((si,sj))
    visited[si][sj] = 1
    total_visited[si][sj] = 1
    cnt = 1

    while q:
        ci,cj = q.pop(0)
        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)): # 상하좌우
            ni,nj = ci+di,cj+dj
            if 0<=ni<n and 0<=nj<n and visited[ni][nj]==0 and arr[ni][nj]==val:
                q.append((ni,nj))
                visited[ni][nj] = 1
                total_visited[ni][nj] = 1
                cnt += 1

    for i in range(n):
        for j in range(n):
            visited[i][j] = max(0,visited[i][j])

    return cnt, val, visited, total_visited


def scoring(arr):
    group = []
    g_idx = 0
    g_arr = [[0 for _ in range(n)] for _ in range(n)]

    total_visited = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if total_visited[i][j] == 0:
                # BFS
                cnt, val, visited, total_visited = bfs(i,j,arr[i][j],total_visited)
                group.append((cnt,val))
                visited = [[x * g_idx for x in row] for row in visited] # 2d list multiplication by scalar value
                g_arr = [[a+b for a,b in zip(i, j)] for i,j in zip(g_arr, visited)] # 2d list 끼리 element-wise addition
                g_idx += 1

    # 그룹끼리 맞닿는 면 계산
    adj_arr = [[0 for _ in range(len(group))] for _ in range(len(group))]

    for i in range(len(group)):
        for j in range(len(group)):
            if i == j:
                adj_arr[i][j] = 0

            else:
                cnt = 0
                for x in range(n):
                    for y in range(n):
                        if g_arr[x][y] == i:
                            for dx,dy in ((-1,0),(1,0),(0,-1),(0,1)): # 상하좌우
                                nx,ny = x+dx, y+dy
                                if 0<=nx<n and 0<=ny<n and g_arr[nx][ny] == j:
                                    cnt += 1
                adj_arr[i][j] = cnt

    # 점수 계산
    score = 0
    for i in range(len(group)):
        for j in range(len(group)):
            score += (group[i][0]+group[j][0])*group[i][1]*group[j][1]*adj_arr[i][j]

    return int(score/2)

def rotate(arr):
    new_arr = [[0 for _ in range(n)] for _ in range(n)]

    # 십자 회전 - 세로선
    for i in range(n):
        new_arr[M][i] = arr[i][M]
    # 십자 회전 - 가로선
    for i in range(n):
        new_arr[n-i-1][M] = arr[M][i]

    # 그 외 회전
    start = [(0,0),(0,M+1),(M+1,0),(M+1,M+1)]

    for (oi,oj) in start:
        for i in range(M):
            for j in range(M):
                new_arr[j+oi][(M-1)-i+oj] = arr[i+oi][j+oj]

    return new_arr


ans = scoring(arr)

for _ in range(3):
    # 회전
    arr = rotate(arr)
    # 점수
    ans += scoring(arr)

print(ans)