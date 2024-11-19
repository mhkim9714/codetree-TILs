n, k = map(int, input().split())
arr = [[0 for _ in range(n)] for _ in range(n)]
tmp = list(map(int, input().split()))
for j in range(n):
    arr[n-1][j] = tmp[j]

cnt = 1
while True:
    # 1. 밀가루 양이 가장 작은 위치에 밀가루 1만큼 더 넣어줌 (가장 작은 위치가 여러개라면 모두 넣기)  [ 10^2 ]
    min_val = 5000
    for j in range(n):
        if arr[n-1][j] < min_val:
            min_val = arr[n-1][j]
    for j in range(n):
        if arr[n-1][j] == min_val:
            arr[n-1][j] += 1

    # 2. 도우를 말아줌
    sj, block_i, block_j, i_add = 0, 1, 1, True
    while True:
        if n-(sj+block_j) < block_i:
            break

        row_idx = n-1
        for j in range(sj+block_j-1, sj-1, -1):
            row_idx -= 1
            col_idx = sj+block_j
            for i in range(n-1, n-1-block_i, -1):
                arr[row_idx][col_idx] = arr[i][j]
                arr[i][j] = 0
                col_idx += 1

        sj += block_j
        if i_add is True:
            block_i, block_j = block_i+1, block_j
            i_add = False
        else:
            block_i, block_j = block_i, block_j+1
            i_add = True

    # 3. 도우 꾹 누르기
    # 3-1. 상하좌우 인접 밀가루 양 조절
    narr = [x[:] for x in arr]
    for i in range(n):
        for j in range(n):
            if arr[i][j] == 0:
                continue

            delta = 0
            for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
                ni,nj = i+di, j+dj
                if 0<=ni<n and 0<=nj<n and arr[ni][nj]!=0:
                    d = abs(arr[ni][nj] - arr[i][j]) // 5
                    if arr[i][j] >= arr[ni][nj]:
                        delta -= d
                    else:
                        delta += d

            narr[i][j] += delta

    # 3-2. 도우를 1자 모양으로 쭉 펴기
    arr = [[0 for _ in range(n)] for _ in range(n)]
    sj = 0
    for j in range(n):
        if narr[n-1][j] == 0:
            continue
        for i in range(n-1,-1,-1):
            if narr[i][j] > 0:
                arr[n-1][sj] = narr[i][j]
                sj += 1

    # 4. 도우를 두 번 반으로 접어주기
    sj, block_i, block_j = 0, 1, n//2
    for _ in range(2):
        row_idx = n - block_i
        for i in range(n-block_i, n, 1):
            row_idx -= 1
            col_idx = sj + block_j
            for j in range(sj+block_j-1, sj-1, -1):
                arr[row_idx][col_idx] = arr[i][j]
                arr[i][j] = 0
                col_idx += 1

        sj += block_j
        block_i *= 2
        block_j = block_j // 2

    # 5. 3의 과정 한번 더 반복
    # 3-1. 상하좌우 인접 밀가루 양 조절
    narr = [x[:] for x in arr]
    for i in range(n):
        for j in range(n):
            if arr[i][j] == 0:
                continue

            delta = 0
            for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < n and arr[ni][nj] != 0:
                    d = abs(arr[ni][nj] - arr[i][j]) // 5
                    if arr[i][j] >= arr[ni][nj]:
                        delta -= d
                    else:
                        delta += d

            narr[i][j] += delta

    # 3-2. 도우를 1자 모양으로 쭉 펴기
    arr = [[0 for _ in range(n)] for _ in range(n)]
    sj = 0
    for j in range(n):
        if narr[n - 1][j] == 0:
            continue
        for i in range(n - 1, -1, -1):
            if narr[i][j] > 0:
                arr[n - 1][sj] = narr[i][j]
                sj += 1

    # 6. 현재 턴의 최댓값, 최솟값 차이 계산하고, 그만둘건지 or 계속할건지 정하기
    min_val = 5000
    max_val = 0
    for j in range(n):
        if arr[n - 1][j] < min_val:
            min_val = arr[n - 1][j]
        if arr[n - 1][j] > max_val:
            max_val = arr[n - 1][j]

    if max_val - min_val <= k:
        print(cnt)
        break
    else:
        cnt += 1

