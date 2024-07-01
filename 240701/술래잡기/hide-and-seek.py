import sys
sys.stdin = open('input.txt', 'r')

n,m,h,k = map(int, input().split())

# 방향
dx = [-1,0,1,0]
dy = [0,1,0,-1]

# 술래
sx = sy = int((n-1)/2)
sd = 0
delta = 1

# 술래 reserved
arr = [[-1 for _ in range(n)] for _ in range(n)]
reserved = []
step = 1
cx,cy = sx,sy
arr[cx][cy] = 0
reserved.append((cx,cy))
while True:
    if step < n-1:
        for _ in range(2):
            nx = cx+step*dx[arr[cx][cy]]
            ny = cy+step*dy[arr[cx][cy]]
            reserved.append((nx,ny))
            arr[nx][ny] = (arr[cx][cy]+1)%4
            cx,cy = nx,ny
        step += 1
    else:
        for _ in range(3):
            nx = cx+step*dx[arr[cx][cy]]
            ny = cy+step*dy[arr[cx][cy]]
            reserved.append((nx,ny))
            arr[nx][ny] = (arr[cx][cy]+1) % 4
            cx,cy = nx,ny
    if (cx,cy) == (0,0):
        break

# 도망자
runner = []
for _ in range(m):
    x,y,d = map(int, input().split())
    if d == 1:
        runner.append((x-1,y-1,1))
    elif d == 2:
        runner.append((x-1,y-1,2))

# 나무
tree = []
for _ in range(h):
    hx,hy = map(int, input().split())
    tree.append((hx-1,hy-1))

def distance(x1,y1,x2,y2):
    return abs(x1-x2) + abs(y1-y2)

# 메인
score = 0
for rnd in range(k):
    if len(runner) == 0:
        break

    # 도망자 이동
    new_runner = [x[:] for x in runner]
    for i,(rx,ry,rd) in enumerate(runner):
        if distance(rx,ry,sx,sy) <= 3:
            nx = rx + dx[rd]
            ny = ry + dy[rd]
            if 0<=nx<n and 0<=ny<n: # 격자 내
                if (nx,ny)!=(sx,sy):
                    new_runner[i] = (nx,ny,rd)
            else: # 격자 밖
                nd = (rd+2)%4
                nx = rx + dx[nd]
                ny = ry + dy[nd]
                if (nx, ny) != (sx, sy):
                    new_runner[i] = (nx,ny,nd)

    runner = new_runner

    # 술래 이동
    sx = sx + dx[sd]
    sy = sy + dy[sd]
    if (sx,sy) == (0,0):
        delta = -1
        sd = 2
    elif (sx,sy) == (int((n-1)/2),int((n-1)/2)):
        delta = 1
        sd = 0
    elif (sx,sy) in reserved:
        sd = (sd+delta)%4

    # 술래 잡기
    px,py = sx,sy
    cnt = 0
    rmv_idx = []
    for _ in range(3):
        if 0<=px<n and 0<=py<n:
            for i,(rx,ry,rd) in enumerate(runner):
                if (px,py) == (rx,ry) and (px,py) not in tree:
                    rmv_idx.append(i)
                    cnt += 1
            px = px + dx[sd]
            py = py + dy[sd]

    for i in rmv_idx[::-1]:
        runner.pop(i)

    score += (rnd+1)*cnt

print(score)