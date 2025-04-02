n, m = map(int, input().split())
tmp = [list(map(int, input().split())) for _ in range(n)]

people = dict()
for idx in range(1, m+1):
    conv_i, conv_j = map(int, input().split())
    people[idx] = [(-1, -1), (conv_i-1, conv_j-1)]

basecamp = []
arr = [[0 for _ in range(n)] for _ in range(n)]
for i in range(n):
    for j in range(n):
        if tmp[i][j] == 1:
            basecamp.append((i, j))

# 상0 좌1 우2 하3
di = [-1, 0, 0, 1]
dj = [0, -1, 1, 0]

MAX_DIST = 15 ** 3
time = 1
while True:
    # to_block_idx 초기화
    to_block_idx = []

    # 1. 격자에 있는 모든 사람에 대해 편의점에 가까워지도록 1칸 움직이기 (상좌우하) -> 최종 O(6750)
    for idx, info in people.items():  # O(30)
        if info[0] == (-1, -1):
            continue

        # BFS 수행 -> O(225)
        q = []
        visited = [[MAX_DIST for _ in range(n)] for _ in range(n)]

        q.append((info[1][0], info[1][1]))
        visited[info[1][0]][info[1][1]] = 0

        while q:
            ci, cj = q.pop(0)
            for d in range(4):
                ni, nj = ci+di[d], cj+dj[d]
                if 0<=ni<n and 0<=nj<n and arr[ni][nj]==0 and visited[ni][nj]==MAX_DIST:
                    q.append((ni, nj))
                    visited[ni][nj] = visited[ci][cj] + 1

        # 최단거리 좌표 구하기 -> O(4)
        min_dist, ni, nj = MAX_DIST+1, -1, -1
        for d in range(4):
            i, j = info[0][0]+di[d], info[0][1]+dj[d]
            if 0<=i<n and 0<=j<n and arr[i][j]==0 and visited[i][j]<min_dist:
                min_dist, ni, nj = visited[i][j], i, j

        info[0] = (ni, nj)

        # 2. 만약 편의점에 도착한다면 -> to_block_idx에 idx 추가
        if info[0] == info[1]:
            to_block_idx.append(idx)

    # to_block_idx 처리
    for idx in to_block_idx:
        arr[people[idx][1][0]][people[idx][1][1]] = 1
        del people[idx]

    # 종료 조건 -> 모든 사람이 다 편의점에 도착하면 종료
    if len(people) == 0:
        break

    # 3. t<=m이면, t번 사람 베캠에 배치
    if time <= m:
        # BFS 수행 -> O(225)
        q = []
        visited = [[MAX_DIST for _ in range(n)] for _ in range(n)]

        q.append(people[time][1])
        visited[people[time][1][0]][people[time][1][1]] = 0

        while q:
            ci, cj = q.pop(0)
            for d in range(4):
                ni, nj = ci+di[d], cj+dj[d]
                if 0<=ni<n and 0<=nj<n and arr[ni][nj]==0 and visited[ni][nj]==MAX_DIST:
                    q.append((ni, nj))
                    visited[ni][nj] = visited[ci][cj] + 1

        min_dist, min_row, min_col = MAX_DIST+1, n, n
        for bi, bj in basecamp:
            if visited[bi][bj] < min_dist:
                min_dist, min_row, min_col = visited[bi][bj], bi, bj
            elif visited[bi][bj] == min_dist:
                if bi < min_row:
                    min_dist, min_row, min_col = visited[bi][bj], bi, bj
                elif bi == min_row:
                    if bj < min_col:
                        min_dist, min_row, min_col = visited[bi][bj], bi, bj

        people[time][0] = (min_row, min_col)
        # 이 베캠 좌표 block 하기
        arr[min_row][min_col] = 1
        basecamp.remove((min_row, min_col))

    time += 1

print(time)
