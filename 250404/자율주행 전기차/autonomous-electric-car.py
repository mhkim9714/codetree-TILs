n, m, battery = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(n)]
car_i, car_j = map(int, input().split())
car_i, car_j = car_i-1, car_j-1
passenger = dict()
for idx in range(1, m+1):
    si, sj, ei, ej = map(int, input().split())
    passenger[idx] = [(si-1, sj-1), (ei-1, ej-1)]

MAX_DIST = n**3

while True:  # O(400)
    # [정상종료] 승객 dict len=0이면 -> 현재 배터리 출력 후 break
    if len(passenger) == 0:
        print(battery)
        break

    # 1. 태울 승객 정하기 -> O(400)
    q = []
    visited = [[MAX_DIST for _ in range(n)] for _ in range(n)]

    q.append((car_i, car_j))
    visited[car_i][car_j] = 0

    while q:
        ci, cj = q.pop(0)
        for di, dj in [(-1,0), (0,1), (1,0), (0,-1)]:
            ni, nj = ci+di, cj+dj
            if 0<=ni<n and 0<=nj<n and arr[ni][nj]==0 and visited[ni][nj]==MAX_DIST:
                q.append((ni, nj))
                visited[ni][nj] = visited[ci][cj] + 1

    min_dist, min_i, min_j, pass_idx = MAX_DIST+1, n, n, -1
    for idx, info in passenger.items():
        if visited[info[0][0]][info[0][1]] < min_dist:
            min_dist, min_i, min_j, pass_idx = visited[info[0][0]][info[0][1]], info[0][0], info[0][1], idx
        elif visited[info[0][0]][info[0][1]] == min_dist:
            if info[0][0] < min_i:
                min_dist, min_i, min_j, pass_idx = visited[info[0][0]][info[0][1]], info[0][0], info[0][1], idx
            elif info[0][0] == min_i:
                if info[0][1] < min_j:
                    min_dist, min_i, min_j, pass_idx = visited[info[0][0]][info[0][1]], info[0][0], info[0][1], idx

    # [종료] 태울 승객 없으면 print(-1) break
    if min_dist == MAX_DIST:
        print(-1)
        break
    else:
        pass_i, pass_j = min_i, min_j

    # 2. 승객의 출발지로 가기 -> O(1)
    if min_dist >= battery:
        print(-1)
        break
    else:
        car_i, car_j, battery = pass_i, pass_j, battery-min_dist

    # 3. 승객의 도착지로 가기 -> O(400)
    q = []
    visited = [[MAX_DIST for _ in range(n)] for _ in range(n)]

    q.append((car_i, car_j))
    visited[car_i][car_j] = 0

    exit_flag = 0
    while q:
        if exit_flag == 1:
            break
        ci, cj = q.pop(0)
        for di, dj in [(-1,0), (0,1), (1,0), (0,-1)]:
            ni, nj = ci+di, cj+dj
            if 0<=ni<n and 0<=nj<n and arr[ni][nj]==0 and visited[ni][nj]==MAX_DIST:
                q.append((ni, nj))
                visited[ni][nj] = visited[ci][cj] + 1
                if (ni, nj) == passenger[pass_idx][1]:
                    exit_flag = 1
                    break

    if exit_flag == 0:
        print(-1)
        break
    else:
        if visited[passenger[pass_idx][1][0]][passenger[pass_idx][1][1]] > battery:
            print(-1)
            break
        else:
            car_i, car_j, battery = passenger[pass_idx][1][0], passenger[pass_idx][1][1], battery+visited[passenger[pass_idx][1][0]][passenger[pass_idx][1][1]]
            del passenger[pass_idx]

