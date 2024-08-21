N,M,P,C,D = map(int, input().split())

Ri,Rj = map(int, input().split())
Ri,Rj = Ri-1, Rj-1

santa = dict()
arr = [[0 for _ in range(N)] for _ in range(N)]
for _ in range(P):
    Pn,Sr,Sc = map(int, input().split())
    santa[Pn] = [(Sr-1,Sc-1),0,0]
    arr[Sr-1][Sc-1] = Pn
santa = dict(sorted(santa.items()))

# ⭡0  ↗1  ⭢2  ↘3  ⭣4  ↙5  ⭠6  ↖7
Rdi = [-1,-1,0,1,1,1,0,-1]
Rdj = [0,1,1,1,0,-1,-1,-1]

# ⭡0  ⭢1  ⭣2  ⭠3
Sdi = [-1,0,1,0]
Sdj = [0,1,0,-1]


def distance(si,sj,ei,ej):
    return (si-ei)**2 + (sj-ej)**2


for _ in range(M):
    # 루돌프의 움직임 -> Ri, Rj, Rd
    dtS, tSi, tSj, tS_idx = 3*N*N, -1, -1, 0
    for idx, info in santa.items():
        if info[0] == (-1,-1):
            continue

        dist = distance(Ri,Rj,info[0][0],info[0][1])
        if dtS > dist:
            dtS, tSi, tSj, tS_idx = dist, info[0][0], info[0][1], idx
        elif dtS == dist:
            if tSi < info[0][0]:
                dtS, tSi, tSj, tS_idx = dist, info[0][0], info[0][1], idx
            elif tSi == info[0][0]:
                if tSj < info[0][1]:
                    dtS, tSi, tSj, tS_idx = dist, info[0][0], info[0][1], idx

    nRi, nRj, Rd = Ri, Rj, -1
    for d in range(8):
        if 0<=Ri+Rdi[d]<N and 0<=Rj+Rdj[d]<N:
            dist = distance(Ri+Rdi[d],Rj+Rdj[d],tSi,tSj)
            if dtS > dist:
                dtS = dist
                nRi, nRj, Rd = Ri+Rdi[d], Rj+Rdj[d], d

    Ri, Rj = nRi, nRj

    # 루돌프로 인한 충돌
    if (Ri,Rj) == (tSi,tSj):
        santa[tS_idx][2] += C
        santa[tS_idx][1] = 2

        arr[tSi][tSj] = 0
        nSi, nSj = tSi+C*Rdi[Rd], tSj+C*Rdj[Rd]

        if 0<=nSi<N and 0<=nSj<N:
            if arr[nSi][nSj] == 0:
                santa[tS_idx][0] = (nSi,nSj)
                arr[nSi][nSj] = tS_idx
            else:
                # 상호작용
                q = [arr[nSi][nSj]]
                nnSi, nnSj = nSi, nSj
                while True:
                    nnSi, nnSj = nnSi+Rdi[Rd], nnSj+Rdj[Rd]
                    if 0<=nnSi<N and 0<=nnSj<N:
                        if arr[nnSi][nnSj] == 0:
                            break
                        else:
                            q.append(arr[nnSi][nnSj])
                    else:
                        break

                for colS_idx in q[::-1]:
                    ci,cj = santa[colS_idx][0][0], santa[colS_idx][0][1]
                    ni,nj = ci+Rdi[Rd], cj+Rdj[Rd]
                    if 0<=ni<N and 0<=nj<N:
                        santa[colS_idx][0] = (ni,nj)
                        arr[ci][cj] = 0
                        arr[ni][nj] = colS_idx
                    else:
                        santa[colS_idx][0] = (-1,-1)
                        arr[ci][cj] = 0

                santa[tS_idx][0] = (nSi,nSj)
                arr[nSi][nSj] = tS_idx

        else:
            santa[tS_idx][0] = (-1,-1)

    end_flag = 1
    for idx, info in santa.items():
        if info[0] != (-1,-1):
            end_flag = 0
            break
    if end_flag == 1:
        break

    # 산타의 움직임
    for idx, info in santa.items():
        if info[1] != 0 or info[0] == (-1,-1):
            continue

        min_d = distance(Ri,Rj,info[0][0],info[0][1])
        mv_Si, mv_Sj, Sd = info[0][0], info[0][1], -1
        for d in range(4):
            ni,nj = info[0][0]+Sdi[d], info[0][1]+Sdj[d]
            dist = distance(Ri,Rj,ni,nj)
            if 0<=ni<N and 0<=nj<N and arr[ni][nj]==0 and min_d>dist:
                min_d = dist
                mv_Si, mv_Sj, Sd = ni, nj, d

        # 산타로 인한 충돌
        if (mv_Si,mv_Sj) == (Ri,Rj):
            santa[idx][2] += D
            santa[idx][1] = 2

            arr[info[0][0]][info[0][1]] = 0
            nSi, nSj = mv_Si + D*Sdi[(Sd+2)%4], mv_Sj + D*Sdj[(Sd+2)%4]

            if 0<=nSi<N and 0<=nSj<N:
                if arr[nSi][nSj] == 0:
                    santa[idx][0] = (nSi, nSj)
                    arr[nSi][nSj] = idx
                else:
                    # 상호작용
                    q = [arr[nSi][nSj]]
                    nnSi, nnSj = nSi, nSj
                    while True:
                        nnSi, nnSj = nnSi + Sdi[(Sd+2)%4], nnSj + Sdj[(Sd+2)%4]
                        if 0<=nnSi<N and 0<=nnSj<N:
                            if arr[nnSi][nnSj] == 0:
                                break
                            else:
                                q.append(arr[nnSi][nnSj])
                        else:
                            break

                    for colS_idx in q[::-1]:
                        ci, cj = santa[colS_idx][0][0], santa[colS_idx][0][1]
                        ni, nj = ci + Sdi[(Sd+2)%4], cj + Sdj[(Sd+2)%4]
                        if 0<=ni<N and 0<=nj<N:
                            santa[colS_idx][0] = (ni,nj)
                            arr[ci][cj] = 0
                            arr[ni][nj] = colS_idx
                        else:
                            santa[colS_idx][0] = (-1, -1)
                            arr[ci][cj] = 0

                    santa[idx][0] = (nSi, nSj)
                    arr[nSi][nSj] = idx

            else:
                santa[idx][0] = (-1, -1)

        else:
            arr[info[0][0]][info[0][1]] = 0
            arr[mv_Si][mv_Sj] = idx
            santa[idx][0] = (mv_Si, mv_Sj)

    end_flag = 1
    for idx, info in santa.items():
        if info[0] != (-1, -1):
            end_flag = 0
            info[1] = max(0,info[1]-1)
            info[2] += 1

    if end_flag == 1:
        break

ans = []
for idx, info in santa.items():
    ans.append(str(info[-1]))
ans_str = ' '.join(ans)
print(ans_str)