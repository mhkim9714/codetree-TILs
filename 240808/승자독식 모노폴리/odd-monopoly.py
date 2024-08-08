# 상(0) 하(1) 좌(2) 우(3)
di = [-1, 1, 0, 0]
dj = [0, 0, -1, 1]

n,m,k = map(int, input().split())
temp_arr = [list(map(int, input().split())) for _ in range(n)]
temp_dir = list(map(int, input().split()))

arr = [[[0,0] for _ in range(n)] for _ in range(n)]
player = dict() # [(좌표), 방향인덱스]

for i in range(n):
    for j in range(n):
        if temp_arr[i][j] != 0:
            player[temp_arr[i][j]] = [(i,j),temp_dir[temp_arr[i][j]-1]-1]
            arr[i][j] = [temp_arr[i][j],k]

priority = dict()
for i in range(1,m+1):
    up_priority = map(int, input().split())
    down_priority = map(int, input().split())
    left_priority = map(int, input().split())
    right_priority = map(int, input().split())
    priority[i] = [[x-1 for x in up_priority], [x-1 for x in down_priority], [x-1 for x in left_priority], [x-1 for x in right_priority]]


for turn in range(1,1000):
    move_direction = dict() # p_idx : 이동할 방향인덱스

    for p_idx, [(ci,cj),d] in player.items():
        buy_candidates = [] # 방향 인덱스 저장
        my_land = [] # 방향 인덱스 저장
        for dir in range(4):
            ni,nj = ci+di[dir],cj+dj[dir]
            if 0<=ni<n and 0<=nj<n and arr[ni][nj][0]==0:
                buy_candidates.append(dir)
            elif 0<=ni<n and 0<=nj<n and arr[ni][nj][0]==p_idx:
                my_land.append(dir)
        
        if len(buy_candidates)>0: # 독점 계약 진행
            for dir in priority[p_idx][d]:
                if dir in buy_candidates:
                    move_direction[p_idx] = dir
                    break
        else: # 자기 땅으로 이동
            for dir in priority[p_idx][d]:
                if dir in my_land:
                    move_direction[p_idx] = dir
                    break

    for p_idx, dir in move_direction.items():
        ci,cj = player[p_idx][0]
        ni,nj = ci+di[dir],cj+dj[dir]
        if arr[ni][nj][0] == 0: # 아무도 없다면 독점계약
            arr[ni][nj] = [p_idx,k+1]
            player[p_idx] = [(ni,nj),dir]
        elif arr[ni][nj][0] == p_idx: # 내 땅이었다면 계약 기간만 연장
            arr[ni][nj] = [p_idx,k+1]
            player[p_idx] = [(ni,nj),dir]
        else: # 다른 플레이어와 같은 땅으로 이동했다면 플레이어 삭제 진행
            if p_idx < arr[ni][nj][0]: # 나 생존
                del player[arr[ni][nj][0]]
                arr[ni][nj] = [p_idx,k+1]
                player[p_idx] = [(ni,nj),dir]
            else: # 나 삭제
                del player[p_idx]

    # 전체적으로 계약 기간 -1
    for i in range(n):
        for j in range(n):
            if arr[i][j][0] > 0:
                if arr[i][j][1] == 1:
                    arr[i][j] = [0,0]
                else:
                    arr[i][j][1] -= 1

    if len(player) == 1:
        print(turn)
        break

else:
    print(-1)