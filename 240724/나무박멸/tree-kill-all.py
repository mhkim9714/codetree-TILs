n,m,k,c = map(int, input().split())
arr = []
for _ in range(n):
    arr.append(list(map(int, input().split())))
for i in range(n):
    for j in range(n):
        if arr[i][j] == -1:
            arr[i][j] = -10000

# 상하좌우 방향
di = [-1, 1, 0, 0]
dj = [0, 0, -1, 1]

# 대각선 방향
ddi = [-1, 1, 1, -1]
ddj = [1, 1, -1, -1]

ans = 0
for _ in range(m):
    # 성장: 동시에
    narr = [x[:] for x in arr]
    for i in range(n):
        for j in range(n):
            if arr[i][j]>0:
                cnt = 0
                for a in range(4):
                    ni = i+di[a]
                    nj = j+dj[a]
                    if 0<=ni<n and 0<=nj<n and arr[ni][nj]>0:
                        cnt += 1
                narr[i][j] += cnt
    arr = [x[:] for x in narr]

    # 번식: 동시에
    narr = [x[:] for x in arr]
    for i in range(n):
        for j in range(n):
            if arr[i][j]>0:
                cnt = 0
                ti = []
                tj = []
                for a in range(4):
                    ni = i+di[a]
                    nj = j+dj[a]
                    if 0<=ni<n and 0<=nj<n and arr[ni][nj]==0:
                        ti.append(ni)
                        tj.append(nj)
                        cnt += 1
                for a in range(len(ti)):
                    narr[ti[a]][tj[a]] += (arr[i][j]//cnt)
    arr = [x[:] for x in narr]

    # 제초제를 뿌릴 위치 선정
    max = -1
    max_i = -1
    max_j = -1
    for i in range(n-1,-1,-1):
        for j in range(n-1,-1,-1):
            if arr[i][j]>0:
                cnt = arr[i][j]
                for a in range(4):
                    for b in range(1,k+1):
                        ni = i+b*ddi[a]
                        nj = j+b*ddj[a]
                        if 0<=ni<n and 0<=nj<n and arr[ni][nj]>0:
                            cnt += arr[ni][nj]
                            continue
                        else:
                            break
                if cnt >= max:
                    max = cnt
                    max_i = i
                    max_j = j

    # 제초제 뿌리기 + ans 더하기
    ans += max
    arr[max_i][max_j] = -1*(c+1)
    for a in range(4):
        for b in range(1,k+1):
            ni = max_i+b*ddi[a]
            nj = max_j+b*ddj[a]
            if 0<=ni<n and 0<=nj<n and arr[ni][nj]>0: # 칸 안 & 나무 있는 경우 -> 제초제O, 전파O
                arr[ni][nj] = -1*(c+1)
                continue
            elif 0<=ni<n and 0<=nj<n and arr[ni][nj]<=0 and arr[ni][nj]>-100: # 칸 안 & 나무 없는 경우 -> 제초제O, 전파X
                arr[ni][nj] = -1*(c+1)
                break
            else: # 칸 밖
                break

    # 음수 조정 (1년 has passed)
    for i in range(n):
        for j in range(n):
            if arr[i][j] < 0:
                arr[i][j] += 1

print(ans)