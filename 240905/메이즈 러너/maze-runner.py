N,M,K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]

player = dict()
for idx in range(1,M+1):
    i,j = map(int, input().split())
    player[idx] = (i-1,j-1)

exi,exj = map(int, input().split())
exi,exj = exi-1,exj-1


def distance(si,sj,ei,ej):
    return abs(si-ei) + abs(sj-ej)


ans = 0
for _ in range(K):
    # 모든 참가자 이동
    del_idx = []
    for idx, coord in player.items():
        min_dist = distance(coord[0],coord[1],exi,exj)
        new_coord_i = coord[0]
        new_coord_j = coord[1]
        for di,dj in ((0,-1),(0,1),(-1,0),(1,0)):
            ni,nj = coord[0]+di, coord[1]+dj
            if 0<=ni<N and 0<=nj<N and arr[ni][nj]==0 and min_dist>=distance(ni,nj,exi,exj):
                min_dist = distance(ni,nj,exi,exj)
                new_coord_i, new_coord_j = ni,nj

        if coord != (new_coord_i, new_coord_j):
            player[idx] = (new_coord_i, new_coord_j)
            ans += 1

        if (new_coord_i, new_coord_j) == (exi,exj):
            del_idx.append(idx)

    for idx in del_idx:
        player.pop(idx)
    if len(player) == 0:
        break

    # 정사각형 찾기
    sq_i, sq_j, sq_d = N,N,N
    for idx, coord in player.items():
        n_sq_d = distance(coord[0],coord[1],exi,exj)
        n_sq_i = max(max(coord[0],exi)-n_sq_d, 0)
        n_sq_j = max(max(coord[1],exj)-n_sq_d, 0)

        if sq_d > n_sq_d:
            sq_d,sq_i,sq_j = n_sq_d,n_sq_i,n_sq_j
        elif sq_d == n_sq_d:
            if sq_i > n_sq_i:
                sq_d,sq_i,sq_j = n_sq_d,n_sq_i,n_sq_j
            elif sq_i == n_sq_i:
                if sq_j > n_sq_j:
                    sq_d,sq_i,sq_j = n_sq_d,n_sq_i,n_sq_j

    # 미로 회전
    new_square = [[0 for _ in range(sq_d+1)] for _ in range(sq_d+1)]
    for i in range(sq_d+1):
        for j in range(sq_d+1):
            new_square[j][sq_d-i] = arr[sq_i+i][sq_j+j]
    for i in range(sq_d+1):
        for j in range(sq_d+1):
            arr[sq_i+i][sq_j+j] = max(new_square[i][j]-1,0)

    # 출구 회전
    nexi = sq_i + (exj-sq_j)
    nexj = sq_j + sq_d - (exi-sq_i)
    exi,exj = nexi, nexj

    # 정사각형에 속하는 플레이어 좌표 회전
    for idx in player.keys():
        if sq_i <= player[idx][0] < (sq_i+sq_d+1) and sq_j <= player[idx][1] < (sq_j+sq_d+1):
            new_coord_i = sq_i + (player[idx][1]-sq_j)
            new_coord_j = sq_j + sq_d - (player[idx][0]-sq_i)
            player[idx] = (new_coord_i, new_coord_j)


print(ans)
print(f'{exi+1} {exj+1}')