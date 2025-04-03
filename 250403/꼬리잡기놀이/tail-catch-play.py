# 1->2 / 2->2or3 / 3->4or1 / 4->4or1
def dfs(ci, cj, visited, idx):
    for di, dj in [(-1,0), (0,1), (1,0), (0,-1)]:
        ni, nj = ci+di, cj+dj
        if 0<=ni<n and 0<=nj<n:
            if tmp[ci][cj]==1 and tmp[ni][nj]==2:
                visited.append((ni, nj))
                arr[ni][nj] = [idx, tmp[ni][nj]]
                return dfs(ni, nj, visited, idx)
            elif tmp[ci][cj]==2 and tmp[ni][nj] in [2,3] and (ni,nj) not in visited:
                visited.append((ni, nj))
                arr[ni][nj] = [idx, tmp[ni][nj]]
                return dfs(ni, nj, visited, idx)
            elif tmp[ci][cj]==3 and tmp[ni][nj]==4:
                visited.append((ni, nj))
                arr[ni][nj] = [idx, tmp[ni][nj]]
                return dfs(ni, nj, visited, idx)
            elif tmp[ci][cj]==3 and tmp[ni][nj]==1:
                return visited
            elif tmp[ci][cj]==4 and tmp[ni][nj]==4 and (ni,nj) not in visited:
                visited.append((ni, nj))
                arr[ni][nj] = [idx, tmp[ni][nj]]
                return dfs(ni, nj, visited, idx)
            elif tmp[ci][cj]==4 and tmp[ni][nj]==1:
                return visited


n, m, k = map(int, input().split())
tmp = [list(map(int, input().split())) for _ in range(n)]

arr = [[[-1, 0] for _ in range(n)] for _ in range(n)]  # [팀인덱스, 1~4]
team = dict()
idx = 1
for i in range(n):
    for j in range(n):
        if tmp[i][j] == 1:
            visited = [(i, j)]
            arr[i][j] = [idx, 1]
            team[idx] = dfs(i, j, visited, idx)
            idx += 1

throw_i = [x for x in range(n)] + [n-1 for _ in range(n)] + [x for x in range(n-1, -1, -1)] + [0 for _ in range(n)]
throw_j = [0 for _ in range(n)] + [x for x in range(n)] + [n-1 for _ in range(n)] + [x for x in range(n-1, -1, -1)]
throw_di = [0 for _ in range(n)] + [-1 for _ in range(n)] + [0 for _ in range(n)] + [1 for _ in range(n)]
throw_dj = [1 for _ in range(n)] + [0 for _ in range(n)] + [-1 for _ in range(n)] + [0 for _ in range(n)]


score = 0
for rnd in range(k):
    # 1. 각팀 한칸씩 이동 => arr,dict 모두 변화
    new_arr = [[[-1, 0] for _ in range(n)] for _ in range(n)]
    for idx in team.keys():
        coord = team[idx]
        new_coord = [coord[-1]] + coord[:-1]
        for cnt, (i, j) in enumerate(coord):
            new_arr[new_coord[cnt][0]][new_coord[cnt][1]] = [idx, arr[i][j][1]]
        team[idx] = new_coord
    arr = new_arr

    # 2. 라운드에 맞춰서 공 던져지는 시작점, 방향 구하기
    th_i = throw_i[rnd%(4*n)]
    th_j = throw_j[rnd%(4*n)]
    th_di = throw_di[rnd%(4*n)]
    th_dj = throw_dj[rnd%(4*n)]

    # 3. 그 행or열로 for문 돌리면서,
    while True:
        if 0<=th_i<n and 0<=th_j<n:
            if 1<= arr[th_i][th_j][1] <= 3:
                idx = arr[th_i][th_j][0]
                order = team[idx].index((th_i,th_j)) + 1
                score += order**2

                coord = team[idx]
                tail = -1
                for cnt, (i, j) in enumerate(coord):
                    if arr[i][j][1] == 3:
                        tail = cnt
                        break
                new_coord = list(reversed(coord[:tail+1])) + list(reversed(coord[tail+1:]))
                arr[coord[0][0]][coord[0][1]][1] = 3
                arr[coord[tail][0]][coord[tail][1]][1] = 1
                team[idx] = new_coord
                break

            else:
                th_i, th_j = th_i+th_di, th_j+th_dj
        else:
            break

print(score)
