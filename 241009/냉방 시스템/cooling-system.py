import copy

# 상(0) 우(1) 하(2) 좌(3)
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

n,m,k = map(int, input().split())
tmp = [list(map(int, input().split())) for _ in range(n)]
wall = []
for _ in range(m):
    x,y,s = map(int, input().split())
    ci,cj = x-1,y-1
    if s == 0:
        ni,nj = ci+di[0], cj+dj[0]
    else:
        ni,nj = ci+di[3], cj+dj[3]
    wall.append({(ci,cj), (ni,nj)})


def blow(wi,wj,wd):
    grid = [[0 for _ in range(n)] for _ in range(n)]

    si,sj = wi+di[wd], wj+dj[wd]
    grid[si][sj] = 5
    q = [(si,sj)]

    check_direction = [[(wd-1)%4,wd], [wd], [(wd+1)%4,wd]]
    while q:
        ori_i,ori_j = q.pop(0)
        for dir_lst in check_direction:
            ci,cj = ori_i,ori_j
            for d in dir_lst:
                ni,nj = ci+di[d],cj+dj[d]
                if 0<=ni<n and 0<=nj<n and {(ci,cj),(ni,nj)} not in wall:
                    ci,cj = ni,nj
                else:
                    break
            else:
                grid[ci][cj] = grid[ori_i][ori_j]-1
                if grid[ci][cj] > 1:
                    q.append((ci,cj))
    return grid


office = []
wind_list = []
for i in range(n):
    for j in range(n):
        if tmp[i][j] == 1: # 사무실
            office.append((i,j))
        elif tmp[i][j] == 2: # 왼쪽 에어컨
            wind_list.append(blow(i,j,3))
        elif tmp[i][j] == 3: # 위쪽 에어컨
            wind_list.append(blow(i,j,0))
        elif tmp[i][j] == 4: # 오른쪽 에어컨
            wind_list.append(blow(i,j,1))
        elif tmp[i][j] == 5: # 아래쪽 에어컨
            wind_list.append(blow(i,j,2))
wind_init = [[0 for _ in range(n)] for _ in range(n)]
for wind in wind_list:
    for i in range(n):
        for j in range(n):
            wind_init[i][j] += wind[i][j]


arr = [[0 for _ in range(n)] for _ in range(n)]
t = 0
while True:
    t += 1

    # 1) 모든 에어컨에 대해 생성된 시원함 총합
    for i in range(n):
        for j in range(n):
            arr[i][j] += wind_init[i][j]

    # 2) 시원한 공기가 섞임
    narr = copy.deepcopy(arr)
    done = [[[] for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for d in range(4):
                ni,nj = i+di[d], j+dj[d]
                if 0<=ni<n and 0<=nj<n and {(i,j),(ni,nj)} not in wall and (ni,nj) not in done[i][j]:
                    delta = abs(arr[i][j]-arr[ni][nj])//4
                    if arr[i][j] > arr[ni][nj]:
                        narr[i][j] -= delta
                        narr[ni][nj] += delta
                        done[i][j].append((ni,nj))
                        done[ni][nj].append((i,j))
                    elif arr[i][j] < arr[ni][nj]:
                        narr[i][j] += delta
                        narr[ni][nj] -= delta
                        done[i][j].append((ni,nj))
                        done[ni][nj].append((i,j))
    arr = narr

    # 3) 외벽과 맞닿은 칸에 대해서 시원함 1씩 감소
    for i in range(n):
        for j in range(n):
            if i in [0, n-1] or j in [0, n-1]:
                arr[i][j] = max(0, arr[i][j]-1)

    # 4) 종료 조건
    for oi,oj in office:
        if arr[oi][oj] < k:
            break
    else:
        print(t)
        break

    if t > 100:
        print(-1)
        break