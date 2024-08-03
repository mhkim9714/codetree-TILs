L,N,Q = map(int,input().split())

arr = [[0]*L for _ in range(L)]
knight = dict() # [[(i1,j1),(i2,j2),...], 잔여체력, 누적대미지]
trap = []
wall = []

grid = [list(map(int,input().split())) for _ in range(L)]
for i in range(L):
    for j in range(L):
        if grid[i][j] == 1: # 함정
            trap.append((i,j))
        elif grid[i][j] == 2: # 벽
            arr[i][j] = -1
            wall.append((i,j))

for k_idx in range(1,N+1):
    r,c,h,w,k = map(int,input().split())
    locs = []
    for i in range(r-1, r-1+h):
        for j in range(c-1, c-1+w):
            arr[i][j] = k_idx
            locs.append((i,j))
    knight[k_idx] = [locs, k, 0]

# 상(0) 우(1) 하(2) 좌(3)
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]


for _ in range(Q):
    idx,d = map(int,input().split())

    if idx not in knight.keys(): # 탈락한 기사는 진행하지 않음
        continue

    # (1) 기사 이동
    q = []
    move_start = []

    for i,j in knight[idx][0]:
        q.append((i,j))

    while q:
        ci,cj = q.pop(0)
        ni,nj = ci+di[d],cj+dj[d]
        if 0<=ni<L and 0<=nj<L and arr[ni][nj]!=-1: # 다음 좌표가 범위내 & 벽X
            move_start.append((ci,cj))
            if arr[ni][nj]>0 and arr[ni][nj]!=arr[ci][cj]:
                for i,j in knight[arr[ni][nj]][0]:
                    q.append((i,j))
        else:
            move_start = []
            break

    # (2) 대결 대미지 축적
    if len(move_start) > 0:
        narr = [[0]*L for _ in range(L)]
        for wi,wj in wall:
            narr[wi][wj] = -1

        for k_idx, info in knight.items():
            if info[0][0] in move_start: # 해당 knight는 이동이 필요
                new_info = []
                for ci,cj in info[0]:
                    ni, nj = ci+di[d], cj+dj[d]
                    narr[ni][nj] = arr[ci][cj]
                    new_info.append((ni,nj))
                    if k_idx != idx:
                        if (ni, nj) in trap:
                            info[1] -= 1
                            info[2] += 1
                info[0] = new_info

            else: # 해당 knight는 이동이 필요 없음
                for ci,cj in info[0]:
                    narr[ci][cj] = arr[ci][cj]
        arr = narr

        # knight에서 탈락하는 기사 삭제
        del_knight_idx, del_knight_coords = [],[]
        for k_idx, info in knight.items():
            if info[1] <= 0:
                del_knight_idx.append(k_idx)
                del_knight_coords.extend(info[0])
        for k_idx in del_knight_idx:
            del knight[k_idx]
        for rmi,rmj in del_knight_coords:
            arr[rmi][rmj] = 0

ans = 0
for k_idx, info in knight.items():
    ans += info[2]
print(ans)