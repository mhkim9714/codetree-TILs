import copy

n,k = map(int, input().split())

tmp = list(map(int, input().split()))
arr = [[0 for _ in range(n)] for _ in range(n)]
for j in range(n):
    arr[-1][j] = tmp[j]


def rotate_90(lst):
    width = len(lst[0])
    height = len(lst)

    rotated_lst = [[0 for _ in range(height)] for _ in range(width)]
    for i in range(width):
        for j in range(height):
            rotated_lst[i][j] = lst[height-1-j][i]
    return rotated_lst


t = 0
while True:
    t += 1

    # 1) 밀가루 양이 가장 작은 위치에 밀가루 1만큼 더 넣기
    min_val = min(arr[-1][:])
    for j in range(n):
        if arr[-1][j] == min_val:
            arr[-1][j] += 1

    # 2) 도우 말기
    w, h = 1, 1
    cur_j = 0
    flag = 0

    while True:
        if h > n-(cur_j+w):
            break

        box = [[0 for _ in range(w)] for _ in range(h)]
        for i in range(h):
            for j in range(w):
                box[i][j] = arr[n-h+i][cur_j+j]
                arr[n-h+i][cur_j+j] = 0

        rotated_box = rotate_90(box)

        for i in range(w):
            for j in range(h):
                arr[n-1-w+i][cur_j+w+j] = rotated_box[i][j]

        cur_j += w
        if flag == 0:
            flag = 1
            h += 1
        else:
            flag = 0
            w += 1

    # 3-1) 도우 꾹 누르기
    narr = copy.deepcopy(arr)
    adj = [[[] for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if arr[i][j] <= 0:
                continue
            for di,dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                ni,nj = i+di,j+dj
                if 0<=ni<n and 0<=nj<n and arr[ni][nj]>0 and (ni,nj) not in adj[i][j]:
                    d = abs(arr[i][j]-arr[ni][nj])//5
                    if d == 0:
                        continue
                    if arr[i][j] > arr[ni][nj]:
                        narr[i][j] -= d
                        narr[ni][nj] += d
                    else:
                        narr[i][j] += d
                        narr[ni][nj] -= d
                    adj[i][j].append((ni,nj))
                    adj[ni][nj].append((i,j))
    arr = narr

    # 3-2) 도우 1차원으로 다시 펴기
    tmp = list()
    for j in range(n):
        if arr[-1][j] <= 0:
            continue
        for i in range(n-1,-1,-1):
            if arr[i][j] > 0:
                tmp.append(arr[i][j])
            else:
                break
    arr = [[0 for _ in range(n)] for _ in range(n)]
    for j in range(n):
        arr[-1][j] = tmp[j]

    # 4) 도우를 두번 반으로 접기
    for w,h,cur_j,cnt in [(n//2,1,0,1),(n//4,2,n//2,2)]:
        box = [[0 for _ in range(w)] for _ in range(h)]
        for i in range(h):
            for j in range(w):
                box[i][j] = arr[n-h+i][cur_j+j]
                arr[n-h+i][cur_j+j] = 0

        rotated_box = rotate_90(rotate_90(box))

        for i in range(h):
            for j in range(w):
                arr[n-cnt-h+i][cur_j+w+j] = rotated_box[i][j]

    # 5) 3의 과정 한번 더 반복
    # 3-1) 도우 꾹 누르기
    narr = copy.deepcopy(arr)
    adj = [[[] for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if arr[i][j] <= 0:
                continue
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < n and arr[ni][nj] > 0 and (ni, nj) not in adj[i][j]:
                    d = abs(arr[i][j] - arr[ni][nj]) // 5
                    if d == 0:
                        continue
                    if arr[i][j] > arr[ni][nj]:
                        narr[i][j] -= d
                        narr[ni][nj] += d
                    else:
                        narr[i][j] += d
                        narr[ni][nj] -= d
                    adj[i][j].append((ni, nj))
                    adj[ni][nj].append((i, j))
    arr = narr

    # 3-2) 도우 1차원으로 다시 펴기
    tmp = list()
    for j in range(n):
        if arr[-1][j] <= 0:
            continue
        for i in range(n - 1, -1, -1):
            if arr[i][j] > 0:
                tmp.append(arr[i][j])
            else:
                break
    arr = [[0 for _ in range(n)] for _ in range(n)]
    for j in range(n):
        arr[-1][j] = tmp[j]

    if max(tmp) - min(tmp) <= k:
        print(t)
        break