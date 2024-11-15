# 그래프 생성
node_idx = [i for i in range(1,34)]  # len=33의 일차원 리스트 (1~33)
node_value = [-1,
              0,2,4,6,8,
              10,13,16,19,25,
              26,27,28,30,12,
              14,16,18,20,22,
              24,26,28,22,24,
              30,35,40,32,34,
              36,38,0]  # len=1+33
blue_node_idx = [6,14,19]
blue_edge = [7,13,24]
edge = [-1,
        2,3,4,5,6,
        15,8,9,10,26,
        10,11,12,29,16,
        17,18,19,20,21,
        22,23,14,25,10,
        27,28,33,30,31,
        32,28,-1]  # len=1+33

move_list = list(map(int, input().split()))


def move(cur_node, mv_cnt):
    if cur_node in blue_node_idx:
        cur_node = blue_edge[blue_node_idx.index(cur_node)]
        mv_cnt -= 1

    for _ in range(mv_cnt):
        cur_node = edge[cur_node]
        if cur_node == 33:
            break

    return cur_node


max_score = -1
for h1 in range(1,4+1):
    for h2 in range(1,4+1):
        for h3 in range(1,4+1):
            for h4 in range(1,4+1):
                for h5 in range(1,4+1):
                    for h6 in range(1,4+1):
                        for h7 in range(1,4+1):
                            for h8 in range(1,4+1):
                                for h9 in range(1,4+1):
                                    for h10 in range(1,4+1):  # 1,048,576 -> 10^6
                                        horse_list = [h1,h2,h3,h4,h5,h6,h7,h8,h9,h10]
                                        score = 0

                                        # 윷놀이 말 4개
                                        horse = dict()
                                        for idx in range(1, 4+1):
                                            horse[idx] = [1, 0]  # [위치 인덱스, 도착 여부(1:도착, 0:디폴트)]
                                        # 윷놀이 말 위치
                                        occupied = [0 for _ in range(33+1)]  # 해당 노드에 있는 말의 인덱스 저장 (시작과 도착 노드는 무시) len=1+33

                                        fail = 0  # 0:성공, 1:실패
                                        for t in range(10):  # 10^7
                                            h_idx = horse_list[t]  # 이번 턴에는, h 말이
                                            mv = move_list[t]  # 이번 턴에는, mv 만큼 움직여

                                            if horse[h_idx][1] == 1:  # [실패]
                                                fail = 1
                                                break

                                            c_node = horse[h_idx][0]
                                            n_node = move(c_node, mv)

                                            if occupied[n_node] != 0:  # [실패]
                                                fail = 1
                                                break

                                            if n_node == 33:  # 도착칸에 도착한 경우
                                                horse[h_idx][1] = 1
                                                occupied[c_node] = 0
                                            else:  # 일반 이동 -> occupied 변경, horse dict 변경, 득점
                                                horse[h_idx][0] = n_node
                                                occupied[c_node] = 0
                                                occupied[n_node] = h_idx
                                                score += node_value[n_node]

                                        if fail == 0:  # 성공
                                            if score > max_score:
                                                max_score = score

print(max_score)








