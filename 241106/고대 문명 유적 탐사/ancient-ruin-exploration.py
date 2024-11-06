import copy

K,M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(5)]
numbers = list(map(int, input().split()))


def get_treasure(grid):
    visited = [[0 for _ in range(5)] for _ in range(5)]
    return_list = []

    for i in range(5):
        for j in range(5):
            if visited[i][j] == 0:
                # BFS 시작
                q = [(i,j)]
                visited[i][j] = 1
                cur_val = grid[i][j]
                this_list = [(i,j)]

                while q:
                    ci,cj = q.pop(0)
                    for di,dj in ((-1,0),(0,1),(1,0),(0,-1)):
                        ni,nj = ci+di, cj+dj
                        if 0<=ni<5 and 0<=nj<5 and visited[ni][nj]==0 and grid[ni][nj]==cur_val:
                            q.append((ni,nj))
                            visited[ni][nj] = 1
                            this_list.append((ni,nj))

                if len(this_list) >= 3:
                    return_list.extend(this_list)

    return return_list


ans_list = []
for _ in range(K):  # 10
    ans = 0

    # 1) 탐사 진행
    max_value, min_angle, min_i, min_j = -1, 360, 10, 10
    missing = []

    for i in range(5):
        for j in range(5):  # 25 -> 250
            if i-1<0 or j-1<0 or i+1>=5 or j+1>=5: # 중심 좌표를 i,j라고 할 때 3x3이 격자를 넘어가는 경우 제외
                continue

            for ang in [90,180,270]:  # 3 -> 750
                # 회전 수행
                narr = copy.deepcopy(arr)
                if ang == 90:
                    for ii in range(i-1,i+2):
                        for jj in range(j-1,j+2):  # 9 -> 6750
                            move_i = ii-(i-1)
                            move_j = jj-(j-1)
                            narr[i-1+move_j][j-1+2-move_i] = arr[i-1+move_i][j-1+move_j]
                elif ang == 180:
                    for ii in range(i-1,i+2):
                        for jj in range(j-1,j+2):
                            move_i = ii-(i-1)
                            move_j = jj-(j-1)
                            narr[i-1+2-move_i][j-1+2-move_j] = arr[i-1+move_i][j-1+move_j]
                else:
                    for ii in range(i-1,i+2):
                        for jj in range(j-1,j+2):
                            move_i = ii-(i-1)
                            move_j = jj-(j-1)
                            narr[i-1+2-move_j][j-1+move_i] = arr[i-1+move_i][j-1+move_j]

                # 유물 획득 시도
                temp_list = get_treasure(narr)  # 25 -> 168750 (10^5)

                if len(temp_list) > max_value:
                    max_value, min_angle, min_i, min_j = len(temp_list), ang, i, j
                    missing = temp_list
                elif len(temp_list) == max_value:
                    if ang < min_angle:
                        max_value, min_angle, min_i, min_j = len(temp_list), ang, i, j
                        missing = temp_list
                    elif ang == min_angle:
                        if j < min_j:
                            max_value, min_angle, min_i, min_j = len(temp_list), ang, i, j
                            missing = temp_list
                        elif j == min_j:
                            if i < min_i:
                                max_value, min_angle, min_i, min_j = len(temp_list), ang, i, j
                                missing = temp_list

    # 선택된 중심점, 각도 기준으로 최종 회전 진행
    narr = copy.deepcopy(arr)
    if min_angle == 90:
        for ii in range(min_i-1, min_i+2):
            for jj in range(min_j-1, min_j+2):
                move_i = ii-(min_i-1)
                move_j = jj-(min_j-1)
                narr[min_i-1+move_j][min_j-1+2-move_i] = arr[min_i-1+move_i][min_j-1+move_j]
    elif min_angle == 180:
        for ii in range(min_i-1, min_i+2):
            for jj in range(min_j-1, min_j+2):
                move_i = ii-(min_i-1)
                move_j = jj-(min_j-1)
                narr[min_i-1+2-move_i][min_j-1+2-move_j] = arr[min_i-1+move_i][min_j-1+move_j]
    else:
        for ii in range(min_i-1, min_i+2):
            for jj in range(min_j-1, min_j+2):
                move_i = ii-(min_i-1)
                move_j = jj-(min_j-1)
                narr[min_i-1+2-move_j][min_j-1+move_i] = arr[min_i-1+move_i][min_j-1+move_j]
    arr = narr

    # 2) 종료 조건
    if max_value == 0:
        break

    # 3) 유물 획득
    while True:
        ans += len(missing)
        missing.sort(key=lambda x:(x[1], -x[0]))
        cnt = 0
        for mi,mj in missing:
            arr[mi][mj] = numbers[cnt]
            cnt += 1

        numbers = numbers[len(missing):]
        missing = []

        # 다시 유물 획득 되는지 확인
        temp_list = get_treasure(arr)

        if len(temp_list) == 0:
            break
        else:
            missing = temp_list

    ans_list.append(str(ans))


ans_str = ' '.join(ans_list)
print(ans_str)