L,N,Q = map(int, input().split())
knight = dict()
command = []
trap = [] #
wall = [] #
arr = [[-1]*L for _ in range(L)]

# 상(0) 우(1) 하(2) 좌(3)
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

temp = [list(map(int, input().split())) for _ in range(L)]
for i in range(L):
    for j in range(L):
        if temp[i][j] == 1:
            trap.append((i,j))
        elif temp[i][j] == 2:
            wall.append((i,j))

for i in range(N):
    r,c,h,w,k = map(int,input().split())
    si,sj = r-1,c-1
    ei,ej = si+(h-1),sj+(w-1)
    lst = []
    for a in range(si,ei+1):
        for b in range(sj,ej+1):
            lst.append((a,b))
            arr[a][b] = i
    knight[i] = [lst,k,0] # 좌표,체력,데미지

for _ in range(Q):
    i,d = map(int, input().split())
    command.append((i-1,d))


def move_targets(i,d):
    q = []
    chunk = []

    unseen = [x for x in knight.keys()]
    unseen.remove(i)

    for item in knight[i][0]:
        q.append(item)
        chunk.append(item)

    while q:
        ci,cj = q.pop(0)
        ni,nj = ci+di[d],cj+dj[d]
        if 0<=ni<L and 0<=nj<L:
            if (ni,nj) in wall: # 벽인 경우 -> 이동 불가
                return []
            elif arr[ni][nj] in unseen: # 다른 기사에 있는 경우 -> 다른 기사도 이동해줘야 함
                unseen.remove(arr[ni][nj])
                for item in knight[arr[ni][nj]][0]:
                    q.append(item)
            else: # 벽도 아니고, 다른팀도 아닐 경우
                chunk.append((ci,cj))
        else: # grid 범위 밖인 경우 -> 이동 불가
            return []

    return list(set(chunk))



# 본격 시작
for i,d in command:
    if i not in knight.keys(): # 이미 사라진 기사에게 명령을 하는 경우 무반응
        continue

    # 한꺼번에 움직일 무브먼트 덩어리 구하기
    chunk = move_targets(i,d)

    # 본격 움직임 (knight 업데이트)
    if len(chunk) > 0:
        narr = [[-1] * L for _ in range(L)]

        for (ci,cj) in chunk:
            ni,nj = ci+di[d],cj+dj[d]
            knight_idx = arr[ci][cj]

            knight[knight_idx][0].remove((ci,cj))
            knight[knight_idx][0].append((ni,nj))

            if (ni,nj) in trap and knight_idx != i:
                knight[knight_idx][1] -= 1 # 체력
                knight[knight_idx][2] += 1 # 대미지

        # 체력이 소진되어 사라지는 기사들 처리
        new_knight = dict()
        for knight_idx in knight.keys():
            if knight[knight_idx][1] > 0:
                lst, _, _ = knight[knight_idx]
                new_knight[knight_idx] = knight[knight_idx]
                for (a,b) in lst:
                    narr[a][b] = knight_idx

        knight = new_knight
        arr = narr

ans = 0
for item in knight.values():
    ans += item[-1]
print(ans)