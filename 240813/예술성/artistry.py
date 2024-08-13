n = int(input())
arr = [list(map(int, input().split())) for _ in range(n)]


def bfs(si,sj,val,g_idx,group,visited):
    q = []

    q.append((si,sj))
    visited[si][sj] = g_idx
    g_lst = [(si,sj)]

    while q:
        ci,cj = q.pop(0)
        for di,dj in ((-1,0),(0,1),(1,0),(0,-1)):
            ni,nj = ci+di,cj+dj
            if 0<=ni<n and 0<=nj<n and visited[ni][nj]==0 and arr[ni][nj]==val:
                q.append((ni,nj))
                visited[ni][nj] = g_idx
                g_lst.append((ni,nj))

    group[g_idx] = [val, g_lst]


def scoring():
    group = dict()
    visited = [[0 for _ in range(n)] for _ in range(n)]
    g_idx = 1

    for i in range(n):
        for j in range(n):
            if visited[i][j] == 0:
                bfs(i,j,arr[i][j],g_idx,group,visited)
                g_idx += 1

    S = 0
    for g1_idx, g1_info in group.items():
        for g2_idx, g2_info in group.items():
            if g1_idx == g2_idx:
                continue

            adj_cnt = 0
            for (ci,cj) in g1_info[1]:
                for di,dj in ((-1,0),(0,1),(1,0),(0,-1)):
                    ni,nj = ci+di,cj+dj
                    if 0<=ni<n and 0<=nj<n and visited[ni][nj]==g2_idx:
                        adj_cnt += 1

            S += (len(g1_info[1])+len(g2_info[1])) * g1_info[0] * g2_info[0] * adj_cnt
    S = int(S / 2)
    return S


ans = scoring()
for _ in range(3):
    # 회전
    narr = [[0 for _ in range(n)] for _ in range(n)]
    square_length = int((n - 1) / 2)

    for i in range(n):
        for j in range(n):

            if i==int(n/2) or j==int(n/2): # 십자 모양 반시계 90도 회전
                narr[n-1-j][i] = arr[i][j]

            elif (i,j) in ((0,0), (0,int(n/2)+1), (int(n/2)+1,0), (int(n/2)+1,int(n/2)+1)): # 정사각형 시계 90도 회전
                temp = [[0 for _ in range(square_length)] for _ in range(square_length)]
                for ti in range(i,i+square_length):
                    for tj in range(j,j+square_length):
                        temp[ti-i][tj-j] = arr[ti][tj]
                for ti in range(square_length):
                    for tj in range(square_length):
                        narr[tj+i][square_length-1-ti+j] = temp[ti][tj]

    arr = narr

    # 점수
    ans += scoring()

print(ans)