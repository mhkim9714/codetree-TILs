Q = int(input())
command = [list(map(int, input().split())) for _ in range(Q)]
INF = 1e10


def get_smallest_node():
    min_dist = INF+1
    idx = -1
    for i in range(n):
        if distance[i] < min_dist and not visited[i]:
            min_dist = distance[i]
            idx = i
    return idx


def dijkstra(start):
    '''
    모든 노드에 대해 반복,
        1. 방문 처리 되지 않은 노드 중 -> 입력된 거리가 가장 짧은 노드 선택
        2. 해당 노드를 방문 처리
        3. 해당 노드를 기준으로 연결된 노드에 대해 거리를 구했을 때, 기존에 입력된 값보다 작으면 거리를 갱신
    '''
    global distance, visited
    distance[start] = 0
    visited[start] = True

    for end, weight in graph[start].items():
        distance[end] = weight

    for _ in range(n):
        now = get_smallest_node()
        visited[now] = True
        for end, weight in graph[now].items():
            if distance[now] + weight < distance[end]:
                distance[end] = distance[now] + weight


trip = dict()
for cmd in command:
    if cmd[0] == 100:  # 코드트리 랜드 건설
        n, m = cmd[1], cmd[2]

        graph = [dict() for _ in range(n)]  # 각 시작노드당, {도착노드:간선가중치, ...}
        distance = [INF] * n
        visited = [False] * n

        for cnt in range((len(cmd)-3)//3):
            i = 3 * (cnt+1)
            v, u, w = cmd[i], cmd[i+1], cmd[i+2]
            if v == u:
                continue
            # 정방향 (v->u)
            if u in graph[v].keys():
                graph[v][u] = min(graph[v][u], w)
            else:
                graph[v][u] = w
            # 역방향 (u->v)
            if v in graph[u].keys():
                graph[u][v] = min(graph[u][v], w)
            else:
                graph[u][v] = w

        dijkstra(0)

    elif cmd[0] == 200:  # 여행 상품 생성
        idx, revenue, dest = cmd[1], cmd[2], cmd[3]
        trip[idx] = [dest, revenue, distance[dest]]  # [도착지, revenue, cost]

    elif cmd[0] == 300:  # 여행 상품 취소
        if cmd[1] in trip.keys():
            del trip[cmd[1]]

    elif cmd[0] == 400:  # 최적의 여행 상품 판매
        max_profit, min_idx = 0, INF
        for idx, info in trip.items():
            profit = info[1] - info[2]
            if profit < 0:
                continue

            if max_profit < profit:
                max_profit, min_idx = profit, idx
            elif max_profit == profit:
                if min_idx > idx:
                    max_profit, min_idx = profit, idx

        if min_idx == INF:
            print(-1)
        else:
            print(min_idx)
            del trip[min_idx]

    else:  # 여행 상품의 출발지 변경
        distance = [INF] * n
        visited = [False] * n
        dijkstra(cmd[1])

        for idx, info in trip.items():
            info[2] = distance[info[0]]

