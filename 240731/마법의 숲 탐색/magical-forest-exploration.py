R,C,K = map(int,input().split())
arr = [[-1]*C for _ in range(R)]
monster = dict()

# 상(0) 우(1) 하(2) 좌(3)
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

ans = 0
for k in range(K):
    init_column, cd = map(int,input().split())
    ci,cj = 0,init_column-1

    # 골렘을 가능한 한 남쪽으로 움직이기
    while True:
        # 남쪽 한칸 이동
        if 0<=(ci+2)<R and arr[ci+1][cj-1]==-1 and arr[ci+2][cj]==-1 and arr[ci+1][cj+1]==-1:
            ci,cj,cd = ci+1,cj,cd

        # 서쪽 한칸 이동
        elif 0<=(ci + 2) < R and 0 <= (cj - 2) < C and arr[ci - 1][cj - 1] == -1 and arr[ci][cj - 2] == -1 and \
                arr[ci + 1][cj - 2] == -1 and arr[ci + 1][cj - 1] == -1 and arr[ci + 2][cj - 1] == -1:
            ci,cj,cd = ci+1,cj-1,(cd+3)%4

        # 동쪽 한칸 이동
        elif 0 <= (ci + 2) < R and 0 <= (cj + 2) < C and arr[ci - 1][cj + 1] == -1 and arr[ci][cj + 2] == -1 and \
                arr[ci + 1][cj + 1] == -1 and arr[ci + 1][cj + 2] == -1 and arr[ci + 2][cj + 1] == -1:
            ci,cj,cd = ci+1,cj+1,(cd+5)%4

        # 아무곳으로도 움직일 수 없는 상태
        else:
            ni,nj,nd = ci,cj,cd
            break

    # 골렘 위치 격자안->fix / 격자밖->continue
    init_flag = 0
    for nni,nnj in ((ni-1,nj),(ni,nj+1),(ni+1,nj),(ni,nj-1)):
        if not (0<=nni<R and 0<=nnj<C):
            init_flag = 1
            break

    if init_flag == 1: # 초기화하고 다시 시작
        monster = dict()
        arr = [[-1]*C for _ in range(R)]
        continue
    else: # 현재 골렘 fix
        monster[k] = [(ni,nj),nd]
        for nni,nnj in ((ni,nj),(ni-1,nj),(ni,nj+1),(ni+1,nj),(ni,nj-1)):
            arr[nni][nnj] = k

    # 정령 이동 후 점수 누적
    q = [] # 게이트 누적
    finals = [] # 최하단 누적
    finals.append((ni+1,nj))
    q.append((ni+di[nd],nj+dj[nd]))

    while q:
        ci,cj = q.pop(0)
        for d in range(4):
            ni,nj = ci+di[d],cj+dj[d]
            if 0<=ni<R and 0<=nj<R and arr[ni][nj]!=-1 and arr[ci][cj]!=arr[ni][nj]: # 격자내 & 골룸 있고 & 나랑 다른 골룸이면
                nm = arr[ni][nj] # 넥스트 골룸의 인덱스
                finals.append((monster[nm][0][0]+1, monster[nm][0][1]))
                q.append((monster[nm][0][0]+di[monster[nm][1]], monster[nm][0][1]+dj[monster[nm][1]]))

    sorted_finals = sorted(finals, key=lambda x:(x[0]), reverse=True) # 큰->작
    ans += (sorted_finals[0][0] + 1)

print(ans)