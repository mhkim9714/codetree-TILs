import copy

init_arr = [[[] for _ in range(4)] for _ in range(4)]
temp = [list(map(int, input().split())) for _ in range(4)]
for i in range(4):
    p0,d0 = temp[i][0], temp[i][1]
    p1,d1 = temp[i][2], temp[i][3]
    p2,d2 = temp[i][4], temp[i][5]
    p3,d3 = temp[i][6], temp[i][7]

    init_arr[i][0] = [p0,d0-1]
    init_arr[i][1] = [p1,d1-1]
    init_arr[i][2] = [p2,d2-1]
    init_arr[i][3] = [p3,d3-1]

di = [-1, -1, 0, 1, 1, 1, 0, -1]
dj = [0, -1, -1, -1, 0, 1, 1, 1]


final_scores = []
q = []

init_Ti, init_Tj = 0,0
init_score = init_arr[init_Ti][init_Tj][0]
init_Td = init_arr[init_Ti][init_Tj][1]
init_arr[init_Ti][init_Tj] = []

q.append((init_arr, init_score, init_Ti, init_Tj, init_Td))

while q:
    arr, score, Ti, Tj, Td = q.pop(0)

    # player dictionary 만들기
    init_player = dict()
    for i in range(4):
        for j in range(4):
            if len(arr[i][j]) > 0:
                init_player[arr[i][j][0]] = (i,j)
    player = dict(sorted(init_player.items()))

    # 도둑말 이동
    for p in list(player.keys()):
        ci,cj = player[p]
        if p != arr[ci][cj][0]:
            print("error")
            exit()
        cd = arr[ci][cj][1]

        for dd in range(8): # 0-7
            nd = (cd+dd)%8
            ni,nj = ci+di[nd], cj+dj[nd]
            if 0<=ni<4 and 0<=nj<4:
                if len(arr[ni][nj])==0 and (ni,nj)!=(Ti,Tj): # 빈칸으로 이동하는 경우
                    player[p] = (ni,nj)
                    arr[ci][cj] = []
                    arr[ni][nj] = [p,nd]
                    break
                elif len(arr[ni][nj]) > 0: # 다른 도둑말과 위치를 바꾸는 경우
                    player[arr[ni][nj][0]] = (ci,cj)
                    player[p] = (ni,nj)
                    tmp = arr[ni][nj]
                    arr[ni][nj] = [p,nd]
                    arr[ci][cj] = tmp
                    break

    # 술래말 이동
    nTi, nTj = Ti, Tj
    catch_cnt = 0

    while True:
        nTi, nTj = nTi+di[Td], nTj+dj[Td]
        if 0<=nTi<4 and 0<=nTj<4:
            if len(arr[nTi][nTj]) > 0:
                new_score = score + arr[nTi][nTj][0]
                nTd = arr[nTi][nTj][1]
                new_arr = copy.deepcopy(arr)
                new_arr[nTi][nTj] = []

                q.append((new_arr, new_score, nTi, nTj, nTd))
        else:
            break

    if catch_cnt == 0:
        final_scores.append(score)


print(max(final_scores))