R,C,K = map(int, input().split())

arr = [[0 for _ in range(C)] for _ in range(R+3)]
monster = dict()

# 상0 우1 하2 좌3
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

ans = 0
for idx in range(1,K+1):
    j,d = map(int, input().split())
    i,j = 1, j-1

    # 가능한 한 아래로 이동
    restart_flag = 0
    while True:
        if 0<=i+2<R+3 and arr[i+1][j-1]==0 and arr[i+2][j]==0 and arr[i+1][j+1]==0:
            i,j = i+1,j
        elif 0<=i+2<R+3 and 0<=j-2<C and arr[i-1][j-1]==0 and arr[i][j-2]==0 and \
            arr[i+1][j-2]==0 and arr[i+1][j-1]==0 and arr[i+2][j-1]==0:
            i,j = i+1,j-1
            d = (d+3)%4
        elif 0<=i+2<R+3 and 0<=j+2<C and arr[i-1][j+1]==0 and arr[i][j+2]==0 and \
            arr[i+1][j+1]==0 and arr[i+1][j+2]==0 and arr[i+2][j+1]==0:
            i,j = i+1,j+1
            d = (d+5)%4
        else:
            if 0<=i<=3:
                arr = [[0 for _ in range(C)] for _ in range(R+3)]
                monster = dict()
                restart_flag = 1
            else:
                arr[i][j] = idx
                for ddi,ddj in ((-1,0),(0,1),(1,0),(0,-1)):
                    arr[i+ddi][j+ddj] = idx
                monster[idx] = [(i,j), d]
            break
    if restart_flag == 1:
        continue

    # 정령 이동
    max_i = i+1
    q = [(i+di[d], j+dj[d])]
    visited = [idx]

    while q:
        ci,cj = q.pop(0)
        for ddi,ddj in ((-1,0),(0,1),(1,0),(0,-1)):
            ni,nj = ci+ddi,cj+ddj
            if 0<=ni<R+3 and 0<=nj<C and arr[ni][nj]!=0 and arr[ni][nj] not in visited:
                nm_i = monster[arr[ni][nj]][0][0]
                nm_j = monster[arr[ni][nj]][0][1]
                nm_d = monster[arr[ni][nj]][1]

                if max_i < nm_i+1:
                    max_i = nm_i+1
                q.append((nm_i+di[nm_d], nm_j+dj[nm_d]))
                visited.append(arr[ni][nj])

    ans += (max_i - 2)

print(ans)