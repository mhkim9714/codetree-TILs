# 최단 길이를 갖는 경로(path) 파악 ★★★★★
N,M,K = map(int, input().split())

# Grid 내의 각 위치마다 [공격력(0~5000; def input), 최근공격시점(0~K-1; def -1)
time = [[-1 for _ in range(M)] for _ in range(N)]
power = []
for _ in range(N):
    power.append(list(map(int, input().split())))

def bfs(si,sj,ei,ej):
    q = []
    visited = [[[] for _ in range(M)] for _ in range(N)]

    q.append((si, sj))
    visited[si][sj] = (si,sj)

    while q:
        ci, cj = q.pop(0)

        for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):  # 우(0), 하(1), 좌(2), 상(3)
            ni, nj = (ci + di) % N, (cj + dj) % M  # 다음 좌표 구하기

            if (ni,nj) == (ei,ej): # [레이저 공격]
                power[ei][ej] = max(power[ei][ej]-power[si][sj], 0)
                while True:
                    power[ci][cj] = max(power[ci][cj]-(power[si][sj]//2), 0)
                    relk.add((ci, cj))
                    ci,cj = visited[ci][cj]
                    if (ci,cj) == (si,sj):
                        return True # 최단 경로를 찾은 경우 레이저 공격을 수행하고 True를 반환

            if len(visited[ni][nj]) == 0 and power[ni][nj] > 0:
                q.append((ni, nj))
                visited[ni][nj] = (ci, cj)

    # 최단 경로를 못찾은 경우
    return False

def bomb(si,sj,ei,ej):
    power[ei][ej] -= power[si][sj]
    for (di,dj) in [(1,0),(-1,0),(0,1),(0,-1),(1,-1),(1,1),(-1,-1),(-1,1)]:
        ni,nj = (ei+di)%N,(ej+dj)%M
        if (ni,nj) != (si,sj) and power[ni][nj]>0:
            power[ni][nj] = max(power[ni][nj]-(power[si][sj]//2), 0)
            relk.add((ni, nj))


for k in range(K):
    relk = set()

    # [공격자 선정]: 공격력 낮은 -> 가장 최근 공격 포탑(time 큰) -> 행+열 큰 -> 열 큰
    attk_pow, attk_i, attk_j = 10000, -1, -1
    attk_candidate = []

    for i in range(N): # 공격력 갈리
        for j in range(M):
            if power[i][j] > 0:
                if power[i][j] < attk_pow:
                    attk_pow = power[i][j]
                    attk_candidate = [(i,j)]
                elif power[i][j] == attk_pow:
                    attk_candidate.append((i,j))

    if len(attk_candidate) == 0: # 공격자 없는 상황
        break
    elif len(attk_candidate) == 1: # 공격력으로 한명 추려진 상황
        attk_i, attk_j = attk_candidate[0]
        power[attk_i][attk_j] += (N+M)
    else:
        temp = []
        for (i,j) in attk_candidate:
            temp.append([time[i][j], i+j, j])
        sorted_temp = sorted(temp, key=lambda x: (x[0], x[1], x[2]), reverse=True) # 내림차순 정렬 (큰->작)
        attk_j = sorted_temp[0][-1]
        attk_i = sorted_temp[0][-2] - attk_j
        power[attk_i][attk_j] += (N+M)

    time[attk_i][attk_j] = k # 공격 시점 업데이트
    relk.add((attk_i, attk_j))

    # [공격대상 선정]: 공격력 높은 -> 가장 오래된 공격 포탑(time 작은) -> 행+열 작은 -> 열 작은 / 공격 포탑 제외
    tgt_pow, tgt_i, tgt_j = 0, -1, -1
    tgt_candidate = []

    for i in range(N):
        for j in range(M):
            if (i,j) != (attk_i,attk_j) and power[i][j] > 0:
                if power[i][j] > tgt_pow:
                    tgt_pow = power[i][j]
                    tgt_candidate = [(i,j)]
                elif power[i][j] == tgt_pow:
                    tgt_candidate.append((i, j))

    if len(tgt_candidate) == 0:  # 대상자 없는 상황
        break
    elif len(tgt_candidate) == 1:  # 공격력으로 한명 추려진 상황
        tgt_i, tgt_j = tgt_candidate[0]
    else:
        temp = []
        for (i, j) in tgt_candidate:
            temp.append([time[i][j], i + j, j])
        sorted_temp = sorted(temp, key=lambda x: (x[0], x[1], x[2])) # 오름차순 정렬 (작->큰)
        tgt_j = sorted_temp[0][-1]
        tgt_i = sorted_temp[0][-2] - tgt_j

    relk.add((tgt_i, tgt_j))

    # [공격]
    if bfs(attk_i, attk_j, tgt_i, tgt_j) is False: # [포탄 공격]
        bomb(attk_i, attk_j, tgt_i, tgt_j)

    # 포탑 정비
    for i in range(N):
        for j in range(M):
            if (i,j) not in relk and power[i][j] > 0:
                power[i][j] += 1

print(max(max(x) for x in power))