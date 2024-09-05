from collections import deque

n,m,k = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(n)]

start_idx = 5
team = dict()
for i in range(n):
    for j in range(n):
        if arr[i][j] == 1:
            q = []
            visited = [[0 for _ in range(n)] for _ in range(n)]
            dq = deque()

            q.append((i,j))
            visited[i][j] = 1
            dq.append((i,j))

            while q:
                ci,cj = q.pop(0)
                for di,dj in ((-1,0),(0,1),(1,0),(0,-1)):
                    ni,nj = ci+di,cj+dj
                    if 0<=ni<n and 0<=nj<n and visited[ni][nj]==0 and 1<=arr[ni][nj]<=3:
                        if not (arr[ci][cj]==1 and arr[ni][nj]==3):
                            q.append((ni,nj))
                            visited[ni][nj] = 1
                            dq.append((ni,nj))

            team[start_idx] = dq
            start_idx += 1

for idx, dq in team.items():
    for i,j in dq:
        arr[i][j] = idx


def throwing(round):
    if 0 <= round < n:
        start = (round, 0)
        dir = (0, 1)
    elif n <= round < 2*n:
        start = (n-1, round-n)
        dir = (-1, 0)
    elif 2*n <= round < 3*n:
        start = ((n-1)-(round-2*n), n-1)
        dir = (0, -1)
    else:
        start = (0, (n-1)-(round-3*n))
        dir = (1, 0)
    return start, dir


score = 0
for rnd in range(k):
    # 각 팀은 머리사람을 따라서 한칸 전진
    for idx, dq in team.items():
        ei,ej = dq.pop()
        arr[ei][ej] = 4
        si,sj = dq[0]
        for di,dj in ((-1,0),(0,1),(1,0),(0,-1)):
            nsi,nsj = si+di,sj+dj
            if 0<=nsi<n and 0<=nsj<n and arr[nsi][nsj]==4:
                dq.appendleft((nsi,nsj))
                arr[nsi][nsj] = idx
                break

    # 공 던지기
    start, direction = throwing(rnd % (4*n))
    bi,bj = start

    while True:
        if 0<=bi<n and 0<=bj<n:
            # 해당 선에 사람이 있는 경우
            if arr[bi][bj] > 4:
                cnt = team[arr[bi][bj]].index((bi,bj))
                score += (cnt+1)**2
                team[arr[bi][bj]].reverse()
                break

            else:
                bi,bj = bi+direction[0], bj+direction[1]

        else:
            break

print(score)