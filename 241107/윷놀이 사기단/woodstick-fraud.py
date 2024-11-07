# 총 10^7짜리 알고리즘
# 그래프 생성
vertex_list = [i for i in range(1,34)]  # len=33의 일차원 리스트 (1~33)
special_vertex = [6,15,25]
special_edge = [11,16,24]
value_list = [-1,
              0,2,4,6,8,
              10,12,14,16,18,
              13,16,19,25,20,
              22,24,22,24,26,
              28,26,27,28,30,
              32,34,36,38,30,
              35,40,0]  # len=34의 일차원 리스트
edge_list = [-1,
             2,3,4,5,6,
             7,8,9,10,15,
             12,13,14,30,18,
             17,14,19,20,21,
             25,14,22,23,26,
             27,28,29,32,31,
             32,33,33]  # len=34의 일차원 리스트

move_list = list(map(int, input().split()))


def move(sidx, cnt):
    if sidx in special_vertex:
        sidx = special_edge[special_vertex.index(sidx)]
        cnt -= 1

    nidx = sidx
    for _ in range(cnt):
        nidx = edge_list[nidx]

    return nidx


max_val = -1
for h1 in range(4):
    for h2 in range(4):
        for h3 in range(4):
            for h4 in range(4):
                for h5 in range(4):
                    for h6 in range(4):
                        for h7 in range(4):
                            for h8 in range(4):
                                for h9 in range(4):
                                    for h10 in range(4): # (1,048,576)

                                        h_list = [h1,h2,h3,h4,h5,h6,h7,h8,h9,h10]
                                        cur_val = 0
                                        horse = [[1, 0] for _ in range(4)]  # [현재 위치 idx, done] -> 0:still playing / 1:done
                                        occupied = []

                                        for t in range(len(h_list)): # (10)
                                            h = h_list[t]
                                            mv_h = move_list[t]
                                            if horse[h][-1] == 1:  # 이미 끝난 말인 경우
                                                flag = 1
                                                break

                                            h_cidx = horse[h][0]
                                            h_nidx = move(horse[h][0], mv_h) # (5)

                                            if h_nidx == 33:  # done
                                                horse[h][-1] = 1
                                            elif h_nidx in occupied:  # 말이 겹쳐서 움직이지 못하는 경우
                                                flag = 1
                                                break
                                            else:  # 득점
                                                horse[h][0] = h_nidx
                                                if h_cidx != 1:
                                                    occupied.remove(h_cidx)
                                                occupied.append(h_nidx)
                                                cur_val += value_list[h_nidx]

                                        else:
                                            if max_val < cur_val:
                                                max_val = cur_val

print(max_val)