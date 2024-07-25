# 예외케이스: 1222222223 해서 4 없이 바로 다음 1과 이어지는 경우!!!!!!!!!!! ★★★★★ 이 경우가 계속 코너케이스로 있었던 거야!!!!!!!!!

n,m,k = map(int, input().split())
arr = []
for _ in range(n):
    arr.append(list(map(int, input().split())))

# 방향: 우(0), 상(1), 좌(2), 하(3)
bdi = [0, -1, 0, 1]
bdj = [1, 0, -1, 0]

# 공 던져지는 순서 미리 정해놓기 (4n회) -> (si,sj,방향)
ball = []
for i in range(n):
    ball.append((i,0,0))
for i in range(n):
    ball.append((n-1,i,1))
for i in range(n-1,-1,-1):
    ball.append((i,n-1,2))
for i in range(n-1,-1,-1):
    ball.append((0,i,3))

from collections import deque
def bfs(si,sj,team_n):
    q = []
    team = deque()

    q.append((si,sj))
    team.append((si,sj))
    visited[si][sj] = 1
    arr[si][sj] = team_n

    while q:
        ci,cj = q.pop(0)
        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = ci+di, cj+dj
            if 0<=ni<n and 0<=nj<n and visited[ni][nj]==0 and arr[ni][nj] in [2,3]: # 범위내, 미방문, 1->3만 차단
                if (ci,cj) == (si,sj) and arr[ni][nj] == 3:
                    continue
                else:
                    q.append((ni,nj))
                    team.append((ni,nj))
                    visited[ni][nj] = 1
                    arr[ni][nj] = team_n
    teams[team_n] = team

# 팀 짜두기: dictionary {team_n:deque((헤드좌표)(미들좌표)(꼬리좌표))} / arr의 숫자들은 싹다 team_n로 대체해주기
visited = [[0 for _ in range(n)] for _ in range(n)]
team_n = 5
teams = {}
for i in range(n):
    for j in range(n):
        if arr[i][j] == 1:
            bfs(i,j,team_n)
            team_n += 1

ans = 0
for rnd in range(k):
    # 각 팀 이동
    for team_n, team in teams.items():
        # 꼬리 먼저 이동: deque에서 pop하고 그 좌표에 있는 arr값을 4로 만들어 줌
        ei,ej = team.pop()
        arr[ei][ej] = 4
        # 머리 이동: 머리 좌표의 adj 중 arr 4값인 곳의 좌표를 얻어와서 deque에 appendleft
        si,sj = team[0]
        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = si+di, sj+dj
            if 0<=ni<n and 0<=nj<n and arr[ni][nj] == 4:
                team.appendleft((ni,nj))
                arr[ni][nj] = team_n
                break

    # 라운드마다 공 던짐
    si,sj,dir = ball[rnd % (4*n)]

    # 사람 맞으면 점수 획득 & 방향 반전
    ci,cj = si,sj
    for _ in range(n):
        if arr[ci][cj] > 4: # 사람 맞은 경우
            team_n = arr[ci][cj]
            # 점수 구하기
            score = teams[team_n].index((ci,cj)) + 1
            ans += (score * score)
            # 해당 팀 머리 꼬리 반전
            teams[team_n].reverse()
            break
        else: # 안맞은 경우 다음 좌표로 이동
            ci,cj = ci+bdi[dir], cj+bdj[dir]

print(ans)