import heapq

INF = int(1e9)
departure = 0
packages = dict() # [출발, 도착, cost, revenue]

def dijkstra(start, n):
    q = []
    distance = [INF] * (n)

    heapq.heappush(q, (0,start)) # (cost,tgt_node)
    distance[start] = 0

    while q:
        dist,now = heapq.heappop(q) # 최단 거리가 가장 짧은 노드 pop
        if distance[now] < dist: # 해당 노드가 이미 처리된 적이 있는 노드라면 무시
            continue
        for i in graph[now]: #
            cost = dist + i[1]
            if cost < distance[i[0]]: # now 노드를 거쳐서 다른 노드로 이동하는 거리가 더 짧은 경우 업데이트
                distance[i[0]] = cost
                heapq.heappush(q, (cost,i[0]))

    return distance

Q = int(input())
for _ in range(Q):
    command = list(map(int, input().split()))

    if command[0] == 100: # 코드트리 랜드 건설
        n,m = command[1], command[2]
        graph = [[] for i in range(n)]
        arr = [[INF]*n for _ in range(n)]

        for i in range(m):
            src, tgt, cost = command[3*(i+1):3*(i+2)]
            if src != tgt:
                val = min(cost, arr[src][tgt], arr[tgt][src])
                arr[src][tgt], arr[tgt][src] = val, val

        for i in range(n):
            for j in range(n):
                if arr[i][j] < INF:
                    graph[i].append((j,arr[i][j]))

    elif command[0] == 200: # 여행 상품 생성
        p_id,revenue,dest = command[1:]
        distance = dijkstra(departure, n)
        packages[p_id] = [departure, dest, distance[dest], revenue]

    elif command[0] == 300: # 여행 상품 취소
        if command[1] in packages.keys():
            del packages[command[1]]

    elif command[0] == 400: # 최적의 여행 상품 판매
        candidates = []
        for p_id, info in packages.items():
            if info[2] == INF or info[2] > info[3]: # 판매 불가 상품 조건
                continue
            else:
                candidates.append((info[3]-info[2], p_id))

        if len(candidates) > 0:
            sorted_candidates = sorted(candidates, key=lambda x:(x[0],-x[1]), reverse=True) # 큰->작
            selected_p_id = sorted_candidates[0][1]
            print(selected_p_id)
            del packages[selected_p_id]
        else:
            print(-1)

    elif command[0] == 500: # 여행 상품의 출발지 변경
        departure = command[1]
        for p_id, info in packages.items():
            distance = dijkstra(departure, n)
            packages[p_id] = [departure, info[1], distance[info[1]], info[3]]