def gravity():
    for j in range(n):
        for i in range(n-1, -1, -1):
            if arr[i][j] in [-2, -1]:
                continue

            to_i = i
            while True:
                n_to_i = to_i + 1
                if 0 <= n_to_i < n:
                    if arr[n_to_i][j] >= -1:  # 돌이나 다른 색깔 폭탄이 있는 경우
                        break
                    else:  # 없는 경우
                        to_i = n_to_i
                else:
                    break

            if i != to_i:
                arr[to_i][j] = arr[i][j]
                arr[i][j] = -2


n, m = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(n)]  # -2(빈공간), -1(검), 0(빨), 1~m(색깔 폭탄)

score = 0
while True:
    # 1. 모든 폭탄 묶음 찾기 -> 그 중 크기가 가장 큰 폭탄 묶음 찾기 (BFS) -> O(400)
    bombs = []  # [좌표 리스트, 빨간색 갯수, 기준점 좌표(빨강X 중에 i최대, j최소)]
    visited = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if arr[i][j] <= 0 or visited[i][j] == 1:
                continue

            color = arr[i][j]

            q = [(i, j)]
            visited[i][j] = 1
            coords = [(i, j)]
            red_coords = []
            max_i, min_j = i, j

            while q:
                ci, cj = q.pop(0)
                for di, dj in [(-1,0),(0,1),(1,0),(0,-1)]:
                    ni, nj = ci+di, cj+dj
                    if 0<=ni<n and 0<=nj<n and visited[ni][nj]==0:

                        if arr[ni][nj] == color:  # 같은색
                            q.append((ni, nj))
                            visited[ni][nj] = 1
                            coords.append((ni, nj))
                            if ni > max_i:
                                max_i, min_j = ni, nj
                            elif ni == max_i:
                                if nj < min_j:
                                    max_i, min_j = ni, nj

                        elif arr[ni][nj] == 0:  # 빨간색
                            q.append((ni, nj))
                            visited[ni][nj] = 1
                            coords.append((ni, nj))
                            red_coords.append((ni, nj))

            if len(coords) >= 2:
                bombs.append([coords, len(red_coords), (max_i, min_j)])
            for ri, rj in red_coords:
                visited[ri][rj] = 0

    # [종료] 폭탄 묶음 갯수=0 -> break
    if len(bombs) == 0:
        break

    max_bomb, min_red, max_bi, min_bj = [], n**2+1, -1, n
    for coords, cnt_red, base_coord in bombs:
        if len(coords) > len(max_bomb):
            max_bomb, min_red, max_bi, min_bj = coords, cnt_red, base_coord[0], base_coord[1]
        elif len(coords) == len(max_bomb):
            if cnt_red < min_red:
                max_bomb, min_red, max_bi, min_bj = coords, cnt_red, base_coord[0], base_coord[1]
            elif cnt_red == min_red:
                if base_coord[0] > max_bi:
                    max_bomb, min_red, max_bi, min_bj = coords, cnt_red, base_coord[0], base_coord[1]
                elif base_coord[0] == max_bi:
                    if base_coord[1] < min_bj:
                        max_bomb, min_red, max_bi, min_bj = coords, cnt_red, base_coord[0], base_coord[1]

    # 2. 선택된 폭탄 묶음에 해당하는 폭탄 제거 -> len**2만큼 score 누적
    score += len(max_bomb) ** 2
    for i, j in max_bomb:
        arr[i][j] = -2

    # 그 후 중력 작용 (돌 제외) -> 중력은 따로 함수를 만드는게 좋을 듯
    gravity()

    # 3. 반시계 방향 90도 격자 회전
    new_arr = [[-2 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            new_arr[n-1-j][i] = arr[i][j]
    arr = new_arr

    # 4. 다시 중력 작용 (same)
    gravity()

print(score)

