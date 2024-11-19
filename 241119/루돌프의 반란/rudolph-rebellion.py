def distance(r1, c1, r2, c2):
    return (r1-r2)**2 + (c1-c2)**2


def interaction(s_idx, si, sj, di, dj, arr):  # 10^2
    global santa

    candidates = []
    ci, cj = si, sj
    while True:  # 10^2
        candidates.append(arr[ci][cj])
        ni, nj = ci+di, cj+dj
        if 0 <= ni < N and 0 <= nj < N:
            if arr[ni][nj] == 0:
                break
            else:
                ci, cj = ni, nj
        else:
            break
    candidates.reverse()

    for idx in candidates:  # 10^2
        ni, nj = santa[idx][0][0]+di, santa[idx][0][1]+dj
        if 0 <= ni < N and 0 <= nj < N:
            santa[idx][0] = (ni, nj)
        else:
            del santa[idx]

    santa[s_idx][0] = (si,sj)


N, M, P, C, D = map(int, input().split())
INF = 10 * N**2

ri, rj = map(int, input().split())
ri, rj = ri-1, rj-1

unsorted_santa = dict()
for _ in range(P):  # 10^1
    idx, si, sj = map(int, input().split())
    unsorted_santa[idx] = [(si-1, sj-1), 0, 0]  # [(좌표), 기절, 점수]
santa = dict(sorted(unsorted_santa.items()))

# 루돌프 방향 (8방향) ↑0 ↗1 →2 ↘3 ↓4 ↙5 ←6 ↖7
rdi = [-1, -1, 0, 1, 1, 1, 0, -1]
rdj = [0, 1, 1, 1, 0, -1, -1, -1]

# 산타 방향 (4방향) ↑0 →1 ↓2 ←3
sdi = [-1, 0, 1, 0]
sdj = [0, 1, 0, -1]

ans = [-1 for _ in range(P+1)]
for _ in range(M):  # 10^3
    # 1. 루돌프 움직임 10^2 -> 총 10^5
    min_dist, tsi, tsj, ts = INF, -1, -1, -1
    for idx, info in santa.items():  # 10^1
        dist = distance(ri, rj, info[0][0], info[0][1])
        if dist < min_dist:
            min_dist, tsi, tsj, ts = dist, info[0][0], info[0][1], idx
        elif dist == min_dist:
            if info[0][0] > tsi:
                min_dist, tsi, tsj, ts = dist, info[0][0], info[0][1], idx
            elif info[0][0] == tsi:
                if info[0][1] > tsj:
                    min_dist, tsi, tsj, ts = dist, info[0][0], info[0][1], idx

    min_dist, nri, nrj, rd = INF, -1, -1, -1
    for d in range(8):  # 10^0
        mv_ri, mv_rj = ri+rdi[d], rj+rdj[d]
        if 0 <= mv_ri < N and 0 <= mv_rj < N:
            dist = distance(mv_ri, mv_rj, tsi, tsj)
            if dist < min_dist:
                min_dist, nri, nrj, rd = dist, mv_ri, mv_rj, d

    if (nri, nrj) != (tsi, tsj):
        ri, rj = nri, nrj
    else:  # 루돌프 유발 충돌
        ri, rj = nri, nrj
        santa[ts][1] = 2
        santa[ts][2] += C

        ntsi, ntsj = tsi+C*rdi[rd], tsj+C*rdj[rd]
        if 0 <= ntsi < N and 0<= ntsj < N:
            arr = [[0 for _ in range(N)] for _ in range(N)]
            for idx, info in santa.items():  # 10^1
                if idx == ts:
                    continue
                arr[info[0][0]][info[0][1]] = idx

            if arr[ntsi][ntsj] == 0:
                santa[ts][0] = (ntsi, ntsj)
            else:  # 상호작용
                interaction(ts, ntsi, ntsj, rdi[rd], rdj[rd], arr)  # 10^2

        else:
            ans[ts] = santa[ts][2]
            del santa[ts]

    # 종료 체크
    if len(santa) == 0:
        break

    # 2. 산타 움직임 10^3 -> 총 10^6
    del_idx = []
    for idx, info in santa.items():  # 10^1
        if info[1] != 0:
            continue

        min_dist = distance(ri, rj, info[0][0], info[0][1])
        nsi, nsj, sd = info[0][0], info[0][1], -1  # 디폴트
        for d in range(4):  # 10^0
            mv_si, mv_sj = info[0][0]+sdi[d], info[0][1]+sdj[d]
            if 0 <= mv_si < N and 0 <= mv_sj < N:
                flag = 0
                for idx2, info2 in santa.items():  # 10^1
                    if idx != idx2 and info2[0] == (mv_si, mv_sj):
                        flag = 1
                        break
                if flag == 1:
                    continue
                else:
                    dist = distance(ri, rj, mv_si, mv_sj)
                    if dist < min_dist:
                        min_dist, nsi, nsj, sd = dist, mv_si, mv_sj, d
            else:
                continue

        if (nsi, nsj) != (ri, rj):
            info[0] = (nsi, nsj)
        else:  # 산타 유발 충돌
            info[1] = 2
            info[2] += D

            sd = (sd+2) % 4
            nsi, nsj = nsi+D*sdi[sd], nsj+D*sdj[sd]
            if 0 <= nsi < N and 0 <= nsj < N:
                arr = [[0 for _ in range(N)] for _ in range(N)]
                for idx2, info2 in santa.items():  # 10^1
                    if idx == idx2:
                        continue
                    arr[info2[0][0]][info2[0][1]] = idx2

                if arr[nsi][nsj] == 0:
                    info[0] = (nsi, nsj)
                else:  # 상호작용
                    interaction(idx, nsi, nsj, sdi[sd], sdj[sd], arr)  # 10^2

            else:
                ans[idx] = info[2]
                del_idx.append(idx)

        # 종료 체크
        if len(santa) == len(del_idx):
            break

    for idx in del_idx:
        del santa[idx]
    if len(santa) == 0:
        break

    # 3. 기절
    # 4. 탈락 안한 산타 점수 추가
    for idx, info in santa.items():
        if info[1] != 0:
            info[1] -= 1
        info[2] += 1


if len(santa) > 0:
    for idx, info in santa.items():
        ans[idx] = info[2]
final_ans = []
for i in range(1, P+1):
    final_ans.append(str(ans[i]))
str_ans = ' '.join(final_ans)
print(str_ans)



