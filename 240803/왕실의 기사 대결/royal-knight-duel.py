L,N,Q = map(int,input().split())

arr = [[0]*L for _ in range(L)]
knight = dict() # [[(i1,j1),(i2,j2),...], 잔여체력, 누적대미지]
trap = []

grid = [list(map(int,input().split())) for _ in range(L)]
for i in range(L):
    for j in range(L):
        if grid[i][j] == 1: # 함정
            trap.append((i,j))
        elif grid[i][j] == 2: # 벽
            arr[i][j] = -1

for kidx in range(1,N+1):
    r,c,h,w,k = map(int,input().split())
    locs = []
    for i in range(r-1, r-1+h):
        for j in range(c-1, c-1+w):
            arr[i][j] = kidx
            locs.append((i,j))
    knight[kidx] = [locs, k, 0]

# 상(0) 우(1) 하(2) 좌(3)
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]


for _ in range(Q):
    i,d = map(int,input().split())

    if i not in knight.keys(): # 탈락한 기사는 진행하지 않음
        continue

    # (1) 기사 이동
    q = []
    move_start = []

    for ki,kj in knight[i][0]:
        q.append((ki,kj))

    while q:
        ci,cj = q.pop(0)
        ni,nj = ci+di[d],cj+dj[d]
        if 0<=ni<L and 0<=nj<L and arr[ni][nj]!=-1: # 다음 좌표가 범위내 & 벽X
            move_start.append((ci,cj))
            if arr[ni][nj]>0 and arr[ni][nj]!=arr[ci][cj]:
                for ki,kj in knight[arr[ni][nj]][0]:
                    q.append((ki,kj))
        else:
            move_start = []
            break

    # (2) 대결 대미지 축적
    if len(move_start) > 0:
        for ci,cj in move_start[::-1]: # reverse
            kidx = arr[ci][cj]
            ni,nj = ci+di[d],cj+dj[d]

            if kidx != i: # 밀려난 기사들에 대해서만 대미지 누적
                if (ni,nj) in trap:
                    knight[kidx][1] -= 1
                    knight[kidx][2] += 1

            arr[ci][cj], arr[ni][nj] = 0, kidx
            knight[kidx][0].remove((ci,cj))
            knight[kidx][0].append((ni,nj))

        # knight에서 탈락하는 기사 삭제
        del_kidx, del_coords = [],[]
        for kidx, info in knight.items():
            if info[1] <= 0:
                del_kidx.append(kidx)
                del_coords.extend(info[0])
        for kidx in del_kidx:
            del knight[kidx]
        for rmi,rmj in del_coords:
            arr[rmi][rmj] = 0

ans = 0
for kidx, info in knight.items():
    ans += info[2]
print(ans)