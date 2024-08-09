n,m = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(n)]

# 초기 주사위
up = 1
down = 6
right = 3
left = 4
front = 2
back = 5
dci,dcj,dcd = 0,0,1 # 초기 주사위 위치, 방향

# 상(0) 우(1) 하(2) 좌(3)
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

def BFS(si,sj,val):
    q = []
    visited = [[0 for _ in range(n)] for _ in range(n)]

    q.append((si,sj))
    visited[si][sj] = 1

    cnt = 1
    while q:
        ci,cj = q.pop(0)
        for d in range(4):
            ni,nj = ci+di[d],cj+dj[d]
            if 0<=ni<n and 0<=nj<n and visited[ni][nj]==0 and arr[ni][nj]==val:
                q.append((ni,nj))
                visited[ni][nj] = 1
                cnt += 1

    return cnt


score = 0
for _ in range(m):
    # 주사위 한번 굴림 -> 주사위 6방향 업데이트 & 주사위 위치와 방향 업데이트
    if dcd == 0: # 상
        new_up = front
        new_down = back
        new_right = right
        new_left = left
        new_front = down
        new_back = up
        new_dci,new_dcj = dci+di[dcd],dcj+dj[dcd]
        if new_down > arr[new_dci][new_dcj]: # 90도 시계방향
            new_dcd = (dcd+1)%4
        elif new_down < arr[new_dci][new_dcj]: # 90도 반시계방향
            new_dcd = (dcd+3)%4
        else: # 그대로
            new_dcd = dcd
        if not(0<=new_dci+di[new_dcd]<n and 0<=new_dcj+dj[new_dcd]<n):
            new_dcd = (new_dcd+2)%4
        up,down,right,left,front,back = new_up,new_down,new_right,new_left,new_front,new_back
        dci,dcj,dcd = new_dci,new_dcj,new_dcd

    elif dcd == 1: # 우
        new_up = left
        new_down = right
        new_right = up
        new_left = down
        new_front = front
        new_back = back
        new_dci, new_dcj = dci + di[dcd], dcj + dj[dcd]
        if new_down > arr[new_dci][new_dcj]:
            new_dcd = (dcd + 1) % 4
        elif new_down < arr[new_dci][new_dcj]:
            new_dcd = (dcd + 3) % 4
        else:
            new_dcd = dcd
        if not(0<=new_dci+di[new_dcd]<n and 0<=new_dcj+dj[new_dcd]<n):
            new_dcd = (new_dcd+2)%4
        up, down, right, left, front, back = new_up, new_down, new_right, new_left, new_front, new_back
        dci, dcj, dcd = new_dci, new_dcj, new_dcd

    elif dcd == 2: # 하
        new_up = back
        new_down = front
        new_right = right
        new_left = left
        new_front = up
        new_back = down
        new_dci, new_dcj = dci + di[dcd], dcj + dj[dcd]
        if new_down > arr[new_dci][new_dcj]:
            new_dcd = (dcd + 1) % 4
        elif new_down < arr[new_dci][new_dcj]:
            new_dcd = (dcd + 3) % 4
        else:
            new_dcd = dcd
        if not(0<=new_dci+di[new_dcd]<n and 0<=new_dcj+dj[new_dcd]<n):
            new_dcd = (new_dcd+2)%4
        up, down, right, left, front, back = new_up, new_down, new_right, new_left, new_front, new_back
        dci, dcj, dcd = new_dci, new_dcj, new_dcd

    elif dcd == 3: # 좌
        new_up = right
        new_down = left
        new_right = down
        new_left = up
        new_front = front
        new_back = back
        new_dci, new_dcj = dci + di[dcd], dcj + dj[dcd]
        if new_down > arr[new_dci][new_dcj]:
            new_dcd = (dcd + 1) % 4
        elif new_down < arr[new_dci][new_dcj]:
            new_dcd = (dcd + 3) % 4
        else:
            new_dcd = dcd
        if not(0<=new_dci+di[new_dcd]<n and 0<=new_dcj+dj[new_dcd]<n):
            new_dcd = (new_dcd+2)%4
        up, down, right, left, front, back = new_up, new_down, new_right, new_left, new_front, new_back
        dci, dcj, dcd = new_dci, new_dcj, new_dcd

    # 점수 계산
    val = arr[dci][dcj]
    cnt = BFS(dci,dcj,val)
    score += (val * cnt)

print(score)