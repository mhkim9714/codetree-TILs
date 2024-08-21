n,m = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(n)]
red_coord = []


def BFS(si,sj,val):
    q = [(si,sj)]
    visited[si][sj] = 1
    coord_lst = [(si,sj)]
    red_cnt = 0
    red_coord_lst = []

    while q:
        ci,cj = q.pop(0)
        for di,dj in ((-1,0),(0,1),(1,0),(0,-1)):
            ni,nj = ci+di,cj+dj
            if 0<=ni<n and 0<=nj<n and visited[ni][nj]==0:
                if arr[ni][nj] == val:
                    q.append((ni,nj))
                    visited[ni][nj] = 1
                    coord_lst.append((ni,nj))
                elif arr[ni][nj] == 0:
                    q.append((ni,nj))
                    visited[ni][nj] = 1
                    coord_lst.append((ni,nj))
                    red_cnt += 1
                    red_coord_lst.append((ni,nj))

    if len(coord_lst) < 2:
        return [], []
    else:
        bi,bj = -1,n
        for i,j in coord_lst:
            if arr[i][j] != 0:
                if bi < i:
                    bi,bj = i,j
                elif bi == i:
                    if bj > j:
                        bi,bj = i,j

        return [coord_lst, red_cnt, (bi,bj)], red_coord_lst


def gravity():
    for cj in range(n):
        for ci in range(n-1,-1,-1):
            if arr[ci][cj] < 0:
                continue

            ni,nj = ci+1,cj
            while True:
                if ni>=n or arr[ni][nj]>=-1:
                    if (ni-1,nj) != (ci,cj):
                        arr[ni-1][nj] = arr[ci][cj]
                        arr[ci][cj] = -2
                    break
                else:
                    ni,nj = ni+1,nj


score = 0
while True:
    # 폭탄 묶음 찾기
    bomb_lst = []
    visited = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if arr[i][j]>0 and visited[i][j]==0:
                info, red_lst = BFS(i,j,arr[i][j])
                if len(info) > 0:
                    bomb_lst.append(info)
                    for ri,rj in red_lst:
                        visited[ri][rj] = 0

    # 종료 조건
    if len(bomb_lst) == 0:
        break

    # 제거할 폭탄 묶음 선택
    bomb_idx = 0
    for idx in range(1,len(bomb_lst)):
        if len(bomb_lst[bomb_idx][0]) < len(bomb_lst[idx][0]):
            bomb_idx = idx
        elif len(bomb_lst[bomb_idx][0]) == len(bomb_lst[idx][0]):
            if bomb_lst[bomb_idx][1] > bomb_lst[idx][1]:
                bomb_idx = idx
            elif bomb_lst[bomb_idx][1] == bomb_lst[idx][1]:
                if bomb_lst[bomb_idx][2][0] < bomb_lst[idx][2][0]:
                    bomb_idx = idx
                elif bomb_lst[bomb_idx][2][0] == bomb_lst[idx][2][0]:
                    if bomb_lst[bomb_idx][2][1] > bomb_lst[idx][2][1]:
                        bomb_idx = idx

    # 선택된 폭탄 제거
    score += (len(bomb_lst[bomb_idx][0])**2)
    for i,j in bomb_lst[bomb_idx][0]:
        arr[i][j] = -2

    # 중력 작용
    gravity()

    # 반시계방향으로 90도 회전
    narr = [[-2 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            narr[n-1-j][i] = arr[i][j]
    arr = narr

    # 다시 중력 작용
    gravity()

print(score)