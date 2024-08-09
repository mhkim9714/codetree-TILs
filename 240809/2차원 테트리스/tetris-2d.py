k = int(input())

red = [[0 for _ in range(6)] for _ in range(4)]
yellow = [[0 for _ in range(4)] for _ in range(6)]

score = 0
for _ in range(k):
    t,x,y = map(int, input().split())

    # 블럭 놓기
    if t == 1:
        final_j = 0
        for j in range(6):
            if red[x][j] == 0:
                final_j = j
            else:
                break
        red[x][final_j] = 1
        final_i = 0
        for i in range(6):
            if yellow[i][y] == 0:
                final_i = i
            else:
                break
        yellow[final_i][y] = 1
    elif t == 2:
        final_j = 0
        for j in range(1,6):
            if red[x][j] == 0 and red[x][j-1] == 0:
                final_j = j
            else:
                break
        red[x][final_j], red[x][final_j-1] = 1, 1
        final_i = 0
        for i in range(6):
            if yellow[i][y] == 0 and yellow[i][y+1] == 0:
                final_i = i
            else:
                break
        yellow[final_i][y], yellow[final_i][y+1] = 1, 1
    else:
        final_j = 0
        for j in range(6):
            if red[x][j] == 0 and red[x+1][j] == 0:
                final_j = j
            else:
                break
        red[x][final_j], red[x+1][final_j] = 1, 1
        final_i = 0
        for i in range(1,6):
            if yellow[i][y] == 0 and yellow[i-1][y] == 0:
                final_i = i
            else:
                break
        yellow[final_i][y], yellow[final_i-1][y] = 1, 1

    # 꽉 채워진 행/열 처리 및 score 누적
    col_reversed = []
    for j in range(5,-1,-1):
        if red[0][j]*red[1][j]*red[2][j]*red[3][j] == 1:
            score += 1
            continue
        else:
            col_reversed.append([red[0][j],red[1][j],red[2][j],red[3][j]])
    if len(col_reversed) < 6:
        for _ in range(6-len(col_reversed)):
            col_reversed.append([0,0,0,0])
        new_red = [[0 for _ in range(6)] for _ in range(4)]
        for i in range(4):
            for j in range(6):
                new_red[i][j] = col_reversed[5-j][i]
        red = new_red

    row_reversed = []
    for i in range(5,-1,-1):
        if yellow[i][0]*yellow[i][1]*yellow[i][2]*yellow[i][3] == 1:
            score += 1
            continue
        else:
            row_reversed.append([yellow[i][0],yellow[i][1],yellow[i][2],yellow[i][3]])
    if len(row_reversed) < 6:
        for _ in range(6-len(row_reversed)):
            row_reversed.append([0,0,0,0])
        new_yellow = [[0 for _ in range(4)] for _ in range(6)]
        for i in range(6):
            for j in range(4):
                new_yellow[i][j] = row_reversed[5-i][j]
        yellow = new_yellow

    # 연한 색 구역에 놓여 있는 블럭 처리
    col_line = 0
    for j in (0,1):
        if red[0][j]+red[1][j]+red[2][j]+red[3][j] > 0:
            col_line += 1
    if col_line > 0:
        col_reversed = []
        for j in range(5-col_line,-1,-1):
            col_reversed.append([red[0][j],red[1][j],red[2][j],red[3][j]])
        for _ in range(col_line):
            col_reversed.append([0,0,0,0])
        new_red = [[0 for _ in range(6)] for _ in range(4)]
        for i in range(4):
            for j in range(6):
                new_red[i][j] = col_reversed[5 - j][i]
        red = new_red

    row_line = 0
    for i in (0,1):
        if yellow[i][0]+yellow[i][1]+yellow[i][2]+yellow[i][3] > 0:
            row_line += 1
    if row_line > 0:
        row_reversed = []
        for i in range(5-row_line,-1,-1):
            row_reversed.append([yellow[i][0],yellow[i][1],yellow[i][2],yellow[i][3]])
        for _ in range(row_line):
            row_reversed.append([0,0,0,0])
        new_yellow = [[0 for _ in range(4)] for _ in range(6)]
        for i in range(6):
            for j in range(4):
                new_yellow[i][j] = row_reversed[5 - i][j]
        yellow = new_yellow

print(score)
cnt = 0
for i in range(4):
    for j in range(6):
        if red[i][j] == 1:
            cnt += 1
for i in range(6):
    for j in range(4):
        if yellow[i][j] == 1:
            cnt += 1
print(cnt)