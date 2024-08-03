N,M,P,C,D = map(int,input().split())

Rr,Rc = map(int,input().split())
Rr,Rc = Rr-1,Rc-1 # 루돌프의 위치 좌표

arr = [[0]*N for _ in range(N)] # 산타의 위치 arr
santa = dict() # [(Sr,Sc),점수(디폴트0),탈락여부(생존0/탈락1),기절플래그(디폴트0/기절시2->1->0)]
for _ in range(P):
    Pn,Sr,Sc = map(int,input().split())
    santa[Pn] = [(Sr-1,Sc-1),0,0,0]
    arr[Sr-1][Sc-1] = Pn
santa = dict(sorted(santa.items()))

MAX_D = 3*(N**2)

# 상(0) 우(1) 하(2) 좌(3)
Pdr = [-1, 0, 1, 0]
Pdc = [0, 1, 0, -1]

def dist(r1,c1,r2,c2):
    return (r1-r2)**2 + (c1-c2)**2


for _ in range(M):
    # 1) 루돌프 이동
    min_d_R2S = MAX_D
    TSr,TSc = -1,-1

    for Pn, info in santa.items():
        if info[2]==0: # 생존한 산타에 대해서만 진행
            d_R2S = dist(Rr,Rc,info[0][0],info[0][1])
            if min_d_R2S > d_R2S: # 최단 거리일 때 업데이트
                min_d_R2S,TSr,TSc = d_R2S, info[0][0], info[0][1]
            elif min_d_R2S == d_R2S:
                if TSr < info[0][0]: # r좌표가 더 클 때 업데이트
                    min_d_R2S, TSr, TSc = d_R2S, info[0][0], info[0][1]
                elif TSr == info[0][0]:
                    if TSc < info[0][1]:
                        min_d_R2S, TSr, TSc = d_R2S, info[0][0], info[0][1] # [타겟 산타인 TSr,TSc 정해짐]

    min_8d = MAX_D
    NRr,NRc = -1,-1
    Rdr,Rdc = 0,0

    for dr,dc in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)):
        if min_8d > dist(TSr,TSc,Rr+dr,Rc+dc): # 최단 거리일 때 업데이트
            min_8d = dist(TSr,TSc,Rr+dr,Rc+dc)
            NRr,NRc = Rr+dr,Rc+dc
            Rdr,Rdc = dr,dc
    Rr,Rc = NRr,NRc # [루돌프가 움직여서 Rr,Rc가 바뀜]

    # 2) 루돌프 유발 충돌 처리 (변경 대상: santa dict, arr)
    if arr[Rr][Rc] > 0: # 루돌프가 이동한 자리에 산타가 있다면
        CPn,CSr,CSc = arr[Rr][Rc],Rr,Rc
        santa[CPn][1] += C # 점수
        santa[CPn][3] = 2 # 기절
        arr[CSr][CSc] = 0 # arr: 현재 좌표 삭제 반영
        NSr,NSc = CSr+C*Rdr,CSc+C*Rdc # 새로운 좌표 계산

        while True:
            if not (0<=NSr<N and 0<=NSc<N): # 새로운 좌표가 격자 밖인 경우 (santa:탈락처리)
                santa[CPn][2] = 1 # santa: 탈락 처리 반영
                break

            elif arr[NSr][NSc] == 0: # 새로운 좌표에 다른 산타가 없는 경우 (arr:새좌표로이동/ santa:좌표변경)
                santa[CPn][0] = (NSr,NSc)
                arr[NSr][NSc] = CPn
                break

            else: # 새로운 좌표에 다른 산타가 있는 경우 (arr:새좌표로이동/ santa:좌표변경/ 새로운CPn,CSr,CSc,NSr,NSc확보)
                santa[CPn][0] = (NSr,NSc)
                temp = arr[NSr][NSc]
                arr[NSr][NSc] = CPn
                CPn,CSr,CSc = temp,NSr,NSc
                NSr,NSc = CSr+Rdr,CSc+Rdc

    # 3) 산타의 움직임 (변경 대상: santa dict, arr)
    for CPn,info in santa.items():
        if info[2]==1 or info[3]>0: # 이미 탈락하거나 기절한 산타는 움직이지 않음
            continue

        r1,c1 = info[0][0],info[0][1]
        di = -1
        min_d_S2R = dist(Rr, Rc, r1, c1)

        for i in range(4):
            r2,c2 = r1+Pdr[i],c1+Pdc[i]
            if 0<=r2<N and 0<=c2<N and arr[r2][c2]==0: # 새로운 좌표의 조건: 격자내&산타없음
                if min_d_S2R > dist(Rr,Rc,r2,c2): # 최단 거리일 때 업데이트
                    min_d_S2R = dist(Rr,Rc,r2,c2)
                    di = i

        if di != -1: # 산타의 이동이 일어나는 경우
            if (r1+Pdr[di],c1+Pdc[di]) != (Rr,Rc): # 산타가 이동한 자리에 루돌프가 없다면
                santa[CPn][0] = (r1+Pdr[di],c1+Pdc[di])
                arr[r1][c1], arr[r1+Pdr[di]][c1+Pdc[di]] = 0, CPn

            # 4) 산타 유발 충돌 처리
            else:  # 산타가 이동한 자리에 루돌프가 있다면
                CSr, CSc = r1+Pdr[di], c1+Pdc[di]
                santa[CPn][1] += D  # 점수
                santa[CPn][3] = 2  # 기절
                arr[r1][c1] = 0  # arr: 현재 좌표 삭제 반영
                NSr, NSc = CSr + D * Pdr[(di+2)%4], CSc + D * Pdc[(di+2)%4]  # 새로운 좌표 계산

                while True:
                    if not (0 <= NSr < N and 0 <= NSc < N):  # 새로운 좌표가 격자 밖인 경우 (santa:탈락처리)
                        santa[CPn][2] = 1  # santa: 탈락 처리 반영
                        break

                    elif arr[NSr][NSc] == 0:  # 새로운 좌표에 다른 산타가 없는 경우 (arr:새좌표로이동/ santa:좌표변경)
                        santa[CPn][0] = (NSr, NSc)
                        arr[NSr][NSc] = CPn
                        break

                    else:  # 새로운 좌표에 다른 산타가 있는 경우 (arr:새좌표로이동/ santa:좌표변경/ 새로운CPn,CSr,CSc,NSr,NSc확보)
                        santa[CPn][0] = (NSr, NSc)
                        temp = arr[NSr][NSc]
                        arr[NSr][NSc] = CPn
                        CPn, CSr, CSc = temp, NSr, NSc
                        NSr, NSc = CSr + Pdr[(di+2)%4], CSc + Pdc[(di+2)%4]

    # 5) 모든 산타가 탈락했으면 게임 종료 (종료 조건) & 기절 조정
    end_flag = 1
    for Pn, info in santa.items():
        if info[2] == 0: # 한명이라도 생존해 있다면
            end_flag = 0
    if end_flag == 1:
        break

    for Pn, info in santa.items():
        info[3] = max(0, info[3]-1)
        if info[2] == 0:
            info[1] += 1

lst = [0] * (P+1)
for Pn, info in santa.items():
    lst[Pn] = info[1]
str = " ".join(map(str, lst[1:]))
print(str)