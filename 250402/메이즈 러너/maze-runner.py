N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
player = dict()
for idx in range(1, M+1):
    i, j = map(int, input().split())
    player[idx] = [i-1, j-1]
exi, exj = map(int, input().split())
exi, exj = exi-1, exj-1

MAX_DIST = 10**3

move_cnt = 0
for _ in range(K):
    # 1. 모든 참가자 한칸씩 동시에 움직임
    del_idx = []
    for idx, info in player.items():
        cur_dist = abs(info[0]-exi) + abs(info[1]-exj)
        next_i, next_j = info
        for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
            ni, nj = info[0]+di, info[1]+dj
            if 0<=ni<N and 0<=nj<N and arr[ni][nj]==0:
                n_dist = abs(ni-exi) + abs(nj-exj)
                if n_dist < cur_dist:
                    cur_dist, next_i, next_j = n_dist, ni, nj

        if [next_i, next_j] == info:  # 안 움직인 경우
            continue
        elif [next_i, next_j] == [exi, exj]:  # 출구에 도착한 경우
            move_cnt += 1
            del_idx.append(idx)
        else:
            move_cnt += 1
            info[0] = next_i
            info[1] = next_j

    for idx in del_idx:
        del player[idx]
    # [종료] 모든 참가자 탈출 -> break
    if len(player) == 0:
        break
    # print()

    # 2. 조건에 따라 미로 회전
    min_side, min_si, min_sj = N, N, N
    for idx, info in player.items():
        side = max(abs(info[0]-exi), abs(info[1]-exj))
        si = max(0, max(info[0],exi)-side)
        sj = max(0, max(info[1],exj)-side)

        if side < min_side:
            min_side, min_si, min_sj = side, si, sj
        elif side == min_side:
            if si < min_si:
                min_side, min_si, min_sj = side, si, sj
            elif si == min_si:
                if sj < min_sj:
                    min_side, min_si, min_sj = side, si, sj
                    
    # 이 범위 내에 있는 사람들 구하기
    rotate_idx = []
    for idx, info in player.items():
        if min_si<=info[0]<=min_si+min_side and min_sj<=info[1]<=min_sj+min_side:
            rotate_idx.append(idx)
    # print()

    # 이 정사각형 시계방향 90도 회전 / 출구, 사람도 같이 회전 / 이 내부에 있던 벽들은 내구도 -= 1
    new_arr = [[0 for _ in range(min_side+1)] for _ in range(min_side+1)]
    for i in range(min_si, min_si+min_side+1):
        for j in range(min_sj, min_sj+min_side+1):
            new_arr[j-min_sj][min_side-(i-min_si)] = max(0, arr[i][j]-1)
    for i in range(min_side+1):
        for j in range(min_side+1):
            arr[min_si+i][min_sj+j] = new_arr[i][j]

    exi, exj = min_si+exj-min_sj, min_sj+min_side-(exi-min_si)

    for idx in rotate_idx:
        ci, cj = player[idx]
        player[idx] = [min_si+cj-min_sj, min_sj+min_side-(ci-min_si)]


print(move_cnt)
print(exi+1, exj+1, sep=' ')

