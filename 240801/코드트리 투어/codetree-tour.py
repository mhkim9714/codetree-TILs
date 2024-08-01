import sys
import heapq

INF = float('inf')
MAX_ID = 30005
isMade = [False] * MAX_ID
isCancelled = [False] * MAX_ID

n,m = 0,0
distance = []
departure = 0
pq = []
class Package:
    def __init__(self, id, revenue, dest, profit):
        self.id = id
        self.revenue = revenue
        self.dest = dest
        self.profit = profit

    def __lt__(self, other): # x<y를 판단하는 기준을 정의 (less than)
        if self.profit == other.profit:
            return self.id < other.id
        return self.profit > other.profit

def dijkstra(start):
    q = []

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

        distance = [INF] * n
        dijkstra(departure)

    elif command[0] == 200: # 여행 상품 생성
        p_id,revenue,dest = command[1:]
        heapq.heappush(pq, Package(p_id,revenue,dest,revenue-distance[dest]))
        isMade[p_id] = True

    elif command[0] == 300: # 여행 상품 취소 (hq에서 특정 인덱스 값 빼기 어려우니까 cancelled 여부를 저장)
        if isMade[command[1]]:
            isCancelled[command[1]] = True

    elif command[0] == 400: # 최적의 여행 상품 판매
        while pq:
            p = pq[0]
            if p.profit < 0:
                print(-1)
                break
            heapq.heappop(pq)
            if not isCancelled[p.id]:
                print(p.id)
                break
        else:
            print(-1)

    elif command[0] == 500: # 여행 상품의 출발지 변경
        departure = command[1]
        distance = [INF] * n
        dijkstra(departure)

        temp_packages = []
        while pq:
            temp_packages.append(heapq.heappop(pq))
        for p in temp_packages:
            heapq.heappush(pq, Package(p.id,p.revenue,p.dest,p.revenue-distance[p.dest]))


# 시간 초과 잡기
# 1) departure 갱신될때마다 다익스트라 한번만 돌려줌
# 2) sorting operation 제거
# 3) packages도 dictionary 말고 heapq (우선순위 큐)으로 구현: 패키지 취소의 operation은 heapq에선 지원이 안되므로 isCancelled라는 True/False list를 따로 활용한다.