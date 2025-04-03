k = int(input())
arr = [[0 for _ in range(10)] for _ in range(10)]  # 0:빈칸, 1:타일

score = 0
for _ in range(k):
    t, ori_i, ori_j = map(int, input().split())

    # 빨간색 블록으로 이동 처리
    if t == 1:  # 하나
        for nj in range(4, 9):
            if arr[ori_i][nj+1] == 1:
                arr[ori_i][nj] = 1
                break
        else:
            arr[ori_i][9] = 1
    elif t == 2:  # 가로
        for nj in range(5, 9):
            if arr[ori_i][nj+1] == 1:
                arr[ori_i][nj] = 1
                arr[ori_i][nj-1] = 1
                break
        else:
            arr[ori_i][9] = 1
            arr[ori_i][8] = 1
    else:  # 세로
        for nj in range(4, 9):
            if arr[ori_i][nj+1] == 1 or arr[ori_i+1][nj+1] == 1:
                arr[ori_i][nj] = 1
                arr[ori_i+1][nj] = 1
                break
        else:
            arr[ori_i][9] = 1
            arr[ori_i+1][9] = 1

    # 진한 빨간 영역 처리
    red = [[0 for _ in range(6)] for _ in range(4)]
    last_j = 6 - 1
    for j in range(9, 3, -1):
        if arr[0][j]==1 and arr[1][j]==1 and arr[2][j]==1 and arr[3][j]==1:
            score += 1
            continue
        else:
            for i in range(4):
                red[i][last_j] = arr[i][j]
            last_j -= 1

    # 연한 빨간 영역 처리
    cnt = 0
    for j in range(2):
        if red[0][j]==1 or red[1][j]==1 or red[2][j]==1 or red[3][j]==1:
            cnt += 1

    if cnt > 0:
        for i in range(4):
            red[i] = [0 for _ in range(cnt)] + red[i][:-cnt]

    for i in range(4):
        for j in range(4,10):
            arr[i][j] = red[i][j-4]

    # 노란색 블록으로 이동 처리
    if t == 1:  # 하나
        for ni in range(4, 9):
            if arr[ni+1][ori_j] == 1:
                arr[ni][ori_j] = 1
                break
        else:
            arr[9][ori_j] = 1
    elif t == 2:  # 가로
        for ni in range(4, 9):
            if arr[ni+1][ori_j] == 1 or arr[ni+1][ori_j+1] == 1:
                arr[ni][ori_j] = 1
                arr[ni][ori_j+1] = 1
                break
        else:
            arr[9][ori_j] = 1
            arr[9][ori_j+1] = 1
    else:  # 세로
        for ni in range(5, 9):
            if arr[ni+1][ori_j] == 1:
                arr[ni][ori_j] = 1
                arr[ni-1][ori_j] = 1
                break
        else:
            arr[9][ori_j] = 1
            arr[8][ori_j] = 1

    # 진한 노란 영역 처리
    yellow = [[0 for _ in range(4)] for _ in range(6)]
    last_i = 6 - 1
    for i in range(9, 3, -1):
        if arr[i][0]==1 and arr[i][1]==1 and arr[i][2]==1 and arr[i][3]==1:
            score += 1
            continue
        else:
            for j in range(4):
                yellow[last_i][j] = arr[i][j]
            last_i -= 1

    # 연한 노란 영역 처리
    cnt = 0
    for i in range(2):
        if yellow[i][0]==1 or yellow[i][1]==1 or yellow[i][2]==1 or yellow[i][3]==1:
            cnt += 1

    if cnt > 0:
        yellow = [[0 for _ in range(4)] for _ in range(cnt)] + yellow[:-cnt]

    for i in range(4, 10):
        for j in range(4):
            arr[i][j] = yellow[i-4][j]


print(score)
cnt_red = 0
for i in range(4):
    for j in range(6, 10):
        if arr[i][j] == 1:
            cnt_red += 1
cnt_yellow = 0
for i in range(6, 10):
    for j in range(4):
        if arr[i][j] == 1:
            cnt_yellow += 1
print(cnt_yellow + cnt_red)
