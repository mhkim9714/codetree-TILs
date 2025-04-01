L, N, Q = map(int, input().split())
arr_init = [list(map(int, input().split())) for _ in range(L)]
knight_init = [list(map(int, input().split())) for _ in range(N)]

pitfall = set()
wall = []
arr = [[0 for _ in range(L)] for _ in range(L)]  # -1:벽, 0:빈칸, 1~:기사인덱스
for i in range(L):
    for j in range(L):
        if arr_init[i][j] == 1:
            pitfall.add((i,j))
        elif arr_init[i][j] == 2:
            wall.append((i,j))
            arr[i][j] = -1

knight = dict()
for idx in range(1, N+1):
    r, c, h, w, k = knight_init[idx-1]
    r, c = r-1, c-1
    coords = []
    for i in range(r, r+h):
        for j in range(c, c+w):
            coords.append((i,j))
            arr[i][j] = idx
    knight[idx] = [coords, k, 0]  # [모든 좌표 리스트, 초기 체력, 누적 대미지]

# 상0 우1 하2 좌3
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]


for _ in range(Q):  # O(100)
    target_idx, d = map(int, input().split())

    # (1) 기사 이동
    if target_idx not in knight.keys():  # O(30)
        continue

    # BFS -> O(1600)
    q = []  # 이동 묶음이 되는 모든 좌표
    visited = []  # 이동하는 모든 기사 인덱스

    for coord in knight[target_idx][0]:
        q.append(coord)
    visited.append(target_idx)

    while q:
        ci, cj = q.pop(0)
        ni, nj = ci+di[d], cj+dj[d]
        if 0<=ni<L and 0<=nj<L:
            if arr[ni][nj] in visited:
                continue
            else:
                if arr[ni][nj] == 0:  # 빈칸인 경우
                    continue
                elif arr[ni][nj] == -1:  # 벽인 경우
                    visited = []
                    break
                else:  # 다른 기사인 경우
                    for coord in knight[arr[ni][nj]][0]:
                        q.append(coord)
                    visited.append(arr[ni][nj])
        else:
            visited = []
            break

    if len(visited) == 0:
        continue

    # (2) 대결 대미지
    new_arr = [[0 for _ in range(L)] for _ in range(L)]  # O(1600)
    for i, j in wall:
        new_arr[i][j] = -1

    for idx in knight.keys():
        if idx in visited:  # 움직인 기사 처리 -> arr 변경, knight [변경, 유지, 변경]
            new_coords = []
            for ci, cj in knight[idx][0]:
                ni, nj = ci+di[d], cj+dj[d]
                new_coords.append((ni,nj))
                new_arr[ni][nj] = idx
                if idx != target_idx:
                    if (ni, nj) in pitfall:
                        knight[idx][2] += 1
            knight[idx][0] = new_coords

        else:  # 안 움직인 기사 처리 -> arr 변경, knight [유지, 유지, 유지]
            for ci, cj in knight[idx][0]:
                new_arr[ci][cj] = idx
    arr = new_arr

    del_idx = []
    for idx in knight.keys():
        if knight[idx][1] <= knight[idx][2]:
            del_idx.append(idx)
    for idx in del_idx:
        for i, j in knight[idx][0]:
            arr[i][j] = 0
        del knight[idx]


answer = 0
for idx, info in knight.items():
    answer += info[2]

print(answer)

