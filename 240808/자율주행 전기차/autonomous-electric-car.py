n,m,battery = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(n)]

evi,evj = map(int, input().split())
evi,evj = evi-1,evj-1

passengers = dict()
for idx in range(m):
    si,sj,ei,ej = map(int, input().split())
    si,sj,ei,ej = si-1,sj-1,ei-1,ej-1
    passengers[idx] = [(si,sj),(ei,ej)]


def BFS(si,sj,ei=None,ej=None):
    q = []
    visited = [[-1 * ele for ele in row] for row in arr]

    q.append((si,sj))
    visited[si][sj] = 1

    while q:
        ci,cj = q.pop(0)
        for di,dj in ((-1,0),(0,1),(1,0),(0,-1)):
            ni,nj = ci+di,cj+dj
            if 0<=ni<n and 0<=nj<n and visited[ni][nj]==0: # 격자내 & 미방문
                q.append((ni,nj))
                visited[ni][nj] = visited[ci][cj]+1
                if ei is not None:
                    if (ni,nj) == (ei,ej):
                        return visited

    return visited


end_flag = 0
while passengers:
    # 태울 손님 선택
    min_d,min_i,min_j = 2*(n**2), 2*n, 2*n
    t_idx = -1
    distance = BFS(evi,evj)

    for idx, info in passengers.items():
        dist = distance[info[0][0]][info[0][1]]-1
        if min_d > dist:
            min_d, min_i, min_j = dist, info[0][0], info[0][1]
            t_idx = idx
        elif min_d == dist:
            if min_i > info[0][0]:
                min_d, min_i, min_j = dist, info[0][0], info[0][1]
                t_idx = idx
            elif min_i == info[0][0]:
                if min_j > info[0][1]:
                    min_d, min_i, min_j = dist, info[0][0], info[0][1]
                    t_idx = idx

    si,sj = passengers[t_idx][0]
    ei,ej = passengers[t_idx][1]

    # 태울 손님에게 차량 이동
    evi,evj = si,sj
    battery -= min_d
    if battery <= 0:
        end_flag = 1
        break

    # 손님의 목적지까지 운행
    dist_to_destination = BFS(si,sj,ei,ej)[ei][ej]-1
    if battery >= dist_to_destination: # 무사히 이동
        evi,evj = ei,ej
        battery += dist_to_destination
        del passengers[t_idx]
    else: # 이동하지 못하고 종료
        end_flag = 1
        break

if end_flag == 1:
    print(-1)
else:
    print(battery)