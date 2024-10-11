# 루돌프 방향
# 상0, 상우1, 우2, 하우3, 하4, 하좌5, 좌6, 상좌7
Rdi = [-1, -1, 0, 1, 1, 1, 0, -1]
Rdj = [0, 1, 1, 1, 0, -1, -1, -1]

# 산타 방향
# 상0, 우1, 하2, 좌3
Pdi = [-1, 0, 1, 0]
Pdj = [0, 1, 0, -1]

N,M,P,C,D = map(int, input().split())
Ri,Rj = map(int, input().split())
Ri,Rj = Ri-1,Rj-1

santa = dict()
santa_arr = [[[] for _ in range(N)] for _ in range(N)]
for _ in range(P):
    Pn,Sr,Sc = map(int, input().split())
    santa[Pn] = [(Sr-1,Sc-1), 0, 0, 0]  # [0:(좌표) / 1:기절 / 2:탈락(0생존,1탈락) / 3:점수]
    santa_arr[Sr-1][Sc-1].append(Pn)
sorted_santa = dict(sorted(santa.items()))
santa = sorted_santa


def distance(r1,c1,r2,c2):
    return (r1-r2)**2 + (c1-c2)**2


for _ in range(M):
    # 루돌프의 움직임
    d_R2P, tgt_Pi, tgt_Pj, tgt_Pidx = N**3, -1, -1, -1
    for idx, info in santa.items():
        if info[2] == 1:
            continue

        dist = distance(Ri, Rj, info[0][0], info[0][1])
        if d_R2P > dist:
            d_R2P, tgt_Pi, tgt_Pj, tgt_Pidx = dist, info[0][0], info[0][1], idx
        elif d_R2P == dist:
            if tgt_Pi < info[0][0]:
                d_R2P, tgt_Pi, tgt_Pj, tgt_Pidx = dist, info[0][0], info[0][1], idx
            elif tgt_Pi == info[0][0]:
                if tgt_Pj < info[0][1]:
                    d_R2P, tgt_Pi, tgt_Pj, tgt_Pidx = dist, info[0][0], info[0][1], idx

    final_Ri, final_Rj, final_Rd = -1, -1, -1
    for d in range(8):
        nRi, nRj = Ri+Rdi[d], Rj+Rdj[d]
        dist = distance(tgt_Pi, tgt_Pj, nRi, nRj)
        if d_R2P > dist:
            d_R2P, final_Ri, final_Rj, final_Rd = dist, nRi, nRj, d
    Ri, Rj = final_Ri, final_Rj

    # 루돌프가 움직여서 일어난 충돌
    if (Ri, Rj) == (tgt_Pi, tgt_Pj):
        santa[tgt_Pidx][3] += C
        santa[tgt_Pidx][1] = 2

        new_Pi, new_Pj = tgt_Pi+C*Rdi[final_Rd], tgt_Pj+C*Rdj[final_Rd]

        if 0<=new_Pi< N and 0<=new_Pj<N:
            if len(santa_arr[new_Pi][new_Pj]) == 0: # 격자내 & 빈칸
                santa_arr[tgt_Pi][tgt_Pj].remove(tgt_Pidx)
                santa_arr[new_Pi][new_Pj].append(tgt_Pidx)
                santa[tgt_Pidx][0] = (new_Pi, new_Pj)
            else: # 격자내 & 다른 산타 있음 -> 상호작용
                q = []
                i, j = new_Pi, new_Pj
                while True:
                    ni, nj = i+Rdi[final_Rd], j+Rdj[final_Rd]
                    if 0<=ni<N and 0<=nj<N:
                        if len(santa_arr[ni][nj]) == 0:
                            break
                    else:
                        break
                    q.append((i, j))
                    i, j = ni, nj

                q_reversed = q[::-1]

                for i,j in q_reversed:
                    that_idx = santa_arr[i][j][0]
                    ni,nj = i+Rdi[final_Rd], j+Rdj[final_Rd]
                    santa_arr[i][j].remove(that_idx)
                    santa_arr[ni][nj].append(that_idx)
                    santa[that_idx][0] = (ni,nj)

                santa_arr[tgt_Pi][tgt_Pj].remove(tgt_Pidx)
                santa_arr[new_Pi][new_Pj].append(tgt_Pidx)
                santa[tgt_Pidx][0] = (new_Pi, new_Pj)

        else: # 격자밖
            santa[tgt_Pidx][2] = 1
            santa_arr[tgt_Pi][tgt_Pj].remove(tgt_Pidx)

    # 종료 조건
    cnt = 0
    for idx, info in santa.items():
        if info[2] == 0:
            cnt += 1
    if cnt == 0:
        break

    # 산타의 움직임
    for idx, info in santa.items():
        if info[1] > 0 or info[2] == 1:
            continue

        d_P2R = distance(Ri, Rj, info[0][0], info[0][1])
        final_Pi, final_Pj, final_Pd = info[0][0], info[0][1], -1
        for d in range(4):
            nPi,nPj = info[0][0]+Pdi[d], info[0][1]+Pdj[d]
            if 0<=nPi<N and 0<=nPj<N and len(santa_arr[nPi][nPj])==0:
                dist = distance(Ri, Rj, nPi, nPj)
                if d_P2R> dist:
                    d_P2R, final_Pi, final_Pj, final_Pd = dist, nPi, nPj, d

        santa_arr[info[0][0]][info[0][1]].remove(idx)
        santa_arr[final_Pi][final_Pj].append(idx)
        info[0] = (final_Pi, final_Pj)

        # 산타가 움직여서 일어난 충돌
        if (final_Pi, final_Pj) == (Ri, Rj):
            info[3] += D
            info[1] = 2

            new_Pi, new_Pj = final_Pi+D*Pdi[(final_Pd+2)%4], final_Pj+D*Pdj[(final_Pd+2)%4]

            if 0<=new_Pi<N and 0<=new_Pj<N:
                if len(santa_arr[new_Pi][new_Pj]) == 0: # 격자내 & 빈칸
                    santa_arr[final_Pi][final_Pj].remove(idx)
                    santa_arr[new_Pi][new_Pj].append(idx)
                    info[0] = (new_Pi, new_Pj)
                else: # 격자내 & 다른 산타 있음 -> 상호작용
                    q = []
                    i, j = new_Pi, new_Pj
                    while True:
                        ni,nj = i+Pdi[(final_Pd+2)%4], j+Pdj[(final_Pd+2)%4]
                        if 0<=ni<N and 0<=nj<N:
                            if len(santa_arr[ni][nj]) == 0:
                                break
                        else:
                            break
                        q.append((ni, nj))
                        i,j = ni,nj
                    q_reversed = q[::-1]

                    for i,j in q_reversed:
                        that_idx = santa_arr[i][j][0]
                        ni,nj = i+Pdi[(final_Pd+2)%4], j+Pdj[(final_Pd+2)%4]
                        santa_arr[i][j].remove(that_idx)
                        santa_arr[ni][nj].append(that_idx)
                        santa[that_idx][0] = (ni,nj)

                    santa_arr[final_Pi][final_Pj].remove(idx)
                    santa_arr[new_Pi][new_Pj].append(idx)
                    info[0] = (new_Pi, new_Pj)

            else: # 격자밖
                info[2] = 1
                santa_arr[final_Pi][final_Pj].remove(idx)

    # 종료 조건
    cnt = 0
    for idx, info in santa.items():
        if info[2] == 0:
            cnt += 1
    if cnt == 0:
        break

    # 기절 조정 & 탈락하지 않은 산타들에게 1점씩 추가 부여
    for idx, info in santa.items():
        if info[1] > 0:
            info[1] -= 1

        if info[2] == 0:
            info[3] += 1

ans_lst = []
for idx, info in santa.items():
    ans_lst.append(str(info[-1]))
ans = ' '.join(ans_lst)
print(ans)