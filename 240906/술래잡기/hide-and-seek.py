n,m,h,k = map(int, input().split())

arr = [[[] for _ in range(n)] for _ in range(n)]
player = dict()
for idx in range(1,m+1):
    x,y,d = map(int, input().split())
    if d == 1:
        player[idx] = [(x-1,y-1),1]
    else:
        player[idx] = [(x-1,y-1),2]
    arr[x-1][y-1].append(idx)

tree = []
for _ in range(h):
    x,y = map(int, input().split())
    tree.append((x-1,y-1))

Ti,Tj,Td = (n-1)//2, (n-1)//2, 0
target = 1
current = 0
cnt = 0
clockwise = 1 # 1:시계 / 0:반시계

# 상0 우1 하2 좌3
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]


def distance(si,sj,ei,ej):
    return abs(si-ei) + abs(sj-ej)


score = 0
for turn in range(k):
    # 도망자 동시에 이동
    for idx, info in player.items():
        if distance(Ti,Tj,info[0][0],info[0][1]) <= 3:
            ni,nj = info[0][0]+di[info[1]], info[0][1]+dj[info[1]]
            if 0<=ni<n and 0<=nj<n:
                if (ni,nj) != (Ti,Tj):
                    arr[info[0][0]][info[0][1]].remove(idx)
                    arr[ni][nj].append(idx)
                    info[0] = (ni,nj)
            else:
                info[1] = (info[1]+2)%4
                ni,nj = info[0][0]+di[info[1]], info[0][1]+dj[info[1]]
                if (ni,nj) != (Ti,Tj):
                    arr[info[0][0]][info[0][1]].remove(idx)
                    arr[ni][nj].append(idx)
                    info[0] = (ni,nj)

    # 술래 이동
    Ti,Tj = Ti+di[Td], Tj+dj[Td]
    current += 1

    if target == current:
        cnt += 1

        if cnt==2 and target<n-1:
            if clockwise == 1:
                Td = (Td+1)%4
                current = 0
                target += 1
                cnt = 0
            else:
                if (Ti,Tj) == ((n-1)//2, (n-1)//2):
                    Td = (Td+2)%4
                    current = 0
                    cnt = 0
                    clockwise = 1
                else:
                    Td = (Td+3)%4
                    current = 0
                    target -= 1
                    cnt = 0

        elif cnt==3 and target==n-1:
            if clockwise == 1:
                Td = (Td+2)%4
                current = 0
                cnt = 0
                clockwise = 0
            else:
                Td = (Td+3)%4
                current = 0
                target -= 1
                cnt = 0

        else:
            if clockwise == 1:
                Td = (Td+1)%4
                current = 0
            else:
                Td = (Td+3)%4
                current = 0

    # 술래잡기
    for v in range(3):
        vi,vj = Ti+v*di[Td], Tj+v*dj[Td]

        if 0<=vi<n and 0<=vj<n:
            if (vi,vj) not in tree:
                if len(arr[vi][vj]) > 0:
                    score += (turn+1) * len(arr[vi][vj])
                    for idx in arr[vi][vj]:
                        del player[idx]
                    arr[vi][vj] = []

    # 종료조건
    if len(player) == 0:
        break

print(score)