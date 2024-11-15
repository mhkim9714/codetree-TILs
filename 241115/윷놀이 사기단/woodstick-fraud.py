# 그래프 생성
node_idx = [i for i in range(33)]  # len=33의 일차원 리스트 (0~32)
node_value = [0, 2, 4, 6, 8,
              10, 12, 14, 16, 18,
              20, 22, 24, 26, 28,
              30, 32, 34, 36, 38,
              40, 13, 16, 19, 25,
              22, 24, 28, 27, 26,
              30, 35, 0]  # len=33
blue_node_idx = [5,10,15]
blue_edge = [21,25,27]
edge = [1, 2, 3, 4, 5,
        6, 7, 8, 9, 10,
        11, 12, 13, 14, 15,
        16, 17, 18, 19, 20,
        32, 22, 23, 24, 30,
        26, 24, 28, 29, 24,
        31, 20, 32]  # len=33

move_nums = list(map(int, input().split()))
max_score = 0
pos = [0,0,0,0]


def move(cur_node, mv_cnt):
    if cur_node in blue_node_idx:
        cur_node = blue_edge[blue_node_idx.index(cur_node)]
        mv_cnt -= 1

    for _ in range(mv_cnt):
        cur_node = edge[cur_node]
        if cur_node == 32:
            break

    return cur_node


def search_turn_score(turn, cur_score):
    global max_score
    global pos

    if turn == 10:
        max_score = max(max_score, cur_score)
        return

    for h in range(4):
        if pos[h] == 32:
            continue

        temp = pos[h]  # 이동 전 저장

        pos[h] = move(pos[h], move_nums[turn])
        if pos[h] == 32:
            search_turn_score(turn+1, cur_score+node_value[pos[h]])
        else:
            if pos.count(pos[h]) == 1:
                search_turn_score(turn+1, cur_score+node_value[pos[h]])

        pos[h] = temp  # 복구


search_turn_score(0, 0)  # turn(0~9)->10번째 평가, cur_score
print(max_score)
