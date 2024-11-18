# 상0, 우1, 하2, 좌3
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

N,M = map(int, input().split())
temp = [list(input()) for _ in range(N)]

# 초기 빨간색 구슬, 파란색 구슬, 최종 탈출 좌표 구하기
arr = [[0 for _ in range(M)] for _ in range(N)]  # 0:빈칸, 1:장애물
ri,rj,bi,bj,exi,exj = -1,-1,-1,-1,-1,-1
for i in range(N):
    for j in range(M):
        if temp[i][j] == '#':
            arr[i][j] = 1
            continue
        if temp[i][j] == 'R':
            ri,rj = i,j
            continue
        elif temp[i][j] == 'B':
            bi,bj = i,j
            continue
        elif temp[i][j] == 'O':
            exi,exj = i,j
            continue


def BFS(ri, rj, bi, bj):  # cnt번째 초기 입력으로 주어지는 ri,rj,bi,bj
    q = []
    visited = []

    q.append((1,ri,rj,bi,bj))
    visited.append((ri,rj,bi,bj))

    while q:
        cnt, cri, crj, cbi, cbj = q.pop(0)

        if cnt > 10:
            return -1

        for d in range(4):
            # 해당 방향으로 한번 이동한 결과 구하기
            red_coords = []
            nri, nrj = cri, crj
            while True:  # move_red
                red_coords.append((nri,nrj))
                if (nri,nrj) == (exi,exj):
                    break
                check_ri, check_rj = nri+di[d], nrj+dj[d]
                if 0<=check_ri<N and 0<=check_rj<M:  # 격자내
                    if arr[check_ri][check_rj] == 1:  # 장애물 있음
                        break
                    else:  # 장애물 없음 & {빈칸 or 출구}
                        nri, nrj = check_ri, check_rj
                else:  # 격자밖
                    break

            blue_coords = []
            nbi, nbj = cbi, cbj
            while True:  # move_blue
                blue_coords.append((nbi,nbj))
                if (nbi,nbj) == (exi,exj):
                    break
                check_bi, check_bj = nbi+di[d], nbj+dj[d]
                if 0<=check_bi<N and 0<=check_bj<M:  # 격자내
                    if arr[check_bi][check_bj] == 1:  # 장애물 있음
                        break
                    else:  # 장애물 없음
                        nbi, nbj = check_bi, check_bj
                else:  # 격자밖
                    break

            if red_coords[-1] != blue_coords[-1]:
                final_nri, final_nrj = red_coords[-1]
                final_nbi, final_nbj = blue_coords[-1]
            else:
                if red_coords[-1] == (exi,exj):
                    final_nri, final_nrj = red_coords[-1]
                    final_nbi, final_nbj = blue_coords[-1]
                else:  # 구슬끼리 충돌이 일어난 경우
                    min_len = min(len(red_coords), len(blue_coords))
                    red_coords = red_coords[:min_len]
                    blue_coords = blue_coords[:min_len]
                    final_nri, final_nrj = red_coords[-1]
                    final_nbi, final_nbj = blue_coords[-1]

            # 결과1: 빨out, 파out -> 실패
            # 결과2: 빨in, 파out -> 실패
            if (final_nbi,final_nbj) == (exi,exj):
                continue

            # 결과3: 빨out, 파in -> 성공 (return)
            elif (final_nri,final_nrj) == (exi,exj):
                return cnt

            # 결과4: 빨in, 파in -> 계속 진행 재귀
            else:
                if (final_nri, final_nrj, final_nbi, final_nbj) in visited:
                    continue
                else:
                    q.append((cnt+1, final_nri, final_nrj, final_nbi, final_nbj))
                    visited.append((final_nri, final_nrj, final_nbi, final_nbj))


ans = BFS(ri,rj,bi,bj)
print(ans)



