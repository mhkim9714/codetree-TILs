n,m,battery = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(n)]
car_i,car_j = map(int, input().split())
car_i,car_j = car_i-1,car_j-1
people = dict()
for idx in range(1,m+1):
    x_s,y_s,x_e,y_e = map(int, input().split())
    people[idx] = [(x_s-1,y_s-1),(x_e-1,y_e-1)]

INF = 1e+6

def BFS(si,sj,ei,ej):
    q = []
    visited = [[INF for _ in range(n)] for _ in range(n)]

    q.append((si,sj))
    visited[si][sj] = 0

    while q:
        ci,cj = q.pop(0)
        for di,dj in ((-1,0),(0,1),(1,0),(0,-1)):
            ni,nj = ci+di,cj+dj
            if 0<=ni<n and 0<=nj<n and visited[ni][nj]==INF and arr[ni][nj]==0:
                q.append((ni,nj))
                visited[ni][nj] = visited[ci][cj]+1
                if (ni,nj) == (ei,ej):
                    return visited[ei][ej]

    return visited[ei][ej]


while True:
    if len(people) == 0:
        print(battery)
        break

    # 태울 승객 정하기
    dist, pi, pj, pidx = INF, n, n, -1
    for idx, info in people.items():
        d_c2p = BFS(car_i,car_j,info[0][0],info[0][1])
        if dist > d_c2p:
            dist, pi, pj, pidx = d_c2p, info[0][0], info[0][1], idx
        elif dist == d_c2p:
            if pi > info[0][0]:
                dist, pi, pj, pidx = d_c2p, info[0][0], info[0][1], idx
            elif pi == info[0][0]:
                if pj > info[0][1]:
                    dist, pi, pj, pidx = d_c2p, info[0][0], info[0][1], idx

    # 선택된 승객 태우기
    if battery > dist:
        battery -= dist
        car_i,car_j = pi,pj
    else:
        print(-1)
        break

    # 선택된 승객 목적지까지 모시기
    d_s2e = BFS(pi,pj,people[pidx][1][0],people[pidx][1][1])
    if battery >= d_s2e:
        battery += d_s2e
        car_i,car_j = people[pidx][1][0],people[pidx][1][1]
        del people[pidx]
    else:
        print(-1)
        break