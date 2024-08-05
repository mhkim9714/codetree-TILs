n,m = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(n)] # -5:빈칸, -1:돌, 0:빨폭, 1~m:색폭

def BFS(i,j,val):
    q = []
    lst = []

    q.append((i,j))
    visited[i][j] = 1
    lst.append((i,j))
    max_i,min_j,cnt_red = i,j,0

    while q:
        ci,cj = q.pop(0)
        for di,dj in ((-1,0),(0,1),(1,0),(0,-1)):
            ni,nj = ci+di,cj+dj
            if 0<=ni<n and 0<=nj<n and visited[ni][nj]==0: # 격자내 & 미방문
                if arr[ni][nj]==val: # 같은 색깔 폭탄
                    q.append((ni,nj))
                    visited[ni][nj] = 1
                    lst.append((ni,nj))
                    if max_i < ni:
                        max_i,min_j = ni,nj
                    elif max_i == nj and min_j > nj:
                        max_i,min_j = ni,nj
                elif arr[ni][nj]==0: # 빨간색 폭탄
                    q.append((ni,nj))
                    lst.append((ni,nj))
                    cnt_red += 1

    return lst, max_i, min_j, cnt_red

def gravity():
    for cj in range(n):
        for ci in range(n-1,-1,-1):
            if arr[ci][cj] >= 0: # 어떤 색깔이던 폭탄이 있다면
                ni,nj = ci,cj
                while True:
                    if 0<=ni+1<n and arr[ni+1][nj]==-5:
                        ni,nj = ni+1,nj
                    else:
                        if (ni,nj)!=(ci,cj):
                            arr[ni][nj] = arr[ci][cj]
                            arr[ci][cj] = -5
                        break


ans = 0
while True:
    # 폭탄 묶음 찾기 (BFS)
    bomb_lst = []
    bomb_red = 0
    bomb_max_i = 0
    bomb_min_j = 0

    visited = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if visited[i][j]==0 and arr[i][j]>0: # 미방문 & 색깔폭탄
                lst, max_i, min_j, cnt_red = BFS(i,j,arr[i][j])
                if len(lst) < 2:
                    continue

                if len(bomb_lst) < len(lst): # 더 큰 폭탄 묶음이면
                    bomb_lst = lst
                    bomb_red,bomb_max_i,bomb_min_j = cnt_red,max_i,min_j
                elif len(bomb_lst) == len(lst):
                    if bomb_red > cnt_red: # 빨간 폭탄을 더 조금 포함하면
                        bomb_lst = lst
                        bomb_red,bomb_max_i,bomb_min_j = cnt_red,max_i,min_j
                    elif bomb_red == cnt_red:
                        if bomb_max_i < max_i: # 기준점의 행이 더 크면
                            bomb_lst = lst
                            bomb_red,bomb_max_i,bomb_min_j = cnt_red,max_i,min_j
                        elif bomb_max_i == max_i:
                            if bomb_min_j > min_j: # 기준점의 열이 더 작으면
                                bomb_lst = lst
                                bomb_red,bomb_max_i,bomb_min_j = cnt_red,max_i,min_j

    if len(bomb_lst) == 0: # 더이상 폭탄 묶음이 존재하지 않으면 -> [종료 조건]
        break

    # 선택된 폭탄 제거
    for i,j in bomb_lst:
        arr[i][j] = -5
    ans += (len(bomb_lst))**2
    
    # 중력
    gravity()

    # 반시계 방향으로 90도 회전
    narr = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            narr[n-1-j][i] = arr[i][j]
    arr = narr

    # 중력
    gravity()

print(ans)