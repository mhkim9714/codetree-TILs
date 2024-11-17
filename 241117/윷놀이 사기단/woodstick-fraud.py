# 그래프 생성
node = [idx for idx in range(33)]  # 0~32
value = [0,2,4,6,8,
         10,12,13,16,18,
         20,22,24,26,28,
         30,32,34,36,38,
         40,13,16,19,22,
         24,25,28,27,26,
         30,35,0]  # 0~32
edge = [1,2,3,4,5,
        6,7,8,9,10,
        11,12,13,14,15,
        16,17,18,19,20,
        32,22,23,26,25,
        26,30,28,29,26,
        31,20,32]
special_node = [5,10,15]
special_edge = [21,24,27]

move_cnt = list(map(int, input().split()))


def backtracking(cnt, score, pos):  # cnt번 이동한 결과물이 score/pos
    global max_score
    if cnt == 10:
        max_score = max(max_score, score)
        return

    for h in range(4):  # 0~3번 말
        if pos[h] == 32:  # 도착칸에 도착한 말은 이동 불가능
            continue

        # 말 이동
        mv = move_cnt[cnt]
        c_pos = pos[h]
        if c_pos in special_node:
            n_pos = special_edge[special_node.index(c_pos)]
            mv -= 1
        else:
            n_pos = pos[h]
        for _ in range(mv):
            n_pos = edge[n_pos]

        if pos.count(n_pos) > 0:  # 도달하는 위치에 다른 말이 이미 있으면 불가능
            continue

        new_pos = pos[:]
        new_pos[h] = n_pos
        backtracking(cnt+1, score+value[n_pos], new_pos)  # DFS (return 조건 -> depth 10까지 서치 완료)


max_score = -1
backtracking(0, 0, [0,0,0,0])
print(max_score)
