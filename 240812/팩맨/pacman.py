m,t = map(int, input().split())

pi,pj = map(int, input().split())
pi,pj = pi-1,pj-1

# ↑(0), ↖(1), ←(2), ↙(3), ↓(4), ↘(5), →(6), ↗(7)
di = [-1,-1,0,1,1,1,0,-1]
dj = [0,-1,-1,-1,0,1,1,1]

monster = dict()
num_alive = [[0 for _ in range(4)] for _ in range(4)] # 몬스터의 갯수 (살아있는 몬스터; 알 상태 제외)
num_dead = [[0 for _ in range(4)] for _ in range(4)] # 몬스터의 갯수 (죽은 몬스터)
for m_idx in range(m):
    r,c,d = map(int, input().split())
    monster[m_idx] = [(r-1,c-1), d-1, 0, -1] # [(좌표), 방향 인덱스, dormant(0몬/1알), dead(디폴트-1,2->1->0(삭제)]
    num_alive[r-1][c-1] += 1
nm = m

for _ in range(t):
    # 탈출 조건 : 살아있는 몬스터가 하나도 없을때 종료
    end_flag = 1
    for i in range(4):
        for j in range(4):
            if num_alive[i][j] > 0:
                end_flag = 0
    if end_flag == 1:
        print(0)
        break

    # 1. 몬스터 복제 시도 -> 아직은 alive에 반영 X
    for m_idx in list(monster.keys()):
        if monster[m_idx][3] == -1:
            monster[nm] = [monster[m_idx][0], monster[m_idx][1], 1, -1]
            nm += 1

    # 2. 몬스터 이동
    for m_idx, info in monster.items():
        if info[2]==1 or info[3]>0: # 알 상태거나 시체 상태일 때는 이동 불가
            continue

        (ci,cj),d = info[0], info[1]
        for _ in range(8):
            ni,nj = ci+di[d],cj+dj[d]
            if 0<=ni<4 and 0<=nj<4 and num_dead[ni][nj]==0 and (ni,nj)!=(pi,pj): # 이동 가능 조건
                info[0] = (ni,nj)
                info[1] = d
                num_alive[ci][cj] -= 1
                num_alive[ni][nj] += 1
                break
            d = (d+1)%8

    # 3. 팩맨 이동
    max_eat = -1
    eat_lst = []
    npi,npj = -1,-1

    for d1 in (0,2,4,6):
        ni1,nj1 = pi+di[d1],pj+dj[d1]
        if 0<=ni1<4 and 0<=nj1<4:
            for d2 in (0,2,4,6):
                ni2,nj2 = ni1+di[d2],nj1+dj[d2]
                if 0<=ni2<4 and 0<=nj2<4:
                    for d3 in (0,2,4,6):
                        ni3,nj3 = ni2+di[d3],nj2+dj[d3]
                        if 0<=ni3<4 and 0<=nj3<4:
                            lst = [(ni1,nj1),(ni2,nj2),(ni3,nj3)]
                            lst2set = list(set(lst))
                            eat = 0
                            for (i,j) in lst2set:
                                eat += num_alive[i][j]
                            if max_eat < eat:
                                max_eat = eat
                                eat_lst = lst2set
                                npi,npj = ni3,nj3

    for m_idx, info in monster.items():
        if info[2]==1 or info[3]>0: # 알 상태거나 시체 상태일 때는 먹히지 않음
            continue

        if info[0] in eat_lst:
            num_alive[info[0][0]][info[0][1]] -= 1
            num_dead[info[0][0]][info[0][1]] += 1
            info[3] = 2

    pi,pj = npi,npj

    # 4&5. 몬스터 시체 소멸 & 몬스터 복제 완성
    for m_idx in list(monster.keys()):
        if monster[m_idx][3] != -1: # 시체인 몬스터에 대해서
            if monster[m_idx][3] == 1:
                num_dead[monster[m_idx][0][0]][monster[m_idx][0][1]] -= 1
                del monster[m_idx]
            else:
                monster[m_idx][3] -= 1

        elif monster[m_idx][2] == 1: # 알이었던 몬스터에 대해서 -> 비로소 alive에 반영 O
            monster[m_idx][2] = 0
            num_alive[monster[m_idx][0][0]][monster[m_idx][0][1]] += 1

else:
    cnt = 0
    for i in range(4):
        for j in range(4):
            if num_alive[i][j] > 0:
                cnt += num_alive[i][j]
    print(cnt)