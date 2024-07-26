N,M,K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
participant = []
for _ in range(M):
    ti,tj = map(int, input().split())
    participant.append((ti-1,tj-1))
ti,tj = map(int, input().split())
exi,exj = ti-1, tj-1

def distance(si,sj,ei,ej):
    return abs(si-ei)+abs(sj-ej)

def square():
    # optimal 정사각형의 변 길이 구하기
    temp = []
    for i,j in participant:
        temp.append(max(abs(i-exi), abs(j-exj)))
    opt_l = min(temp)

    for si in range(N):
        for sj in range(N):
            if exi-si<0 or exj-sj<0:
                continue
            l = max(exi-si, exj-sj)
            while l <= opt_l:
                ei,ej = si+l,sj+l
                if 0<=ei<N and 0<=ej<N:
                    for ci,cj in participant:
                        if si<=ci<=ei and sj<=cj<=ej:
                            return si,sj,l
                l += 1
    # 이런 일은 없음
    return -1,-1,-1


ans = 0
for _ in range(K):
    # 참가자 동시 이동
    new_participant = []
    for i, (ci,cj) in enumerate(participant):
        min_d = distance(ci,cj,exi,exj) # 현재 참가자의 좌표와 출구까지의 거리
        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = ci+di,cj+dj
            if 0<=ni<N and 0<=nj<N and arr[ni][nj]==0 and distance(ni,nj,exi,exj)<min_d: # 이동하는 경우
                if (ni,nj) == (exi,exj): # 참가자가 exit을 통해 탈출하는 경우
                    ans += 1
                    break
                new_participant.append((ni,nj))
                ans += 1
                break
        else:
            new_participant.append((ci,cj))
    participant = new_participant

    # 탈출 조건: 모든 참가자가 exit을 통해 탈출했을때 종료
    if len(participant) == 0:
        break

    # 미로 회전 (grid O, exit, 참가자 모두 처리)
    narr = [x[:] for x in arr]
    new_participant = [x for x in participant]
    si,sj,l = square() # 정사각형의 좌상단 좌표, 정사각형의 변 길이

    nexi,nexj = exi,exj
    for i in range(l+1):
        for j in range(l+1):
            narr[si+j][sj+l-i] = max(arr[si+i][sj+j]-1, 0)
            # exit 처리 (1회)
            if (si+i,sj+j) == (exi,exj):
                nexi,nexj = si+j,sj+l-i
            # 참가자 처리 (속하는 모든 참가자들에 대해 처리)
            for idx, (ci,cj) in enumerate(participant):
                if (si+i,sj+j) == (ci,cj):
                    new_participant[idx] = (si+j,sj+l-i)

    arr = narr
    participant = new_participant
    exi,exj = nexi,nexj

print(ans)
print(f'{exi+1} {exj+1}')