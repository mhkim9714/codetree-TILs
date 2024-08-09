# ↑(0) ↖(1) ←(2) ↙(3) ↓(4) ↘(5) →(6) ↗(7)
di = [-1, -1, 0, 1, 1, 1, 0, -1]
dj = [0, -1, -1, -1, 0, 1, 1, 1]

init_arr = [[[0,-1] for _ in range(4)] for _ in range(4)]
for i in range(4):
    lst = list(map(int, input().split()))
    init_arr[i][0] = [lst[0],lst[1]-1]
    init_arr[i][1] = [lst[2],lst[3]-1]
    init_arr[i][2] = [lst[4],lst[5]-1]
    init_arr[i][3] = [lst[6],lst[7]-1]


def move(arr):
    # 모든 도둑말의 위치 파악해두기
    location = dict()
    for i in range(4):
        for j in range(4):
            if arr[i][j][0] > 0:
                location[arr[i][j][0]] = (i,j)
    location = dict(sorted(location.items()))

    for idx, (i,j) in location.items():
        d = arr[i][j][1]
        while True:
            ni,nj = i+di[d],j+dj[d]
            if 0<=ni<4 and 0<=nj<4 and arr[ni][nj][0]>=0:
                break
            else:
                d = (d+1)%8
        ni,nj = i+di[d],j+dj[d]
        arr[i][j][1] = d

        location[arr[i][j][0]] = (ni,nj)
        if arr[ni][nj][0] > 0:
            location[arr[ni][nj][0]] = (i,j)

        temp = arr[i][j]
        arr[i][j] = arr[ni][nj]
        arr[ni][nj] = temp

    return arr


final_score = []

score = init_arr[0][0][0]
init_arr[0][0][0] = -1

q = []
q.append((score, init_arr))

while q:
    base_score, arr = q.pop(0)
    arr = move(arr)
    
    # 현재 술래 위치,방향 찾기
    Ti,Tj,Td = -1,-1,-1
    for i in range(4):
        for j in range(4):
            if arr[i][j][0] == -1:
                Ti,Tj,Td = i,j,arr[i][j][1]

    next_Tag = []
    nTi,nTj = Ti,Tj
    while True:
        nTi,nTj = nTi+di[Td], nTj+dj[Td]
        if not (0<=nTi<4 and 0<=nTj<4):
            break
        else:
            if arr[nTi][nTj][0] > 0:
                next_Tag.append((nTi,nTj))

    if len(next_Tag) == 0:
        final_score.append(base_score)
    else:
        for nTi,nTj in next_Tag:
            new_score = base_score + arr[nTi][nTj][0]
            new_arr = [[col[:] for col in row] for row in arr]
            new_arr[Ti][Tj] = [0,-1]
            new_arr[nTi][nTj][0] = -1
            q.append((new_score, new_arr))

print(max(final_score))