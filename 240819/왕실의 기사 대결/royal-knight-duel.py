L,N,Q = map(int, input().split())

temp = [list(map(int, input().split())) for _ in range(L)]
trap = []
wall = []
for i in range(L):
    for j in range(L):
        if temp[i][j] == 1:
            trap.append((i,j))
        elif temp[i][j] == 2:
            wall.append((i,j))

arr = [[0 for _ in range(L)] for _ in range(L)]
knight = dict()
for idx in range(1,N+1):
    r,c,h,w,k = map(int, input().split())
    coord = []
    for i in range(h):
        for j in range(w):
            ki,kj = (r-1)+i, (c-1)+j
            arr[ki][kj] = idx
            coord.append((ki,kj))
    knight[idx] = [coord, k, 0]
for i,j in wall:
    arr[i][j] = -1

# 상0 우1 하2 좌3
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]


def BFS(idx,d):
    q = []
    visited = [[0 for _ in range(L)] for _ in range(L)]
    move_knight = []

    for i,j in knight[idx][0]:
        q.append((i,j))
        visited[i][j] = 1
    move_knight.append(idx)

    while q:
        ci,cj = q.pop(0)
        ni,nj = ci+di[d], cj+dj[d]
        if 0 <= ni < L and 0 <= nj < L:
            if visited[ni][nj] == 0:
                if arr[ni][nj] == -1:
                    return []
                elif arr[ni][nj] > 0 and arr[ni][nj] != arr[ci][cj]:
                    for i,j in knight[arr[ni][nj]][0]:
                        q.append((i,j))
                        visited[i][j] = 1
                    move_knight.append(arr[ni][nj])
        else:
            return []

    return move_knight


for _ in range(Q):
    if len(knight) == 0:
        print(0)
        break

    target_idx, d = map(int, input().split())
    if target_idx not in knight.keys():
        continue

    # 기사 이동
    move_knight = BFS(target_idx, d)
    if len(move_knight) == 0:
        continue

    # 대결 대미지
    narr = [[0 for _ in range(L)] for _ in range(L)]
    for i,j in wall:
        narr[i][j] = -1

    del_knight = []
    for idx, info in knight.items():
        if idx == target_idx: # 타겟 기사를 미는 경우 -> 이동O, 체력 깎임X, 대미지 누적X (arr,dict)
            new_coord = []
            for i,j in info[0]:
                ni,nj = i+di[d], j+dj[d]
                narr[ni][nj] = idx
                new_coord.append((ni,nj))
            info[0] = new_coord

        elif idx in move_knight: # 밀려난 기사를 미는 경우 -> 이동O, 체력 깎임O, 대미지 누적O (arr,dict)
            damage = 0
            new_coord = []
            for i,j in info[0]:
                ni,nj = i+di[d], j+dj[d]
                if (ni,nj) in trap:
                    damage += 1
                new_coord.append((ni,nj))

            if damage >= info[1]: # 기사 사라짐
                del_knight.append(idx)
            else: # 기사 유지
                for i,j in new_coord:
                    narr[i][j] = idx
                info[0] = new_coord
                info[1] = info[1] - damage
                info[2] += damage

        else: # 무관한 기사인 경우 -> 이동X, 체력 깎임X, 대미지 누적X
            for i,j in info[0]:
                narr[i][j] = idx

    arr = narr
    for del_idx in del_knight:
        del knight[del_idx]

else:
    ans = 0
    for idx, info in knight.items():
        ans += info[2]
    print(ans)