n,m,h,k = map(int, input().split())

player = dict()
arr = [[[] for _ in range(n)] for _ in range(n)]
for idx in range(1,m+1):
    x,y,d = map(int, input().split())
    if d == 1:
        player[idx] = [(x-1,y-1),1]
    elif d == 2:
        player[idx] = [(x-1,y-1),2]
    arr[x-1][y-1].append(idx)

tree = []
for _ in range(h):
    x,y = map(int, input().split())
    tree.append((x-1,y-1))

# 상0 우1 하2 좌3
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

Ti,Tj,Td = n//2, n//2, 0
mx_cnt, cnt, flag, val = 1,0,0,1

def distance(si,sj,ei,ej):
    return abs(si-ei) + abs(sj-ej)

ans = 0
for t in range(1,k+1):
    # 도망자 이동
    for idx, info in player.items():
        if distance(info[0][0], info[0][1], Ti, Tj) <= 3:
            ni,nj = info[0][0]+di[info[1]], info[0][1]+dj[info[1]]
            if 0<=ni<n and 0<=nj<n:
                if (ni,nj) != (Ti,Tj):
                    arr[info[0][0]][info[0][1]].remove(idx)
                    info[0] = (ni,nj)
                    arr[info[0][0]][info[0][1]].append(idx)
            else:
                info[1] = (info[1]+2)%4
                ni,nj = info[0][0]+di[info[1]], info[0][1]+dj[info[1]]
                if (ni,nj) != (Ti,Tj):
                    arr[info[0][0]][info[0][1]].remove(idx)
                    info[0] = (ni,nj)
                    arr[info[0][0]][info[0][1]].append(idx)

    # 술래 이동
    Ti,Tj = Ti+di[Td], Tj+dj[Td]
    cnt += 1

    if (Ti,Tj) == (n//2,n//2):
        Td = (Td+2)%4
        mx_cnt, cnt, flag, val = 1,0,0,1
    elif (Ti,Tj) == (0,0):
        Td = (Td+2)%4
        mx_cnt, cnt, flag, val = n,1,1,-1
    elif mx_cnt == cnt:
        Td = (Td+val)%4
        cnt = 0
        if flag == 0:
            flag = 1
        else:
            mx_cnt += val
            flag = 0

    # 술래 잡기
    caught = 0
    for delta in range(3):
        i,j = Ti+delta*di[Td], Tj+delta*dj[Td]
        if 0<=i<n and 0<=j<n:
            if (i,j) not in tree:
                if len(arr[i][j]) != 0:
                    caught += len(arr[i][j])
                    for idx in arr[i][j]:
                        del player[idx]
                    arr[i][j] = []
        else:
            break
    ans += (t*caught)

    # 종료 조건
    if len(player) == 0:
        break

print(ans)