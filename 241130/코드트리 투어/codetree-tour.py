import heapq

INF = 1e10
MAX_ITEM = 30001

Q = int(input())
command = [list(map(int, input().split())) for _ in range(Q)]

pq = []
is_made = [False] * MAX_ITEM
is_cancelled = [False] * MAX_ITEM
class Packages:
    def __init__(self, id, revenue, dest, profit):
        self.id = id
        self.revenue = revenue
        self.dest = dest
        self.profit = profit

    def __lt__(self, other):  # less than을 정의하는 기준 -> 우선적으로 선택할 내용
        if self.profit == other.profit:
            return self.id < other.id  # 우리는 id가 더 작은걸 우선적으로 생각
        return self.profit > other.profit  # 우리는 profit이 더 큰걸 우선적으로 생각


def dijkstra(start):
    global distance
    q = []
    heapq.heappush(q, (0, start))
    distance[start] = 0

    while q:
        dist, now = heapq.heappop(q)

        if distance[now] < dist:
            continue

        for end, weight in graph[now].items():
            if dist + weight < distance[end]:
                distance[end] = dist + weight
                heapq.heappush(q, (dist+weight, end))


for cmd in command:
    if cmd[0] == 100:  # 코드트리 랜드 건설
        n, m = cmd[1], cmd[2]
        graph = [dict() for _ in range(n)]  # 각 시작노드당, {도착노드:간선가중치, ...}
        distance = [INF] * n

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
        heapq.heappush(pq, Packages(cmd[1], cmd[2], cmd[3], cmd[2]-distance[cmd[3]]))  # id, revenue, dest, profit
        is_made[cmd[1]] = True

    elif cmd[0] == 300:  # 여행 상품 취소
        if is_made[cmd[1]]:
            is_cancelled[cmd[1]] = True

    elif cmd[0] == 400:  # 최적의 여행 상품 판매
        while pq:
            p = pq[0]
            if p.profit < 0:
                print(-1)
                break

            heapq.heappop(pq)
            if is_cancelled[p.id]:
                continue
            else:
                print(p.id)
                break
        else:
            print(-1)

    else:  # 여행 상품의 출발지 변경 (10^7)
        distance = [INF] * n
        dijkstra(cmd[1])

        temp = []
        while pq:
            temp.append(heapq.heappop(pq))

        pq = []
        for p in temp:
            heapq.heappush(pq, Packages(p.id, p.revenue, p.dest, p.revenue-distance[p.dest]))  # id, revenue, dest, profit


