import copy

N,M = map(int, input().split())
arr = [list(input()) for _ in range(N)]
narr = [[0 for _ in range(M)] for _ in range(N)]  # 0:빈칸, 1:장애물

blue_i, blue_j = -1, -1
red_i, red_j = -1, -1
exi,exj = -1, -1
for i in range(N):
    for j in range(M):
        if arr[i][j] == '#':
            narr[i][j] = 1
        elif arr[i][j] == 'B':
            blue_i, blue_j = i,j
        elif arr[i][j] == 'R':
            red_i, red_j = i,j
        elif arr[i][j] == 'O':
            exi,exj = i,j
arr = narr

# 상0 우1 하2 좌3
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

configuration = [(blue_i,blue_j,red_i,red_j)]
q = [[0,(blue_i,blue_j),(red_i,red_j), configuration]]  # [cnt, blue 좌표, red 좌표, cfg]


flag = -1
while q:
    cnt, b_loc, r_loc, cfg = q.pop(0)

    if cnt == 10:
        continue

    for d in range(4):  # 상우하좌 우선순위
        if d in (0,2) and b_loc[1] == r_loc[1]:  # 상,하 간섭 일어나는 경우
            if d == 0:  # 상
                i, j = min(b_loc[0],r_loc[0]), b_loc[1]
                while True:
                    ni, nj = i+di[d], j+dj[d]
                    if 0 <= ni < N and 0 <= nj < N:
                        if arr[ni][nj] == 1:
                            break
                        else:
                            i, j = ni, nj
                    else:
                        break
                if (i,j) == (exi,exj):
                    continue
                if b_loc[0] < r_loc[0]:
                    bi, bj = i, j
                    ri, rj = i+1, j
                else:
                    ri, rj = i, j
                    bi, bj = i+1, j
            else:  # 하
                i, j = max(b_loc[0], r_loc[0]), b_loc[1]
                while True:
                    ni, nj = i + di[d], j + dj[d]
                    if 0 <= ni < N and 0 <= nj < N:
                        if arr[ni][nj] == 1:
                            break
                        else:
                            i, j = ni, nj
                    else:
                        break
                if (i,j) == (exi,exj):
                    continue
                if b_loc[0] > r_loc[0]:
                    bi, bj = i, j
                    ri, rj = i-1, j
                else:
                    ri, rj = i, j
                    bi, bj = i-1, j
        elif d in (1,3) and b_loc[0] == r_loc[0]:  # 좌,우 간섭 일어나는 경우
            if d == 1:  # 우
                i, j = b_loc[0], max(b_loc[1],r_loc[1])
                while True:
                    ni, nj = i+di[d], j+dj[d]
                    if 0 <= ni < N and 0 <= nj < N:
                        if arr[ni][nj] == 1:
                            break
                        else:
                            i, j = ni, nj
                    else:
                        break
                if (i,j) == (exi,exj):
                    continue
                if b_loc[1] > r_loc[1]:
                    bi, bj = i, j
                    ri, rj = i, j-1
                else:
                    ri, rj = i, j
                    bi, bj = i, j-1
            else:  # 좌
                i, j = b_loc[0], min(b_loc[1],r_loc[1])
                while True:
                    ni, nj = i + di[d], j + dj[d]
                    if 0 <= ni < N and 0 <= nj < N:
                        if arr[ni][nj] == 1:
                            break
                        else:
                            i, j = ni, nj
                    else:
                        break
                if (i,j) == (exi,exj):
                    continue
                if b_loc[1] < r_loc[1]:
                    bi, bj = i, j
                    ri, rj = i, j+1
                else:
                    ri, rj = i, j
                    bi, bj = i, j+1

        else:  # 독립적인 경우
            # 빨간 구슬 -> 해당 방향으로 tilting 진행
            ri, rj = r_loc
            while True:
                nri, nrj = ri + di[d], rj + dj[d]
                if 0 <= nri < N and 0 <= nrj < M:
                    if arr[nri][nrj] == 1:
                        break
                    else:
                        ri, rj = nri, nrj
                else:
                    break
            # 파랑 구슬 -> 해당 방향으로 tilting 진행
            bi, bj = b_loc
            while True:
                nbi, nbj = bi + di[d], bj + dj[d]
                if 0 <= nbi < N and 0 <= nbj < M:
                    if arr[nbi][nbj] == 1:
                        break
                    else:
                        bi, bj = nbi, nbj
                else:
                    break

        # 빨O,파O / 빨X,파O -> continue
        if (bi, bj) == (exi, exj):
            continue

        # 빨O,파X -> break
        if (ri, rj) == (exi, exj):
            flag = cnt + 1
            break

        # 빨X,파X -> queue에 work 추가
        if (bi,bj,ri,rj) not in cfg:
            new_cfg = copy.deepcopy(cfg)
            new_cfg.append((bi,bj,ri,rj))
            q.append([cnt+1, (bi,bj), (ri,rj), new_cfg])

    if flag > 0:
        break


if flag > 0:
    print(flag)
else:
    print(-1)







