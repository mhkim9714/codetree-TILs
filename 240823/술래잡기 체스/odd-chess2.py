import copy

# ↑0, ↖1, ←2, ↙3, ↓4, ↘5, →6, ↗7
di = [-1,-1,0,1,1,1,0,-1]
dj = [0,-1,-1,-1,0,1,1,1]

# 도둑말
player = dict()
arr = [[0 for _ in range(4)] for _ in range(4)]
for i in range(4):
    lst = list(map(int, input().split()))

    player[lst[0]] = [(i,0), lst[1]-1]
    arr[i][0] = lst[0]

    player[lst[2]] = [(i,1), lst[3]-1]
    arr[i][1] = lst[2]

    player[lst[4]] = [(i,2), lst[5]-1]
    arr[i][2] = lst[4]

    player[lst[6]] = [(i,3), lst[7]-1]
    arr[i][3] = lst[6]
player = dict(sorted(player.items()))

# 술래말
Ti,Tj = 0,0

scores = []
q = []

# 초기 인풋 만들어 주기
Td = player[arr[Ti][Tj]][1]
del player[arr[Ti][Tj]]
score = arr[Ti][Tj]
arr[Ti][Tj] = -1

q.append((player, arr, Ti, Tj, Td, score))

while q:
    p, a, ti, tj, td, s = q.pop(0)

    # 술래말 이동 가능 조건 확인
    nti, ntj = ti+di[td], tj+dj[td]
    next_tag = []
    while True:
        if 0<=nti<4 and 0<=ntj<4:
            if arr[nti][ntj] != 0:
                next_tag.append((nti,ntj))
            nti, ntj = nti+di[td], ntj+dj[td]
        else:
            break
    if len(next_tag) == 0:
        scores.append(s)
        continue
    
    # 도둑말 순서대로 이동
    for idx, info in p.items():
        ci,cj,nd = info[0][0], info[0][1], info[1]
        for _ in range(8):
            ni,nj = ci+di[nd], cj+dj[nd]
            if not (0<=ni<4 and 0<=nj<4 and a[ni][nj]>=0):
                nd = (nd+1)%8
            else: # 이동 가능
                if a[ni][nj] == 0: # 빈칸
                    info[0] = (ni,nj)
                    info[1] = nd
                    a[ci][cj] = 0
                    a[ni][nj] = idx
                else:
                    info[0] = (ni,nj)
                    info[1] = nd
                    p[a[ni][nj]] = [(ci,cj), p[a[ni][nj]][1]]
                    a[ci][cj] = a[ni][nj]
                    a[ni][nj] = idx
                break

    # 술래 이동 후 q에 append
    a[ti][tj] = 0
    for nti,ntj in next_tag:
        np = copy.deepcopy(p)
        na = [x[:] for x in a]
        ntd = np[na[nti][ntj]][1]
        del np[na[nti][ntj]]
        ns = s + na[nti][ntj]
        na[ntj][ntj] = -1

        q.append((np, na, nti, ntj, ntd, ns))

print(max(scores))