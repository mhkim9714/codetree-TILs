import copy

N,M,K = map(int, input().split())
INF = N**3
arr = [list(map(int, input().split())) for _ in range(N)]

people = dict()
for idx in range(1,M+1):
    x,y = map(int, input().split())
    people[idx] = [x-1,y-1]

exi,exj = map(int, input().split())
exi,exj = exi-1,exj-1


def distance(x1,y1,x2,y2):
    return abs(x1-x2) + abs(y1-y2)


ans = 0
for t in range(1,K+1):
    # 1) 모든 참가자가 동시에 한칸씩 움직임 (현재보다 거리 짧아야함 / 거리작->상하->좌우)
    del_idx = []
    for idx, info in people.items():
        new_i,new_j = info[0],info[1]
        cur_dist = distance(info[0],info[1],exi,exj)
        for di,dj in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni,nj = info[0]+di, info[1]+dj
            if 0<=ni<N and 0<=nj<N and arr[ni][nj]==0:
                new_dist = distance(ni,nj,exi,exj)
                if cur_dist > new_dist:
                    new_i,new_j = ni,nj
                    cur_dist = new_dist

        if (new_i,new_j) != (info[0],info[1]):
            info[0],info[1] = new_i,new_j
            ans += 1

        if (new_i,new_j) == (exi,exj):
            del_idx.append(idx)

    for idx in del_idx:
        del people[idx]

    if len(people) == 0:
        break

    # 2) 정사각형 구하기 (한명 이상의 참가자와 출구 포함) (길이작->좌상단r작->좌상단c작)
    final_l, final_i0, final_j0 = N+2, N, N
    for idx, info in people.items():
        length = max(abs(info[0]-exi), abs(info[1]-exj))
        i0 = max(max(info[0],exi)-length, 0)
        j0 = max(max(info[1],exj)-length, 0)
        if final_l > length:
            final_l, final_i0, final_j0 = length, i0, j0
        elif final_l == length:
            if final_i0 > i0:
                final_l, final_i0, final_j0 = length, i0, j0
            elif final_i0 == i0:
                if final_j0 > j0:
                    final_l, final_i0, final_j0 = length, i0, j0

    # 3) 정사각형 시계방향 90도 회전 및 내구도 -1
    narr = copy.deepcopy(arr)
    final_exi,final_exj = exi,exj
    for i in range(final_i0,final_i0+final_l+1):
        for j in range(final_j0,final_j0+final_l+1):
            narr[final_i0+(j-final_j0)][final_j0+(final_l-(i-final_i0))] = max(arr[i][j]-1, 0)
            if (i,j) == (exi,exj):
                final_exi,final_exj = final_i0+(j-final_j0), final_j0+(final_l-(i-final_i0))
    arr = narr
    exi,exj = final_exi,final_exj

    for idx, info in people.items():
        if final_i0<=info[0]<=final_i0+final_l and final_j0<=info[1]<=final_j0+final_l:
            info[0], info[1] = final_i0+(info[1]-final_j0), final_j0+(final_l-(info[0]-final_i0))

print(ans)
print(exi+1,exj+1)