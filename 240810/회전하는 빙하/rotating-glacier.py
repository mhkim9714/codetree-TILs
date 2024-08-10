n,q = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(2**n)]

def BFS(si,sj):
    q = []

    q.append((si,sj))
    visited[si][sj] = 1

    cnt = 1
    while q:
        ci,cj = q.pop(0)
        for ni,nj in ((ci-1,cj),(ci,cj+1),(ci+1,cj),(ci,cj-1)):
            if 0<=ni<(2**n) and 0<=nj<(2**n) and visited[ni][nj]==0 and arr[ni][nj]>0:
                q.append((ni,nj))
                visited[ni][nj] = 1
                cnt += 1

    return cnt


rotate_levels = list(map(int, input().split()))
# 순서대로 모든 회전 진행
for L in rotate_levels:
    if L != 0:
        for i in range(2**n):
            for j in range(2**n):
                if i%(2**L)==0 and j%(2**L)==0: # i,j -> 회전 덩어리의 좌측 상단 좌표
                    top_left = [[0 for _ in range(2**(L-1))] for _ in range(2**(L-1))]
                    top_right = [[0 for _ in range(2**(L-1))] for _ in range(2**(L-1))]
                    bottom_left = [[0 for _ in range(2**(L-1))] for _ in range(2**(L-1))]
                    bottom_right = [[0 for _ in range(2**(L-1))] for _ in range(2**(L-1))]

                    # top_left ~ bottom_right 채워넣기
                    for x in range(i,i+2**(L-1)):
                        for y in range(j,j+2**(L-1)):
                            top_left[x-i][y-j] = arr[x][y]
                    for x in range(i,i+2**(L-1)):
                        for y in range(j+2**(L-1),j+2**L):
                            top_right[x-i][y-(j+2**(L-1))] = arr[x][y]
                    for x in range(i+2**(L-1),i+2**L):
                        for y in range(j,j+2**(L-1)):
                            bottom_left[x-(i+2**(L-1))][y-j] = arr[x][y]
                    for x in range(i+2**(L-1),i+2**L):
                        for y in range(j+2**(L-1),j+2**L):
                            bottom_right[x-(i+2**(L-1))][y-(j+2**(L-1))] = arr[x][y]

                    # arr에 알맞게 다시 채워넣기
                    for x in range(2**(L-1)):
                        for y in range(2**(L-1)):
                            arr[i+x][j+y] = bottom_left[x][y]
                            arr[i+x][j+2**(L-1)+y] = top_left[x][y]
                            arr[i+2**(L-1)+x][j+y] = bottom_right[x][y]
                            arr[i+2**(L-1)+x][j+2**(L-1)+y] = top_right[x][y]

    # 얼음 녹음
    narr = [x[:] for x in arr]
    for i in range(2 ** n):
        for j in range(2 ** n):
            if arr[i][j] > 0:
                adj = []
                for ni, nj in ((i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)):
                    if 0 <= ni < (2 ** n) and 0 <= nj < (2 ** n) and arr[ni][nj] > 0:
                        adj.append(arr[ni][nj])
                if len(adj) < 3:
                    narr[i][j] -= 1
    arr = narr


cnt_ice = 0
group_size = []
visited = [[0 for _ in range(2**n)] for _ in range(2**n)]

for i in range(2**n):
    for j in range(2**n):
        cnt_ice += arr[i][j]
        if arr[i][j]>0 and visited[i][j]==0:
            group_size.append(BFS(i,j))

print(cnt_ice)
if len(group_size) == 0:
    print(0)
else:
    print(max(group_size))